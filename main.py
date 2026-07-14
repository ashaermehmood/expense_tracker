"""
Personal Expense Tracker
-------------------------
A simple command-line application to track personal expenses.
Data is stored in expenses.json in the same folder as this script.

Author: (Ashaer Mehmood)
"""

import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


# ---------------------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------------------

def load_expenses():
    """Load the list of expenses from the JSON file.

    Returns an empty list if the file does not exist, is empty,
    or contains invalid JSON (so the app never crashes on startup).
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: could not read {DATA_FILE} ({e}). Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save the list of expenses to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
    except IOError as e:
        print(f"Error: could not save expenses ({e}).")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_next_id(expenses):
    """Return the next available integer ID (max existing ID + 1)."""
    if not expenses:
        return 1
    return max(expense["id"] for expense in expenses) + 1


def get_valid_amount():
    """Repeatedly prompt the user until a valid positive number is entered."""
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be greater than 0. Try again.")
                continue
            return amount
        except ValueError:
            print("Invalid number. Please enter a numeric amount (e.g. 250 or 99.50).")


def get_valid_date():
    """Prompt for a date in YYYY-MM-DD format, defaulting to today if left blank."""
    while True:
        raw = input("Date (YYYY-MM-DD), leave blank for today: ").strip()
        if raw == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# ---------------------------------------------------------------------------
# Core features
# ---------------------------------------------------------------------------

def add_expense(expenses):
    """Prompt the user for expense details and append a new expense."""
    # Validates  amount  and date  before saving 
    print("\n--- Add Expense ---")
    amount = get_valid_amount()
    category = input("Category: ").strip() or "Uncategorized"
    description = input("Description: ").strip()
    date = get_valid_date()

    expense = {
        "id": get_next_id(expenses),
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added with ID {expense['id']}.")


def view_expenses(expenses):
    """Print all expenses in a readable table format."""
     # Sorted by date for easier reading
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<4}{'Date':<12}{'Category':<15}{'Amount':<10}Description")
    print("-" * 60)
    for e in sorted(expenses, key=lambda x: x["date"]):
        print(f"{e['id']:<4}{e['date']:<12}{e['category']:<15}{e['amount']:<10.2f}{e['description']}")


def search_by_category(expenses):
    """Find and display all expenses matching a given category (case-insensitive)."""
     # Case-insensitive match so "Food" and "food" both work
    print("\n--- Search by Category ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    category = input("Enter category to search: ").strip().lower()
    results = [e for e in expenses if e["category"].lower() == category]

    if not results:
        print(f"No expenses found in category '{category}'.")
        return

    print(f"{'ID':<4}{'Date':<12}{'Category':<15}{'Amount':<10}Description")
    print("-" * 60)
    for e in results:
        print(f"{e['id']:<4}{e['date']:<12}{e['category']:<15}{e['amount']:<10.2f}{e['description']}")


def show_total(expenses):
    """Display the total of all recorded expenses, and a per-category breakdown."""
    # Uses accumulator pattern to sum amounts
    print("\n--- Total Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"Total spent: {total:.2f}")

    # Bonus: category summary
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    print("\nBy category:")
    for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:<15}{amount:.2f}")


def delete_expense(expenses):
    """Delete an expense by its ID, handling nonexistent IDs gracefully."""
    print("\n--- Delete Expense ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    raw_id = input("Enter the ID of the expense to delete: ").strip()
    try:
        expense_id = int(raw_id)
    except ValueError:
        print("Invalid ID. Please enter a whole number.")
        return

    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            confirm = input(f"Delete '{e['description']}' ({e['amount']:.2f})? (y/n): ").strip().lower()
            if confirm == "y":
                expenses.pop(i)
                save_expenses(expenses)
                print("Expense deleted.")
            else:
                print("Cancelled.")
            return

    print(f"No expense found with ID {expense_id}.")


# ---------------------------------------------------------------------------
# Bonus features
# ---------------------------------------------------------------------------

def edit_expense(expenses):
    """Edit an existing expense's fields, keeping the current value on blank input."""
    print("\n--- Edit Expense ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    raw_id = input("Enter the ID of the expense to edit: ").strip()
    try:
        expense_id = int(raw_id)
    except ValueError:
        print("Invalid ID.")
        return

    for e in expenses:
        if e["id"] == expense_id:
            print("Leave a field blank to keep its current value.")

            new_amount = input(f"Amount [{e['amount']}]: ").strip()
            if new_amount:
                try:
                    e["amount"] = float(new_amount)
                except ValueError:
                    print("Invalid amount, keeping original.")

            new_category = input(f"Category [{e['category']}]: ").strip()
            if new_category:
                e["category"] = new_category

            new_description = input(f"Description [{e['description']}]: ").strip()
            if new_description:
                e["description"] = new_description

            new_date = input(f"Date [{e['date']}]: ").strip()
            if new_date:
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    e["date"] = new_date
                except ValueError:
                    print("Invalid date, keeping original.")

            save_expenses(expenses)
            print("Expense updated.")
            return

    print(f"No expense found with ID {expense_id}.")


def sort_expenses(expenses):
    """Display expenses sorted by amount or date, ascending or descending."""
    print("\n--- Sort Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("Sort by: 1) Amount  2) Date")
    choice = input("Choose (1/2): ").strip()
    key = "amount" if choice == "1" else "date"

    order = input("Order: (a)scending or (d)escending? ").strip().lower()
    reverse = order == "d"

    sorted_list = sorted(expenses, key=lambda x: x[key], reverse=reverse)

    print(f"{'ID':<4}{'Date':<12}{'Category':<15}{'Amount':<10}Description")
    print("-" * 60)
    for e in sorted_list:
        print(f"{e['id']:<4}{e['date']:<12}{e['category']:<15}{e['amount']:<10.2f}{e['description']}")


def monthly_summary(expenses):
    """Show total spending grouped by year-month (YYYY-MM)."""
    print("\n--- Monthly Summary ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}
    for e in expenses:
        month = e["date"][:7]  # "YYYY-MM"
        summary[month] = summary.get(month, 0) + e["amount"]

    for month, total in sorted(summary.items()):
        print(f"{month}: {total:.2f}")


def export_csv(expenses):
    """Export all expenses to expenses.csv."""
    print("\n--- Export to CSV ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    filename = "expenses.csv"
    try:
        with open(filename, "w") as f:
            f.write("id,date,category,amount,description\n")
            for e in expenses:
                f.write(f"{e['id']},{e['date']},{e['category']},{e['amount']},{e['description']}\n")
        print(f"Exported to {filename}.")
    except IOError as e:
        print(f"Error exporting CSV: {e}")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU = """
===== Personal Expense Tracker =====
1. Add Expense
2. View All Expenses
3. Search by Category
4. Show Total Expenses
5. Delete an Expense
6. Edit an Expense
7. Sort Expenses
8. Monthly Summary
9. Export to CSV
0. Exit
"""


def main():
    expenses = load_expenses()

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            search_by_category(expenses)
        elif choice == "4":
            show_total(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            edit_expense(expenses)
        elif choice == "7":
            sort_expenses(expenses)
        elif choice == "8":
            monthly_summary(expenses)
        elif choice == "9":
            export_csv(expenses)
        elif choice == "0":
            print("Goodbye! Your data has been saved.")
            break
        else:
            print("Invalid option. Please choose a number from the menu.")


if __name__ == "__main__":
    main()
