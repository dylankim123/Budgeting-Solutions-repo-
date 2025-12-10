import os
from datetime import datetime
from collections import Counter
from Classes import User, ExpenseTracker, Finance

class BudgetAnalyzer:
    """Analyzes spending patterns and overall budget health."""

    def __init__(self, user: User, tracker: ExpenseTracker, finance: Finance):
        self.user = user
        self.tracker = tracker
        self.finance = finance

    def calculate_budget_balance(self):
        """Returns remaining balance after expenses."""
        after_tax = self.finance.calculate_after_tax_income()
        total_spent = self.tracker.get_total_spending()
        return after_tax - total_spent

    def detect_spending_trends(self):
        """Placeholder for trend analysis (can expand later)."""
        return self.tracker.get_most_frequent_category()

    def generate_report(self):
        """Generates a summary of the user's monthly budget."""
        balance = self.calculate_budget_balance()
        trend = self.detect_spending_trends()
        return (
            f"\n=== {self.user.username}'s Budget Report ===\n"
            f"Gross Income: ${self.finance.salary:,.2f}\n"
            f"After-Tax Income: ${self.finance.calculate_after_tax_income():,.2f}\n"
            f"Total Spending: ${self.tracker.get_total_spending():,.2f}\n"
            f"Most Frequent Category: {trend}\n"
            f"Remaining Balance: ${balance:,.2f}\n"
        )

