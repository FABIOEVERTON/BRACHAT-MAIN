from langchain_core.vectorstores import InMemoryVectorStore


def create_embeddings():
    """Create Google Generative AI embeddings for semantic search."""
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def create_memory_tools():
    """Create langmem tools for memory management.

    Returns:
        Tuple of (manage_memory_tool, search_memory_tool)
    """
    from langmem import create_manage_memory_tool, create_search_memory_tool
    manage_tool = create_manage_memory_tool(namespace=("memories", "{namespace}"))
    search_tool = create_search_memory_tool(namespace=("memories", "{namespace}"))
    return manage_tool, search_tool


def create_vector_store():
    """Create an in-memory vector store with embeddings."""
    embeddings = create_embeddings()
    return InMemoryVectorStore.from_texts(
        texts=["Initial context placeholder"],
        embedding=embeddings,
        metadatas=[{"source": "init"}],
    )


class SemanticMemory:
    """Semantic memory manager for long-term facts and concepts."""

    def __init__(self):
        self._embeddings = None
        self._vector_store = None
        self._manage_tool = None
        self._search_tool = None
        self.facts: list[dict] = []

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = create_embeddings()
        return self._embeddings

    @property
    def vector_store(self):
        if self._vector_store is None:
            self._vector_store = InMemoryVectorStore(self.embeddings)
        return self._vector_store

    @property
    def manage_tool(self):
        if self._manage_tool is None:
            self._manage_tool, _ = create_memory_tools()
        return self._manage_tool

    @property
    def search_tool(self):
        if self._search_tool is None:
            _, self._search_tool = create_memory_tools()
        return self._search_tool

    def store_fact(self, fact: str, metadata: dict | None = None):
        """Store a fact in semantic memory."""
        meta = metadata or {"source": "conversation"}
        self.vector_store.add_texts([fact], metadatas=[meta])
        self.facts.append({"fact": fact, "metadata": meta})

    def search_facts(self, query: str, k: int = 3) -> list[str]:
        """Search for relevant facts in semantic memory."""
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def has_schedule(self, person: str) -> bool:
        """Check if a person already has a schedule."""
        facts = self.search_facts(f"agendamento {person}", k=5)
        return any(person.lower() in f.lower() for f in facts)

    def get_all_facts(self) -> list[dict]:
        """Return all stored facts."""
        return self.facts
