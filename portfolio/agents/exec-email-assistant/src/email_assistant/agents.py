from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import create_all_tools, get_memory_store


def _llm(temperature: float = 0.3):
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)


CLASSIFIER_PROMPT = """Você é um classificador de e-mails executivos. Analise o e-mail e retorne APENAS uma das opções:
- reply: E-mail que precisa de resposta
- schedule: Pedido de agendamento/reunião
- archive: E-mail informativo, sem ação necessária
- search_memory: Precisa buscar informações na memória do usuário
- unknown: Não classificado

Retorne APENAS a classificação, sem explicações."""


def classifier_node(state: dict) -> dict:
    """Classify the email intent."""
    llm = _llm(0.1)
    email = state.get("email_content", "")
    sender = state.get("sender", "")
    subject = state.get("subject", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=(
            f"{CLASSIFIER_PROMPT}\n\n"
            f"De: {sender}\nAssunto: {subject}\n\n{email}"
        ))
    ])

    intent = response.content.strip().lower()
    valid_intents = ["reply", "schedule", "archive", "search_memory", "unknown"]
    if intent not in valid_intents:
        intent = "unknown"

    new_messages = messages + [
        HumanMessage(content=f"Novo e-mail de {sender}: {subject}"),
        AIMessage(content=f"Classificação: {intent}")
    ]

    needs_human = intent == "schedule"

    return {
        "intent": intent,
        "messages": new_messages,
        "current_phase": "process",
        "needs_human": needs_human,
    }


DRAFTER_PROMPT = """Você é um assistente executivo. Redija uma resposta profissional e concisa.
Seja cordial, direto e mantenha o tom executivo.
Não exceda 3 parágrafos."""


def draft_reply_node(state: dict) -> dict:
    """Draft a reply to the email."""
    llm = _llm(0.7)
    email = state.get("email_content", "")
    sender = state.get("sender", "")
    memory_context = state.get("memory_context", "")
    messages = state.get("messages", [])

    context = f"E-mail de: {sender}\n\n{email}"
    if memory_context:
        context += f"\n\nContexto da memória:\n{memory_context}"

    response = llm.invoke([
        HumanMessage(content=f"{DRAFTER_PROMPT}\n\n{context}")
    ])

    new_messages = messages + [
        AIMessage(content=f"[Rascunho] {response.content[:100]}...")
    ]

    return {
        "reply_draft": response.content,
        "messages": new_messages,
        "current_phase": "done",
    }


SCHEDULE_PROMPT = """Você é um assistente de agendamento. Analise o pedido de reunião e extraia:
- Pessoa a ser agendada
- Data sugerida
- Duração estimada
- Propósito da reunião

Retorne em formato estruturado."""


def schedule_node(state: dict) -> dict:
    """Process scheduling requests with HITL check."""
    llm = _llm(0.3)
    email = state.get("email_content", "")
    sender = state.get("sender", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=f"{SCHEDULE_PROMPT}\n\nE-mail de {sender}:\n{email}")
    ])

    memory = get_memory_store()
    has_existing = memory.has_schedule(sender)

    new_messages = messages + [
        AIMessage(content=f"[Agendamento] {response.content}")
    ]

    return {
        "schedule_info": response.content,
        "messages": new_messages,
        "current_phase": "human_review" if not has_existing else "done",
        "needs_human": not has_existing,
    }


MEMORY_SEARCH_PROMPT = """Você é um assistente que busca contexto na memória do usuário.
Dado o conteúdo do e-mail, determine quais informações devem ser buscadas na memória."""


def memory_search_node(state: dict) -> dict:
    """Search memory for relevant context before processing."""
    llm = _llm(0.3)
    email = state.get("email_content", "")
    sender = state.get("sender", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=(
            f"{MEMORY_SEARCH_PROMPT}\n\nE-mail de {sender}:\n{email}"
        ))
    ])

    memory = get_memory_store()
    facts = memory.search_facts(response.content, k=3)
    memory_context = "\n".join(f"- {f}" for f in facts) if facts else "Nenhum contexto encontrado."

    new_messages = messages + [
        AIMessage(content=f"[Memória] {memory_context}")
    ]

    return {
        "memory_context": memory_context,
        "messages": new_messages,
        "current_phase": "process",
    }


def human_review_node(state: dict) -> dict:
    """Handle human-in-the-loop review for scheduling."""
    schedule_info = state.get("schedule_info", "")
    sender = state.get("sender", "")

    memory = get_memory_store()
    memory.store_fact(
        f"Agendamento com {sender}: {schedule_info}",
        metadata={"type": "schedule", "person": sender}
    )

    return {
        "human_approval": "approved",
        "current_phase": "done",
        "needs_human": False,
    }
