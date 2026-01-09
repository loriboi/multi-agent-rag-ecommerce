from __future__ import annotations

from pathlib import Path

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex


def load_index(persist_dir: Path) -> VectorStoreIndex:
    storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
    return load_index_from_storage(storage_context)
