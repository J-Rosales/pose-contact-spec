"""Load canonical pose-contact documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_document(path: str | Path) -> Any:
    """Load a YAML or JSON document from disk."""
    resolved = Path(path)
    with resolved.open(encoding="utf-8") as handle:
        if resolved.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)
