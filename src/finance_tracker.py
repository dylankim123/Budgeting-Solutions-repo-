import json
import os
from datetime import datetime
from collections import defaultdict

class FinanceTracker:
    def __init__(self, filename='finance_data.json'):
        self.filename = filename
        self.data = self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'income': [],
                'expenses': [],
                'budget_categories': {}
            }
    
    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def set_data_folder(self):
        """Allow user to specify a custom folder name for saving data"""
        print("\n" + "="*50)
        print("SET DATA FOLDER")
        print("="*50)
        
        current_folder = os.path.dirname(self.filename) or "current directory"
        current_file = os.path.basename(self.filename)
        
        print(f"Current location: {current_folder}")
        print(f"Current file: {current_file}")
        print("\nOptions:")
        print("1. Create a new folder for your data")
        print("2. Use existing folder")
        print("3. Cancel")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            folder_name = input("\nEnter folder name (e.g., '2024_finances' or 'personal_budget'): ").strip()
            if not folder_name:
                print("✗ No folder name provided. Cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Create the folder if it doesn't exist
            try:
                os.makedirs(folder_name, exist_ok=True)
                new_filename = os.path.join(folder_name, 'finance_data.json')
                
                # Ask if they want to move existing data
                if os.path.exists(self.filename):
                    move_data = input(f"\nMove existing data to new folder? (yes/no): ").strip().lower()
                    if move_data == 'yes':
                        # Save current data to new location
                        old_filename = self.filename
                        self.filename = new_filename
                        self.save_data()
                        print(f"✓ Data moved to: {new_filename}")
                    else:
                        # Start fresh in new folder
                        self.filename = new_filename
                        print(f"✓ New data file created at: {new_filename}")
                else:
                    self.filename = new_filename
                    self.save_data()
                    print(f"✓ Data folder created: {new_filename}")
                
            except Exception as e:
                print(f"✗ Error creating folder: {e}")
        
        elif choice == '2':
            folder_path = input("\nEnter folder path: ").strip()
            if not folder_path:
                print("✗ No folder path provided. Cancelled.")
                input("\nPress Enter to continue...")
                return
            
            if os.path.isdir(folder_path):
                new_filename = os.path.join(folder_path, 'finance_data.json')
                
                # Ask if they want to move existing data
                if os.path.exists(self.filename):
                    move_data = input(f"\nMove existing data to this folder? (yes/no): ").strip().lower()
                    if move_data == 'yes':
                        old_filename = self.filename
                        self.filename = new_filename
                        self.save_data()
                        print(f"✓ Data moved to: {new_filename}")
                    else:
                        self.filename = new_filename
                        print(f"✓ Using folder: {new_filename}")
                else:
                    self.filename = new_filename
                    self.save_data()
                    print(f"✓ Data will be saved to: {new_filename}")
            else:
                print(f"✗ Folder '{folder_path}' does not exist.")
        
        else:
            print("✓ Cancelled.")
        
        input("\nPress Enter to continue...")
    
    def clear_all_data(self):
        """Reset all financial data to start fresh"""
        print("\n⚠️  WARNING: This will delete ALL your financial data!")
        print("This includes:")
        print("  • All income entries")
        print("  • All expense entries")
        print("  • All budget categories")
        
        confirmation = input("\nType 'YES' to confirm deletion (or anything else to cancel): ").strip()
        
        if confirmation == 'YES':
            self.data = {
                'income': [],
                'expenses': [],
                'budget_categories': {}
            }
            self.save_data()
            print("\n✓ All data has been cleared. Starting fresh!")
        else:
            print("\n✓ Deletion cancelled. Your data is safe.")
    
    def add_income(self, amount, source, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.data['income'].append({
            'amount': amount,
            'source': source,
            'date': date
        })
        self.save_data()
        print(f"✓ Income added: ${amount} from {source}")
    
    def add_expense(self, amount, category, description, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.data['expenses'].append({
            'amount': amount,
            'category': category,
            'description': description,
            'date': date
        })
        self.save_data()
        print(f"✓ Expense added: ${amount} for {description} ({category})")
    
    def get_monthly_income(self, month=None, year=None):
        if month is None or year is None:
            now = datetime.now()
            month = now.month
            year = now.year
        
        total = 0
        for income in self.data['income']:
            date = datetime.strptime(income['date'], '%Y-%m-%d')
            if date.month == month and date.year == year:
                total += income['amount']
        
        return total
    
    def get_monthly_expenses(self, month=None, year=None):
        if month is None or year is None:
            now = datetime.now()
            month = now.month
            year = now.year
        
        total = 0
        category_breakdown = defaultdict(float)
        
        for expense in self.data['expenses']:
            date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if date.month == month and date.year == year:
                total += expense['amount']
                category_breakdown[expense['category']] += expense['amount']
        
        return total, dict(category_breakdown)
    
    def suggest_budget(self):
        income = self.get_monthly_income()
        
        if income == 0:
            print("No income data available. Please add your income first.")
            return
        
        # 50/30/20 rule: 50% needs, 30% wants, 20% savings
        needs = income * 0.50
        wants = income * 0.30
        savings = income * 0.20
        
        print(f"\n{'='*50}")
        print(f"BUDGET RECOMMENDATION (50/30/20 Rule)")
        print(f"{'='*50}")
        print(f"Monthly Income: ${income:,.2f}")
        print(f"\nRecommended Budget Allocation:")
        print(f"  • Needs (50%):     ${needs:,.2f}")
        print(f"    Housing, utilities, groceries, transportation")
        print(f"  • Wants (30%):     ${wants:,.2f}")
        print(f"    Entertainment, dining out, hobbies")
        print(f"  • Savings (20%):   ${savings:,.2f}")
        print(f"    Emergency fund, investments, debt repayment")
        print(f"{'='*50}\n")
        
        # Detailed category suggestions
        categories = {
            'Housing': needs * 0.60,
            'Utilities': needs * 0.10,
            'Groceries': needs * 0.20,
            'Transportation': needs * 0.10,
            'Entertainment': wants * 0.40,
            'Dining Out': wants * 0.30,
            'Shopping': wants * 0.30,
            'Savings': savings
        }
        
        self.data['budget_categories'] = categories
        self.save_data()
        
        print("Detailed Category Breakdown:")
        for category, amount in categories.items():
            print(f"  {category:.<20} ${amount:>8,.2f}")
        
        input("\nPress Enter to continue...")
        return categories
    
    def show_summary(self):
        now = datetime.now()
        income = self.get_monthly_income()
        expenses, breakdown = self.get_monthly_expenses()
        remaining = income - expenses
        
        print(f"\n{'='*50}")
        print(f"FINANCIAL SUMMARY - {now.strftime('%B %Y')}")
        print(f"{'='*50}")
        print(f"Monthly Income:       ${income:>12,.2f}")
        print(f"Total Expenses:       ${expenses:>12,.2f}")
        print(f"{'─'*50}")
        print(f"Remaining Balance:    ${remaining:>12,.2f}")
        print(f"{'='*50}\n")
        
        if breakdown:
            print("Expenses by Category:")
            for category, amount in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / expenses * 100) if expenses > 0 else 0
                print(f"  {category:.<20} ${amount:>8,.2f} ({percentage:>5.1f}%)")
            print()
        
        # Budget comparison if available
        if self.data['budget_categories']:
            print("Budget vs Actual Spending:")
            for category, budgeted in self.data['budget_categories'].items():
                if category == 'Savings':
                    continue
                spent = breakdown.get(category, 0)
                diff = budgeted - spent
                status = "✓" if diff >= 0 else "✗"
                print(f"  {status} {category:.<18} Budget: ${budgeted:>8,.2f} | Spent: ${spent:>8,.2f} | Diff: ${diff:>8,.2f}")
            print()
        
        input("\nPress Enter to continue...")

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n" + "="*50)
        print("PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Monthly Income")
        print("4. View Monthly Expenses")
        print("5. Suggest Budget for My Lifestyle")
        print("6. View Complete Summary")
        print("7. Set Data Folder")
        print("8. Clear All Data")
        print("9. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            try:
                amount = float(input("Enter income amount: $"))
                source = input("Enter income source (e.g., Salary, Freelance): ")
                tracker.add_income(amount, source)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == '2':
            try:
                amount = float(input("Enter expense amount: $"))
                category = input("Enter category (e.g., Housing, Groceries, Entertainment): ")
                description = input("Enter description: ")
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == '3':
            income = tracker.get_monthly_income()
            month = datetime.now().strftime('%B %Y')
            print(f"\nYour monthly income for {month}: ${income:,.2f}")
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            expenses, breakdown = tracker.get_monthly_expenses()
            month = datetime.now().strftime('%B %Y')
            print(f"\nYour total expenses for {month}: ${expenses:,.2f}")
            if breakdown:
                print("\nBreakdown by category:")
                for category, amount in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {category}: ${amount:,.2f}")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            tracker.suggest_budget()
        
        elif choice == '6':
            tracker.show_summary()
        
        elif choice == '7':
            tracker.set_data_folder()
        
        elif choice == '8':
            tracker.clear_all_data()
        
        elif choice == '9':
            print("\nThank you for using Personal Finance Tracker!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
