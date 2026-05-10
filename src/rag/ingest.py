"""
ingest.py — Load the study knowledge base into ChromaDB.
Run this once (or whenever you add new documents).

Uses a local TF-IDF embedding function (no internet needed).
In production, swap embed_fn for OpenAI or a HuggingFace model.

Usage:
    python ingest.py
"""

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer
from common.knowledge_base import DOCUMENTS

# ── Path ──────────────────────────────────────────────────────────────────────
import os

# Get the absolute path to the directory containing retriever.py
current_file_path = os.path.abspath(__file__)

# Go up two levels (rag/ -> src/ -> root) to get to the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# Combine root with the database folder name
DB_PATH = os.path.join(project_root, "common/chroma_db")

COLLECTION_NAME = "study_techniques"


class TFIDFEmbeddingFunction(EmbeddingFunction):
    """Simple offline embedding function using TF-IDF."""

    def __init__(self, corpus: list[str]):
        self.vectorizer = TfidfVectorizer(max_features=512, stop_words="english")
        self.vectorizer.fit(corpus)

    def __call__(self, input: Documents) -> Embeddings:
        vecs = self.vectorizer.transform(input).toarray().tolist()
        return vecs


def ingest():
    all_texts = [doc["text"] for doc in DOCUMENTS]
    ef = TFIDFEmbeddingFunction(corpus=all_texts)

    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Cleared existing collection.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    ids       = [doc["id"]       for doc in DOCUMENTS]
    texts     = [doc["text"]     for doc in DOCUMENTS]
    metadatas = [doc["metadata"] for doc in DOCUMENTS]

    collection.add(documents=texts, metadatas=metadatas, ids=ids)

    print(f"Ingested {len(DOCUMENTS)} documents into '{COLLECTION_NAME}'.")
    print("Topics loaded:")
    for doc in DOCUMENTS:
        print(f"  • {doc['id']}")


if __name__ == "__main__":
    ingest()