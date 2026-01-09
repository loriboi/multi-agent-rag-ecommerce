from __future__ import annotations

from pathlib import Path
from typing import Dict


def topic_to_dir(storage_root: Path) -> Dict[str, Path]:
    """
    Central registry mapping: topic -> persisted index directory.
    """
    return {
        "shoes": storage_root / "shoes",
        "hoes": storage_root / "hoes",
    }
