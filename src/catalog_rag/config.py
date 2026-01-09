from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    # Repo root = current working directory by default
    repo_root: Path = Path(os.getenv("CATALOG_RAG_REPO_ROOT", Path.cwd()))

    # Input data paths
    data_dir: Path = Path(os.getenv("CATALOG_RAG_DATA_DIR", "data"))
    shoes_json: Path = Path(os.getenv("CATALOG_RAG_SHOES_JSON", "data/shoes.json"))
    hoes_json: Path = Path(os.getenv("CATALOG_RAG_HOES_JSON", "data/hoes.json"))

    # Persisted indices root
    storage_dir: Path = Path(os.getenv("CATALOG_RAG_STORAGE_DIR", "storage"))

    # Local embedding model
    embed_model_name: str = os.getenv(
        "CATALOG_RAG_EMBED_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    def abs_path(self, p: Path) -> Path:
        # If p is already absolute, return it; else resolve relative to repo_root
        return p if p.is_absolute() else (self.repo_root / p).resolve()
