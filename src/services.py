from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from .models import Transaction


# ---------- helpers / validation ----------

def _next_id(transactions: List[Transaction]) -> int:
    return max((tx.id for tx in transactions), default=0) + 1


def parse_date_or_today(s: str) -> date:
    s = (s or "").strip()
    if not s:
        return date.today()
    return datetime.strptime(s, "%Y-%m-%d").date()


def normalize_type(tx_type: str) -> str:
    tx_type = (tx_type or "").strip().lower()
    if tx_type not in {"income", "expense"}:
        raise ValueError("Type must be 'income' or 'expense'.")
    return tx_type


def normalize_category(category: str) -> str:
    category = (category or "").strip()
    return category if category else "Uncategorized"


def normalize_amount(amount) -> float:
    amt = float(amount)
    if amt <= 0:
        raise ValueError("Amount must be a positive number.")
    return amt


# ---------- core operations ----------

def add_transaction(
    transactions: List[Transaction],
    tx_date: date,
    tx_type: str,
    category: str,
    amount: float,
    note: str = "",
) -> Transaction:
    tx = Transaction(
        id=_next_id(transactions),
        date=tx_date,
        tx_type=normalize_type(tx_type),
        category=normalize_category(category),
        amount=normalize_amount(amount),
        note=(note or "").strip(),
    )
    transactions.append(tx)
    return tx


def filter_transactions(
    transactions: List[Transaction],
    month: Optional[str] = None,        # "YYYY-MM"
    category: Optional[str] = None,
    tx_type: Optional[str] = None,      # "income" or "expense"
) -> List[Transaction]:
    result = list(transactions)

    if month:
        month = month.strip()
        result = [tx for tx in result if tx.date.strftime("%Y-%m") == month]

    if category:
        c = category.strip().lower()
        result = [tx for tx in result if tx.category.lower() == c]

    if tx_type:
        t = normalize_type(tx_type)
        result = [tx for tx in result if tx.tx_type == t]

    return sorted(result, key=lambda t: (t.date, t.id))


def get_summary(transactions: List[Transaction], month: Optional[str] = None) -> dict:
    scoped = filter_transactions(transactions, month=month) if month else list(transactions)
    income = sum(tx.amount for tx in scoped if tx.tx_type == "income")
    expenses = sum(tx.amount for tx in scoped if tx.tx_type == "expense")
    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": income - expenses,
        "count": len(scoped),
    }


def update_transaction(transactions: List[Transaction], tx_id: int, **changes) -> bool:
    """
    changes can include: date, type, category, amount, note
    Return True if updated, False if ID not found.
    """
    for tx in transactions:
        if tx.id == tx_id:
            if "date" in changes and changes["date"] is not None:
                tx.date = parse_date_or_today(str(changes["date"]))
            if "type" in changes and changes["type"] is not None:
                tx.tx_type = normalize_type(str(changes["type"]))
            if "category" in changes and changes["category"] is not None:
                tx.category = normalize_category(str(changes["category"]))
            if "amount" in changes and changes["amount"] is not None:
                tx.amount = normalize_amount(changes["amount"])
            if "note" in changes and changes["note"] is not None:
                tx.note = str(changes["note"]).strip()
            return True
    return False


def delete_transaction(transactions: List[Transaction], tx_id: int) -> bool:
    for i, tx in enumerate(transactions):
        if tx.id == tx_id:
            transactions.pop(i)
            return True
    return False
