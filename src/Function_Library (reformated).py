import os
import random
from collections import Counter

# ------------------------------
# Simple Functions
# ------------------------------

def get_numeric_input(prompt: str, integer_only: bool = False) -> float | int:
    """
    Prompt the user for numeric input with validation.

    Args:
        prompt (str): The input message to display.
        integer_only (bool): If True, only accept whole numbers.

    Returns:
        float | int: The numeric input from the user.
    """
    while True:
        user_input = input(prompt)
        try:
            number = float(user_input)
            if integer_only and number != int(number):
                print("Please enter a whole number.")
            else:
                return int(number) if integer_only else number
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_valid_input(prompt: str, valid_options: list[str]) -> str:
    """
    Prompt the user until a valid input from valid_options is entered.

    Args:
        prompt (str): The input message to display.
        valid_options (list[str]): List of valid responses.

    Returns:
        str: The validated input.
    """
    while True:
        value = input(prompt).strip()
        if value in valid_options:
            return value
        print(f"Invalid input. Valid options: {', '.join(valid_options)}")


def generate_unique_identifier() -> int:
    """
    Generate a random 6-digit identifier.

    Returns:
        int: Random identifier.
    """
    return random.randint(100000, 999999)


def what_month() -> int:
    """Prompt user to enter a valid month (1–12)."""
    return get_numeric_input("Enter the month (MM format): ", integer_only=True)


def what_year() -> int:
    """Prompt user to enter a valid 4-digit year."""
    while True:
        year = get_numeric_input("Enter the year (YYYY format): ", integer_only=True)
        if len(str(year)) == 4:
            return year
        print("Invalid year. Please enter a 4-digit year.")


# ------------------------------
# Medium Functions
# ------------------------------

def is_username_taken_from_file(username: str, filename: str = "users.txt") -> bool:
    """
    Check if the username exists in the file.

    Args:
        username (str): Username to check.
        filename (str): File containing usernames.

    Returns:
        bool: True if taken, False if available.
    """
    try:
        with open(filename, "r") as f:
            for line in f:
                if username.lower() == line.strip().split(",")[0].lower():
                    return True
        return False
    except FileNotFoundError:
        return False


def calculate_money_available_after_tax(salary: float, tax_rate: float) -> float:
    """
    Calculate money available after tax deduction.

    Args:
        salary (float): Gross salary.
        tax_rate (float): Tax rate (0–1).

    Returns:
        float: Net salary after taxes.
    """
    if salary < 0:
        raise ValueError("Salary cannot be negative.")
    if not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1.")
    return salary * (1 - tax_rate)


def purchase_category() -> str:
    """Prompt user to select a spending category."""
    categories = {1: "Utilities", 2: "Rent", 3: "Leisure"}
    while True:
        print("Select a purchase category:")
        for key, value in categories.items():
            print(f"{key}: {value}")
        choice = get_numeric_input("Enter category number: ", integer_only=True)
        if choice in categories:
            return categories[choice]
        print("Invalid category number.")


def what_state() -> str:
    """Prompt user to enter a valid US state."""
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
        "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]
    return get_valid_input("Enter your state: ", states)


def track_monthly_spending(amount: float, category: str, description: str, month: int) -> None:
    """Append spending entry to file."""
    with open("monthly_spending.txt", "a") as file:
        file.write(f"{month},{amount},{category},{description}\n")


# ------------------------------
# Complex Functions
# ------------------------------

def username_creation() -> None:
    """
    Prompt user to create a unique username and save it.

    Raises:
        IOError: If file cannot be written.
    """
    while True:
        username = input("Create a username: ").strip()
        if is_username_taken_from_file(username):
            print("Username taken. Try another.")
        else:
            try:
                with open("users.txt", "a") as file:
                    file.write(username + "\n")
                print(f"Username '{username}' saved successfully.")
                break
            except IOError as e:
                print(f"Error writing to file: {e}")


def save_budget_summary(income: float, spending: float, category_breakdown: dict[int, float], month: int, year: int) -> None:
    """Save full monthly budget to a file."""
    with open("budget.txt", "a") as file:
        file.write(f"{month}/{year} - Income: {income}, Spending: {spending}\n")
        for category, amount in category_breakdown.items():
            file.write(f"  {category}: {amount}\n")


def get_most_frequent_transaction_category() -> str | None:
    """
    Return the most frequent transaction category from file.

    Returns:
        str | None: Most frequent category or None if no data.
    """
    categories = []
    try:
        with open("monthly_spending.txt", "r") as file:
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


def aggregate_category_spending(month: int) -> dict[str, float]:
    """
    Aggregate spending by category for a given month.

    Args:
        month (int): Month number.

    Returns:
        dict[str, float]: Category totals.
    """
    totals = {}
    try:
        with open("monthly_spending.txt", "r") as file:
            for line in file:
                m, amount, category, _ = line.strip().split(",", 3)
                if int(m) == month:
                    totals[category] = totals.get(category, 0) + float(amount)
    except FileNotFoundError:
        return totals
    return totals


def generate_budget_report(month: int, year: int) -> None:
    """Generate a full report including totals and frequent category."""
    totals = aggregate_category_spending(month)
    total_spending = sum(totals.values())
    most_frequent = get_most_frequent_transaction_category()

    print(f"\nBudget Report {month}/{year}:")
    print(f"Total spending: ${total_spending:.2f}")
    print("Category breakdown:")
    for category, amount in totals.items():
        print(f"  {category}: ${amount:.2f}")
    if most_frequent:
        print(f"Most frequent spending category: {most_frequent}")


def format_currency(amount: float) -> str:
    """
    Format a numeric amount as US dollar currency.
    
    Args:
        amount (float): The amount to format.
        
    Returns:
        str: Formatted string, e.g., $1,234.56
    """
    return f"${amount:,.2f}"

def generate_monthly_report(income_records: list[dict], expense_records: list[dict]) -> None:
    """
    Outputs monthly totals and balances.

    Args:
        income_records (list[dict]): List of income records, each with keys 'month', 'year', 'amount'.
        expense_records (list[dict]): List of expense records, each with keys 'month', 'year', 'amount', 'category'.
    """
    # Group income by month/year
    income_by_month = {}
    for rec in income_records:
        key = (rec['month'], rec['year'])
        income_by_month[key] = income_by_month.get(key, 0) + rec['amount']

    # Group expenses by month/year
    expense_by_month = {}
    for rec in expense_records:
        key = (rec['month'], rec['year'])
        expense_by_month[key] = expense_by_month.get(key, 0) + rec['amount']

    # Generate report
    all_keys = sorted(set(income_by_month) | set(expense_by_month))
    print("\nMonthly Report:")
    for key in all_keys:
        income = income_by_month.get(key, 0)
        expenses = expense_by_month.get(key, 0)
        balance = income - expenses
        print(f"{key[0]}/{key[1]} - Income: {format_currency(income)}, "
              f"Expenses: {format_currency(expenses)}, "
              f"Balance: {format_currency(balance)}")

def predict_future_savings(income_records: list[dict], expense_records: list[dict], months: int = 6) -> float:
    """
    Estimates future savings based on average income and expenses.

    Args:
        income_records (list[dict]): List of income records.
        expense_records (list[dict]): List of expense records.
        months (int): Number of months to predict.

    Returns:
        float: Estimated total savings for the next `months`.
    """
   #Compute total income and expenses
    total_income = sum(record['amount'] for record in income_records)
    total_expenses = sum(record['amount'] for record in expense_records)

    #Determine how many unique months of data exist
    all_months = {(rec['month'], rec['year']) for rec in income_records + expense_records}
    num_months = max(len(all_months), 1)  # Avoid division by zero

    #Compute monthly averages
    avg_income = total_income / num_months
    avg_expenses = total_expenses / num_months
    avg_savings = avg_income - avg_expenses

    #Predict savings for the given number of months
    projected_savings = avg_savings * months

    print(f"\nEstimated average monthly savings: {format_currency(avg_savings)}")
    print(f"Predicted total savings over next {months} months: {format_currency(projected_savings)}")

    return projected_savings
def validate_amount(amount: float | int) -> bool:
    """
    Validate that an amount is a positive number.

    Args:
        amount (float | int): Amount to validate.

    Returns:
        bool: True if amount is positive.

    Raises:
        TypeError: If amount is not numeric.
    """
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")
    return amount >= 0

def validate_category(category: str) -> bool:
    """
    Validate that a category name is a non-empty string.

    Args:
        category (str): Category to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        TypeError: If category is not a string.
    """
    if not isinstance(category, str):
        raise TypeError("Category must be a string")
    return len(category.strip()) > 0

