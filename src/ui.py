from __future__ import annotations

from typing import Optional, Set


def print_menu() -> None:
    print("\n=== Personal Budget Tracker ===")
    print("1) Add transaction")
    print("2) List transactions")
    print("3) Summary")
    print("4) Edit transaction")
    print("5) Delete transaction")
    print("0) Exit")


def prompt(text: str) -> str:
    return input(text).strip()


def prompt_optional(text: str) -> Optional[str]:
    val = input(text).strip()
    return val if val else None


def prompt_float(text: str) -> float:
    while True:
        s = input(text).strip()
        try:
            return float(s)
        except ValueError:
            print("Invalid number. Try again.")


def prompt_int(text: str) -> int:
    while True:
        s = input(text).strip()
        try:
            return int(s)
        except ValueError:
            print("Invalid integer. Try again.")


def confirm(text: str) -> bool:
    s = input(f"{text} (y/n): ").strip().lower()
    return s in {"y", "yes"}


def prompt_choice(text: str, choices: Set[str]) -> str:
    """
    Keep asking until the user enters one of the allowed choices (case-insensitive).
    """
    allowed = {c.lower() for c in choices}
    while True:
        val = input(text).strip().lower()
        if val in allowed:
            return val
        print(f"Invalid choice. Choose one of: {', '.join(sorted(allowed))}")


def prompt_choice_optional(text: str, choices: Set[str]) -> Optional[str]:
    """
    Allow blank (returns None) OR a valid choice.
    """
    allowed = {c.lower() for c in choices}
    while True:
        val = input(text).strip().lower()
        if val == "":
            return None
        if val in allowed:
            return val
        print(f"Invalid choice. Choose one of: {', '.join(sorted(allowed))} (or press Enter to skip)")
