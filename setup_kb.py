"""
setup_kb.py – One-shot script to build the Chroma vector store.
Run once before using the app or running evaluations.

Usage:
  python setup_kb.py
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from data.knowledge_base import KB_DOCUMENTS
from vector_store import build_vector_store, retrieve_relevant_chunks


def main():
    print("=" * 60)
    print(" Customer Support Triage Crew — Knowledge Base Setup")
    print("=" * 60)
    print(f"\nBuilding vector store from {len(KB_DOCUMENTS)} documents…\n")

    collection = build_vector_store(KB_DOCUMENTS)

    # Quick smoke test
    test_queries = [
        ("my payment failed", "billing"),
        ("app won't load", "technical"),
        ("reset my password", "account"),
        ("how do I contact support", "general"),
    ]

    print("\n── Smoke-test retrieval ──────────────────────────────────")
    for query, expected_cat in test_queries:
        chunks = retrieve_relevant_chunks(query)
        top = chunks[0] if chunks else {}
        match = "✓" if top.get("category") == expected_cat else "?"
        print(f"  {match} Query: '{query}' → [{top.get('id','?')}] {top.get('title','?')}")

    print("\n✅ Vector store built successfully!")
    print(f"   Persisted to: {os.path.abspath('./chroma_db')}\n")


if __name__ == "__main__":
    main()
