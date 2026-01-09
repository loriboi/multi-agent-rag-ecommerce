from __future__ import annotations

from typing import Any, Dict, List

from llama_index.core import VectorStoreIndex


def retrieve(index: VectorStoreIndex, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieval-only. Returns a compact list of product-like dicts from node metadata.
    """
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)

    results: List[Dict[str, Any]] = []
    for n in nodes:
        md = dict(n.node.metadata) if n.node.metadata else {}
        results.append(
            {
                "id": md.get("id"),
                "name": md.get("name"),
                "brand": md.get("brand"),
                "category": md.get("category"),
                "price": md.get("price"),
                "available": md.get("available"),
                "topic": md.get("topic"),
                "score": float(getattr(n, "score", 0.0) or 0.0),
            }
        )
    return results
