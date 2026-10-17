"""
vector_store.py – Build, persist, and query the Chroma vector store
that powers the Knowledge Retriever agent.
"""

from __future__ import annotations

import os
from typing import List, Dict

import chromadb
from chromadb.utils import embedding_functions

from config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    TOP_K_RESULTS,
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
)


# ---------------------------------------------------------------------------
# Embedding function (uses Google Gemini text-embedding-004)
# ---------------------------------------------------------------------------

class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """Embedding function using Google Generative AI (Gemini text-embedding-004)."""

    def __init__(self, api_key: str, model_name: str = "models/text-embedding-004"):
        self.api_key = api_key
        self.model_name = model_name
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        import google.generativeai as genai
        embeddings = []
        for text in input:
            res = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document",
            )
            embeddings.append(res["embedding"])
        return embeddings


def _get_embedding_fn():
    if hasattr(embedding_functions, "GoogleGenerativeAiEmbeddingFunction"):
        try:
            return embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=GOOGLE_API_KEY,
                model_name=EMBEDDING_MODEL,
            )
        except Exception:
            pass
    return GeminiEmbeddingFunction(
        api_key=GOOGLE_API_KEY,
        model_name=EMBEDDING_MODEL,
    )


# ---------------------------------------------------------------------------
# Build / load collection
# ---------------------------------------------------------------------------

def build_vector_store(documents: List[Dict]) -> chromadb.Collection:
    """
    Create (or overwrite) the Chroma collection from a list of KB dicts.
    Each dict must have: id, title, content, category.
    """
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    ef = _get_embedding_fn()

    # Delete old collection if it exists to allow rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [doc["id"] for doc in documents]
    texts = [f"{doc['title']}\n\n{doc['content']}" for doc in documents]
    metadatas = [{"category": doc["category"], "title": doc["title"]} for doc in documents]

    collection.add(documents=texts, ids=ids, metadatas=metadatas)
    print(f"[VectorStore] Built collection '{COLLECTION_NAME}' with {len(ids)} documents.")
    return collection


def get_collection() -> chromadb.Collection:
    """Load an existing Chroma collection (raises if not found)."""
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    ef = _get_embedding_fn()
    return client.get_collection(name=COLLECTION_NAME, embedding_function=ef)


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def retrieve_relevant_chunks(query: str, category_filter: str | None = None) -> List[Dict]:
    """
    Retrieve the top-K most relevant KB chunks for a query.
    Optionally filter by category metadata.

    Returns list of dicts: {id, content, title, category, distance}
    """
    collection = get_collection()

    where_filter = {"category": category_filter} if category_filter else None

    results = collection.query(
        query_texts=[query],
        n_results=TOP_K_RESULTS,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append(
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "title": results["metadatas"][0][i]["title"],
                "category": results["metadatas"][0][i]["category"],
                "distance": results["distances"][0][i],
            }
        )
    return chunks


# ---------------------------------------------------------------------------
# CLI helper
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from data.knowledge_base import KB_DOCUMENTS

    build_vector_store(KB_DOCUMENTS)
    sample = retrieve_relevant_chunks("my payment failed")
    for c in sample:
        print(f"  [{c['id']}] {c['title']} (dist={c['distance']:.3f})")
