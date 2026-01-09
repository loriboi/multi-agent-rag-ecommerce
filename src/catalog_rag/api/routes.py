from __future__ import annotations

from flask import Blueprint, jsonify, request

from catalog_rag.config import AppConfig
from catalog_rag.indexing.build import configure_local_embeddings
from catalog_rag.indexing.registry import topic_to_dir
from catalog_rag.agents.shoes_agent import ShoesAgent
from catalog_rag.agents.hoes_agent import HoesAgent
from catalog_rag.agents.router import SimpleKeywordRouter

api_bp = Blueprint("api", __name__)

# Initialize once at import time (simple + ok for demo)
_cfg = AppConfig()
configure_local_embeddings(_cfg.embed_model_name)

_storage_root = _cfg.abs_path(_cfg.storage_dir)
_dirs = topic_to_dir(_storage_root)

_shoes_agent = ShoesAgent(_dirs["shoes"])
_hoes_agent = HoesAgent(_dirs["hoes"])
_router = SimpleKeywordRouter()


@api_bp.post("/retrieve")
def retrieve_explicit():
    """
    POST /retrieve
    Body JSON:
      { "topic": "shoes"|"hoes", "query": "...", "top_k": 5 }
    """
    payload = request.get_json(force=True, silent=False) or {}
    topic = (payload.get("topic") or "").strip().lower()
    query = (payload.get("query") or "").strip()
    top_k = int(payload.get("top_k") or 5)

    if not query:
        return jsonify({"error": "Missing 'query'"}), 400
    if topic not in ("shoes", "hoes"):
        return jsonify({"error": "Invalid 'topic'. Use 'shoes' or 'hoes'."}), 400

    agent = _shoes_agent if topic == "shoes" else _hoes_agent
    res = agent.run(query=query, top_k=top_k)

    return jsonify(
        {
            "topic": res.topic,
            "query": res.query,
            "top_k": top_k,
            "results": res.results,
        }
    )


@api_bp.post("/query")
def query_auto():
    """
    POST /query
    Body JSON:
      { "query": "...", "top_k": 5 }
    Routes automatically to one or more agents, then returns merged results.
    """
    payload = request.get_json(force=True, silent=False) or {}
    query = (payload.get("query") or "").strip()
    top_k = int(payload.get("top_k") or 5)

    if not query:
        return jsonify({"error": "Missing 'query'"}), 400

    decision = _router.decide(query)
    results = []

    for t in decision.topics:
        if t == "shoes":
            results.append(_shoes_agent.run(query=query, top_k=top_k))
        elif t == "hoes":
            results.append(_hoes_agent.run(query=query, top_k=top_k))

    # Merge: simple concatenation; in una versione avanzata puoi rerankare
        results_by_topic = {}
    results_by_topic = {}
    merged = []

    for r in results:
        results_by_topic[r.topic] = r.results
        merged.extend(r.results)

    # facoltativo: ordina il merge per score desc
    merged.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    return jsonify(
        {
            "query": query,
            "routed_topics": decision.topics,
            "top_k_per_topic": top_k,
            "results_by_topic": results_by_topic,
            "results": merged,
        }
    )

