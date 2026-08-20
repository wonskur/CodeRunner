from typing import Any
import json
import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("FORGE_DATA_DIR", Path(__file__).resolve().parents[2] / "data"))


def load_json(name: str) -> Any:
    path = DATA_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(name: str, data: Any) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)