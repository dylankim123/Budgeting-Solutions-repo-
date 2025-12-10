import os
from datetime import datetime
from collections import Counter

class Expense:
    """Represents a single spending transaction."""

    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = self._validate_amount(amount)
        self.category = category.strip()
        self.description = description.strip()
        self.date = self._validate_date(date)

    @staticmethod
    def _validate_amount(amount):
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")
        return amount

    @staticmethod
    def _validate_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def to_dict(self):
        """Converts expense data to dictionary form for file storage."""
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat()
        }

    def __str__(self):
        return f"${self.amount:.2f} — {self.category} ({self.date})"

    def __repr__(self):
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}')"
