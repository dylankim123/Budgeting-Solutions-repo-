# CSV Import Guide

## Overview
**BudgetBuddy can import transaction data from CSV files, making it easy to load bank statements or existing spending records**

## CSV File Format
- Your CSV file must have these four columns (in any order):
Date:       Description:   Amount:  Category:
2024-01-15  Grocery Store  150.00  Food
2024-01-16  Gas Station    45.00   Transport

# Supported Categories
**We recommend using these standard categories for consistency:**
Food - Groceries, restaurants, coffee shops
Housing - Rent, mortgage, property tax
Transport - Gas, public transit, ride shares, car payments
Utilities - Electric, water, internet, phone
Entertainment - Movies, concerts, subscriptions (Netflix, Spotify)
Shopping - Clothing, electronics, general retail
Health - Medical bills, pharmacy, gym membership
Insurance - Car, health, home, life insurance
Home - Furniture, repairs, home improvement
Bills - Credit cards, loans, other regular payments
Other - Miscellaneous expenses

# Sample CSV Files
We've included several sample CSV files in the examples/ folder:
1. sample_transactions.csv
   - Contains 30 transactions across 3 months
   - Covers all major expense categories
   - Good for testing multi-month analysis

2. bank_statement_january.csv
  - Single month (January 2024)
  - 13 transactions
  - Realistic bank statement format

3. test_import.csv
  - Minimal test file with 5 transactions
  - Good for quick testing
  - Used in automated tests

# How to import using python code:

from file_handler import FileHandler

- Create file handler
fh = FileHandler()

- Import transactions from CSV
transactions = fh.import_transactions_from_csv("examples/sample_transactions.csv")

- Now you can work with the transactions
print(f"Imported {len(transactions)} transactions")


# Creating Your Own CSV Files From Excel

1. Enter your data in Excel with the four required columns
2. File → Save As → CSV (Comma delimited) (*.csv)
3. Import into BudgetBuddy

# From Bank Statements
  - Most banks allow you to download transaction history as CSV:

1. Log into your online banking
2. Navigate to account history/statements
3. Select date range
4. Download as CSV
5. Important: Rename columns to match our format (date, description, amount, category)
6. You may need to manually add the category column
