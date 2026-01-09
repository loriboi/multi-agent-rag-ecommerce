from __future__ import annotations

from typing import Any, Dict, List

from llama_index.core import Document


def product_to_document(product: Dict[str, Any], topic: str) -> Document:
    """
    Minimal, retrieval-oriented text representation + metadata.
    """
    attrs = product.get("attributes") or {}
    tags = product.get("tags") or []

    attrs_str = ", ".join(f"{k}: {v}" for k, v in attrs.items()) if attrs else ""
    tags_str = ", ".join(tags) if tags else ""

    text = (
        f"Name: {product.get('name','')}\n"
        f"Category: {product.get('category','')}\n"
        f"Brand: {product.get('brand','')}\n"
        f"Price: {product.get('price','')}\n"
        f"Available: {product.get('available','')}\n"
        f"Description: {product.get('description','')}\n"
        f"Attributes: {attrs_str}\n"
        f"Tags: {tags_str}\n"
    ).strip()

    metadata = {
        "id": product.get("id"),
        "topic": topic,
        "category": product.get("category"),
        "brand": product.get("brand"),
        "price": product.get("price"),
        "available": product.get("available"),
        "attributes": attrs,
        "tags": tags,
        "name": product.get("name"),
    }

    return Document(text=text, metadata=metadata)


def products_to_documents(products: List[Dict[str, Any]], topic: str) -> List[Document]:
    return [product_to_document(p, topic=topic) for p in products]
