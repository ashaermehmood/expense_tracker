# Personal Expense Tracker

A simple command-line Python application to track personal expenses — add, view, search, total, edit, delete, sort, and export your spending.

## Features

- Add an expense (amount, category, description, date)
- View all expenses
- Search expenses by category
- Show total expenses (with a category breakdown)
- Delete an expense by ID
- Edit an existing expense
- Sort expenses by amount or date
- Monthly summary of spending
- Export all expenses to CSV
- Data is saved automatically to `expenses.json`

## Project Structure

```
expense_tracker/
├── main.py
├── expenses.json      (created automatically on first run)
├── expenses.csv        (created only if you use the export feature)
└── README.md
```

## How to Run

Requires Python 3.

```bash
python3 main.py
```

Then choose an option from the menu (0–9) and follow the prompts.

## Data Format

Each expense is stored as a JSON object like this:

```json
{
    "id": 1,
    "amount": 1200,
    "category": "Food",
    "description": "Pizza",
    "date": "2026-07-09"
}
```

All expenses are stored together in a JSON list inside `expenses.json`.

## Error Handling

The app is designed not to crash on bad input:
- Missing or empty `expenses.json` → starts with an empty list
- Invalid numeric input → asks again
- Invalid date format → asks again
- Searching a category that doesn't exist → reports no results found
- Deleting/editing a nonexistent ID → reports the ID wasn't found

## Possible Future Improvements

- Date range filtering
- Highest single expense lookup
- Multi-user support
- A simple GUI or web front end
