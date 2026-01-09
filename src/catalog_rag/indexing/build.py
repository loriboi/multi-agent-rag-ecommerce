from __future__ import annotations

from pathlib import Path
from typing import List

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def configure_local_embeddings(model_name: str) -> None:
    """
    Configure local embeddings. Retrieval-only (no LLM).
    """
    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
    Settings.llm = None


def build_and_persist_index(docs: List[Document], persist_dir: Path) -> None:
    persist_dir.mkdir(parents=True, exist_ok=True)

    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)

    index = VectorStoreIndex.from_documents(
        docs,
        transformations=[splitter],
    )

    index.storage_context.persist(persist_dir=str(persist_dir))
