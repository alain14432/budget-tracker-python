from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .models import Transaction

# repo_root/src/storage.py -> repo_root/src -> repo_root
ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = ROOT_DIR / "data" / "transactions.json"


def load_transactions(path: Path = DEFAULT_DATA_PATH) -> List[Transaction]:
    """
    Load transactions from JSON.
    - If the file doesn't exist: return []
    - If file is corrupted or wrong shape: return [] (no crash)
    """
    try:
        if not path.exists():
            return []

        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []

        return [Transaction.from_dict(item) for item in raw]
    except Exception:
        return []


def save_transactions(transactions: List[Transaction], path: Path = DEFAULT_DATA_PATH) -> None:
    """
    Save transactions to JSON (atomic-ish write using a temp file).
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = [tx.to_dict() for tx in transactions]
    tmp_path = path.with_suffix(".tmp")

    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)
