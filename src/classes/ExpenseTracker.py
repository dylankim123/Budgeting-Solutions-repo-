import os
from datetime import datetime
from collections import Counter
from Classes import Expense

class ExpenseTracker:
    """Tracks and analyzes user expenses."""

    def __init__(self):
        self._expenses = []

    def add_expense(self, expense: Expense):
        if not isinstance(expense, Expense):
            raise TypeError("Expected an Expense object.")
        self._expenses.append(expense)

    def get_total_spending(self):
        """Calculates total money spent."""
        return sum(e.amount for e in self._expenses)

    def get_most_frequent_category(self):
        """Finds most frequent spending category."""
        if not self._expenses:
            return None
        categories = [e.category for e in self._expenses]
        return Counter(categories).most_common(1)[0][0]

    def save_to_file(self, filename="monthly_spending.txt"):
        """Appends all expenses to a local file."""
        with open(filename, "a") as f:
            for e in self._expenses:
                f.write(f"{e.date},{e.amount},{e.category},{e.description}\n")

    def __str__(self):
        return f"Total Expenses: ${self.get_total_spending():,.2f}"

    def __repr__(self):
        return f"ExpenseTracker({len(self._expenses)} expenses)"
