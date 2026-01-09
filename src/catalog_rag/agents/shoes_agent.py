from __future__ import annotations

from pathlib import Path

from catalog_rag.agents.base import AgentResult
from catalog_rag.retrieval.load import load_index
from catalog_rag.retrieval.retriever import retrieve


class ShoesAgent:
    topic = "shoes"

    def __init__(self, index_dir: Path):
        self._index = load_index(index_dir)

    def run(self, query: str, top_k: int = 5) -> AgentResult:
        return AgentResult(
            topic=self.topic,
            query=query,
            results=retrieve(self._index, query=query, top_k=top_k),
        )
