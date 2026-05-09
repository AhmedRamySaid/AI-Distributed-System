"""
rag/retriever.py — ChromaDB-backed RAG retriever.

Uses the same TF-IDF embedding function as ingest.py so vectors
are compatible with the stored collection (no internet needed).

The function retrieve_context(query) is what gpu_worker.py calls:
    context = retrieve_context(request.query)
"""

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from knowledge_base import DOCUMENTS

# ── Config ────────────────────────────────────────────────────────────────────
COLLECTION_NAME = "study_techniques"
DB_PATH = "./chroma_db"          # same path used in ingest.py
TOP_K = 3                        # number of passages to retrieve


# ── Embedding function (must match ingest.py exactly) ─────────────────────────
class TFIDFEmbeddingFunction(EmbeddingFunction):
    """Offline TF-IDF embeddings — no internet required."""

    def __init__(self, corpus: list[str]):
        self.vectorizer = TfidfVectorizer(max_features=512, stop_words="english")
        self.vectorizer.fit(corpus)

    def __call__(self, input: Documents) -> Embeddings:
        return self.vectorizer.transform(input).toarray().tolist()


# ── Singleton client / collection (loaded once per process) ───────────────────
_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        corpus = [doc["text"] for doc in DOCUMENTS]
        ef = TFIDFEmbeddingFunction(corpus=corpus)

        client = chromadb.PersistentClient(path=DB_PATH)
        _collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
        )
    return _collection


# ── Public API ─────────────────────────────────────────────────────────────────
def retrieve_context(query: str, top_k: int = TOP_K) -> str:
    """
    Retrieve the most relevant passages for `query` from ChromaDB.

    Returns a single formatted string ready to be injected into the LLM prompt.
    Example output:
        [Context 1] Spaced repetition is one of the most evidence-backed...
        [Context 2] Active recall means testing yourself...
    """
    collection = _get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]       # list of passage strings
    metadatas = results["metadatas"][0]       # list of metadata dicts
    distances = results["distances"][0]       # cosine distances (lower = closer)

    if not documents:
        return "No relevant context found."

    parts = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), start=1):
        technique = meta.get("technique", "unknown")
        topic     = meta.get("topic", "unknown")
        similarity = round(1 - dist, 3)       # convert distance → similarity score
        parts.append(
            f"[Context {i} | technique: {technique} | topic: {topic} | score: {similarity}]\n{doc}"
        )

    return "\n\n".join(parts)


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "How can I remember things better for my exam?",
        "I keep losing focus while studying",
        "What is the best way to understand a hard concept?",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print("-" * 60)
        ctx = retrieve_context(q)
        print(ctx)