#!/usr/bin/env python3
from __future__ import annotations

from catalog_rag.config import AppConfig
from catalog_rag.data.loaders import load_products_json
from catalog_rag.data.mappers import products_to_documents
from catalog_rag.indexing.build import configure_local_embeddings, build_and_persist_index
from catalog_rag.indexing.registry import topic_to_dir


def main() -> None:
    cfg = AppConfig()

    # Local embeddings
    configure_local_embeddings(cfg.embed_model_name)

    storage_root = cfg.abs_path(cfg.storage_dir)
    mapping = topic_to_dir(storage_root)

    shoes_path = cfg.abs_path(cfg.shoes_json)
    hoes_path = cfg.abs_path(cfg.hoes_json)

    shoes_products = load_products_json(shoes_path)
    hoes_products = load_products_json(hoes_path)

    shoes_docs = products_to_documents(shoes_products, topic="shoes")
    hoes_docs = products_to_documents(hoes_products, topic="hoes")

    build_and_persist_index(shoes_docs, mapping["shoes"])
    build_and_persist_index(hoes_docs, mapping["hoes"])

    print("Done. Persisted indices:")
    print(f" - shoes: {mapping['shoes']}")
    print(f" - hoes:  {mapping['hoes']}")


if __name__ == "__main__":
    main()
