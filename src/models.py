from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Transaction:
    id: int
    date: date
    tx_type: str  # "income" or "expense"
    category: str
    amount: float
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "type": self.tx_type,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
        }

    @staticmethod
    def from_dict(d: dict) -> "Transaction":
        tx_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        return Transaction(
            id=int(d["id"]),
            date=tx_date,
            tx_type=str(d["type"]).strip().lower(),
            category=str(d["category"]).strip(),
            amount=float(d["amount"]),
            note=str(d.get("note", "")).strip(),
        )
