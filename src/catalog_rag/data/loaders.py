from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_products_json(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list in {path}, got: {type(data).__name__}")

    return data
