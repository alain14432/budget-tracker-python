from __future__ import annotations

from .storage import load_transactions, save_transactions
from .services import (
    add_transaction,
    delete_transaction,
    filter_transactions,
    get_summary,
    parse_date_or_today,
    update_transaction,
)
from .ui import confirm, print_menu, prompt, prompt_float, prompt_int, prompt_optional


def print_table(rows) -> None:
    headers = ["ID", "Date", "Type", "Category", "Amount", "Note"]
    widths = [4, 10, 8, 16, 10, 30]

    def fmt_row(cols):
        return "  ".join(str(c)[:w].ljust(w) for c, w in zip(cols, widths))

    print("\n" + fmt_row(headers))
    print("-" * (sum(widths) + 10))
    for tx in rows:
        print(
            fmt_row(
                [
                    tx.id,
                    tx.date.isoformat(),
                    tx.tx_type,
                    tx.category,
                    f"{tx.amount:.2f}",
                    tx.note,
                ]
            )
        )


def main() -> None:
    transactions = load_transactions()

    while True:
        print_menu()
        choice = prompt("Choose an option: ")

        try:
            if choice == "1":
                d = prompt_optional("Date (YYYY-MM-DD) [blank=today]: ")
                tx_date = parse_date_or_today(d or "")

                tx_type = prompt("Type (income/expense): ").lower()
                category = prompt("Category [blank=Uncategorized]: ")
                amount = prompt_float("Amount (positive number): ")
                note = prompt("Note (optional): ")

                tx = add_transaction(transactions, tx_date, tx_type, category, amount, note)
                save_transactions(transactions)
                print(f"Added transaction #{tx.id} ✅")

            elif choice == "2":
                month = prompt_optional("Filter month (YYYY-MM) [blank=all]: ")
                category = prompt_optional("Filter category [blank=all]: ")
                tx_type = prompt_optional("Filter type (income/expense) [blank=all]: ")

                rows = filter_transactions(transactions, month=month, category=category, tx_type=tx_type)
                if not rows:
                    print("No transactions found.")
                else:
                    print_table(rows)

            elif choice == "3":
                month = prompt_optional("Summary month (YYYY-MM) [blank=overall]: ")
                s = get_summary(transactions, month=month)
                print("\n--- Summary ---")
                print(f"Transactions:   {s['count']}")
                print(f"Total income:   {s['total_income']:.2f}")
                print(f"Total expenses: {s['total_expenses']:.2f}")
                print(f"Net balance:    {s['net_balance']:.2f}")

            elif choice == "4":
                tx_id = prompt_int("Transaction ID to edit: ")
                print("Leave blank to keep current value.\n")

                new_date = prompt_optional("New date (YYYY-MM-DD): ")
                new_type = prompt_optional("New type (income/expense): ")
                new_cat = prompt_optional("New category: ")
                new_amt = prompt_optional("New amount: ")
                new_note = prompt_optional("New note: ")

                ok = update_transaction(
                    transactions,
                    tx_id,
                    date=new_date,
                    type=new_type,
                    category=new_cat,
                    amount=float(new_amt) if new_amt else None,
                    note=new_note,
                )
                if ok:
                    save_transactions(transactions)
                    print("Updated ✅")
                else:
                    print("ID not found.")

            elif choice == "5":
                tx_id = prompt_int("Transaction ID to delete: ")
                if confirm("Are you sure you want to delete this transaction?"):
                    ok = delete_transaction(transactions, tx_id)
                    if ok:
                        save_transactions(transactions)
                        print("Deleted ✅")
                    else:
                        print("ID not found.")
                else:
                    print("Cancelled.")

            elif choice == "0":
                save_transactions(transactions)
                print("Goodbye 👋")
                break

            else:
                print("Invalid option. Try again.")

        except Exception:
            # never show a Python stack trace to the user
            print("Something went wrong with that input. Please try again.")


if __name__ == "__main__":
    main()
