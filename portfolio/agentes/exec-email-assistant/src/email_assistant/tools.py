from langchain_core.tools import tool
from .memory import SemanticMemory


_memory_store = None


def get_memory_store() -> SemanticMemory:
    """Get the global memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = SemanticMemory()
    return _memory_store


@tool
def check_calendar(date: str) -> str:
    """Check calendar availability for a given date.

    Args:
        date: Date to check in YYYY-MM-DD format.

    Returns:
        Calendar availability status.
    """
    busy_slots = ["10:00-11:00", "14:00-15:30"]
    return f"📅 {date}: Ocupado em {', '.join(busy_slots)}. Disponível: 09:00, 12:00, 16:00"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body content.

    Returns:
        Confirmation of email sent.
    """
    return f"✅ Email enviado para {to}\nAssunto: {subject}\nCorpo: {body[:100]}..."


@tool
def search_user_memory(query: str) -> str:
    """Search long-term memory for information about the user.

    Args:
        query: Search query for user information.

    Returns:
        Relevant facts from memory.
    """
    store = get_memory_store()
    facts = store.search_facts(query, k=3)
    if facts:
        return "🔍 Memória encontrada:\n" + "\n".join(f"- {f}" for f in facts)
    return "🔍 Nenhuma informação encontrada na memória."


@tool
def store_user_fact(fact: str) -> str:
    """Store an important fact about the user in long-term memory.

    Args:
        fact: The fact to remember.

    Returns:
        Confirmation that the fact was stored.
    """
    store = get_memory_store()
    store.store_fact(fact)
    return f"💾 Fato armazenado: {fact}"


def create_all_tools() -> list:
    """Create all tools for the email assistant.

    Returns:
        List of all available tools including langmem memory tools.
    """
    store = get_memory_store()
    manage_tool, search_tool = store.manage_tool, store.search_tool

    return [
        check_calendar,
        send_email,
        search_user_memory,
        store_user_fact,
        manage_tool,
        search_tool,
    ]
