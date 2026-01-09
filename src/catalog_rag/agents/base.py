from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class AgentResult:
    topic: str
    query: str
    results: List[Dict[str, Any]]


class Agent(Protocol):
    topic: str

    def run(self, query: str, top_k: int = 5) -> AgentResult:
        ...
