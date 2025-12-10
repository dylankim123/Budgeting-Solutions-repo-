from collections import Counter

class Transaction:
    def __init__(self, amount, category, description, month):
        self.amount = amount
        self.category = category
        self.description = description
        self.month = month

    def save(self, filename="monthly_spending.txt"):
        """Save this transaction to a text file."""
        with open(filename, "a") as file:
            file.write(f"{self.month},{self.amount},{self.category},{self.description}\n")
        print("Transaction saved successfully.")

    @staticmethod
    def get_all_transactions(filename="monthly_spending.txt"):
        """Load all transactions from file as a list of Transaction objects."""
        transactions = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",", 3)
                    if len(parts) == 4:
                        month, amount, category, description = parts
                        transactions.append(Transaction(float(amount), category, description, month))
        except FileNotFoundError:
            print("No transaction file found.")
        return transactions

    @staticmethod
    def get_most_frequent_category(filename="monthly_spending.txt"):
        """Find and return the most frequent spending category."""
        categories = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",", 3)
                    if len(parts) >= 3:
                        categories.append(parts[2])
        except FileNotFoundError:
            return None

        if not categories:
            return None

        counter = Counter(categories)
        most_common = counter.most_common(1)
        return most_common[0][0] if most_common else None

def __str__(self):
        return (f"Month: {self.month}, "
                f"Amount: ${self.amount:.2f}, "
                f"Category: {self.category}, "
                f"Description: {self.description}")

def __repr__(self):
        return (f"Transaction(amount={self.amount}, "
                f"category='{self.category}', "
                f"description='{self.description}', "
                f"month='{self.month}')")
