from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def _llm(temperature: float = 0.7):
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)


PLANNER_PROMPT = """Você é um Planejador de Redações. Dado um tópico, crie um plano estruturado:
1. Título provável
2. Introdução (tese)
3. Desenvolvimento (3-4 argumentos)
4. Conclusão
Seja conciso e direto."""

WRITER_PROMPT = """Você é um Escritor Profissional. Escreva uma redação completa baseada no plano e notas de pesquisa.
Formato: texto corrido, parágrafos bem estruturados, linguagem formal."""

RESEARCHER_PROMPT = """Você é um Pesquisador. Para o tópico fornecido, gere notas de pesquisa com:
- Fatos relevantes
- Dados estatísticos (mesmo que fictícios para demonstração)
- Referências conceituais
Seja objetivo e conciso."""

REFLECTOR_PROMPT = """Você é um Refletor. Analise o rascunho atual e forneça uma reflexão sobre:
- Coerência do texto
- Força dos argumentos
- Sugestões de melhoria
Seja construtivo e específico."""

CRITIC_PROMPT = """Você é um Crítico Literário. Avalie o rascunho com foco em:
- Gramática e estilo
- Originalidade
- Impacto do texto
Dê uma nota de 1-10 e justifique."""


def planner_node(state: dict) -> dict:
    llm = _llm(0.7)
    topic = state["topic"]
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=f"{PLANNER_PROMPT}\n\nTópico: {topic}")
    ])

    new_messages = messages + [
        HumanMessage(content=f"Planeje uma redação sobre: {topic}"),
        AIMessage(content=response.content)
    ]

    return {
        "planner_output": response.content,
        "messages": new_messages,
        "current_phase": "researching"
    }


def researcher_node(state: dict) -> dict:
    llm = _llm(0.5)
    topic = state["topic"]
    plan = state.get("planner_output", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=f"{RESEARCHER_PROMPT}\n\nTópico: {topic}\nPlano: {plan}")
    ])

    new_messages = messages + [
        AIMessage(content=f"[Pesquisa] {response.content}")
    ]

    return {
        "research_notes": response.content,
        "messages": new_messages,
        "current_phase": "writing"
    }


def writer_node(state: dict) -> dict:
    llm = _llm(0.8)
    topic = state["topic"]
    plan = state.get("planner_output", "")
    research = state.get("research_notes", "")
    critique = state.get("critique", "")
    messages = state.get("messages", [])

    context = f"Plano: {plan}\n\nPesquisa: {research}"
    if critique:
        context += f"\n\nCrítica anterior: {critique}\nIncorpore as sugestões."

    response = llm.invoke([
        HumanMessage(content=f"{WRITER_PROMPT}\n\n{context}\n\nTópico: {topic}")
    ])

    new_messages = messages + [
        AIMessage(content=f"[Rascunho] {response.content[:200]}...")
    ]

    return {
        "draft": response.content,
        "messages": new_messages,
        "current_phase": "reflecting"
    }


def reflector_node(state: dict) -> dict:
    llm = _llm(0.6)
    draft = state.get("draft", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=f"{REFLECTOR_PROMPT}\n\nRascunho:\n{draft}")
    ])

    new_messages = messages + [
        AIMessage(content=f"[Reflexão] {response.content}")
    ]

    return {
        "reflection": response.content,
        "messages": new_messages,
        "current_phase": "critiquing"
    }


def critic_node(state: dict) -> dict:
    llm = _llm(0.5)
    draft = state.get("draft", "")
    reflection = state.get("reflection", "")
    messages = state.get("messages", [])

    response = llm.invoke([
        HumanMessage(content=(
            f"{CRITIC_PROMPT}\n\nRascunho:\n{draft}\n\nReflexão:\n{reflection}"
        ))
    ])

    iteration = state.get("iteration", 0) + 1
    max_iter = state.get("max_iterations", 3)
    new_messages = messages + [
        AIMessage(content=f"[Crítica] {response.content}")
    ]

    next_phase = "writing" if iteration < max_iter else "done"

    return {
        "critique": response.content,
        "messages": new_messages,
        "iteration": iteration,
        "current_phase": next_phase
    }
