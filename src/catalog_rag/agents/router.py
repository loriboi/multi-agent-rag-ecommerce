from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RouteDecision:
    topics: List[str]


class SimpleKeywordRouter:
    """
    Minimal deterministic router:
    - Routes to 'shoes' if query mentions shoe-like terms
    - Routes to 'hoes' if query mentions hoodie/sweatshirt-like terms
    - Routes to both if ambiguous
    """

    SHOES_KW = {
        "scarpa", "scarpe", "sneaker", "sneakers", "stivale", "stivali",
        "sandalo", "sandali", "mocassino", "mocassini", "trekking", "running",
        "scarponi", "scarponcini",
    }

    HOES_KW = {
        "felpa", "felpe", "hoodie", "sweatshirt", "zip", "cappuccio",
        "oversize", "pullover",
    }

    def decide(self, query: str) -> RouteDecision:
        q = query.lower()

        shoes_hit = any(k in q for k in self.SHOES_KW)
        hoes_hit = any(k in q for k in self.HOES_KW)

        if shoes_hit and hoes_hit:
            return RouteDecision(topics=["shoes", "hoes"])
        if shoes_hit:
            return RouteDecision(topics=["shoes"])
        if hoes_hit:
            return RouteDecision(topics=["hoes"])

        # fallback: query ambiguous, search both
        return RouteDecision(topics=["shoes", "hoes"])
