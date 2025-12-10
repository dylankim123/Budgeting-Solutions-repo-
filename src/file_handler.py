import json
import csv
from pathlib import Path
from datetime import datetime


class FileHandler:
    """Handles all file I/O operations for BudgetBuddy"""
    
    def __init__(self, data_dir="data"):
        """Initialize with data directory path"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_user_profile(self, username, income, state, transactions=None):
        """
        Save complete user profile to JSON file
        
        Args:
            username: User's username
            income: Monthly income
            state: User's state
            transactions: List of transaction dicts (optional)
        
        Returns:
            Path to saved file
        """
        if transactions is None:
            transactions = []
        
        user_data = {
            "username": username,
            "income": income,
            "state": state,
            "transactions": transactions,
            "last_updated": datetime.now().isoformat()
        }
        
        filepath = self.data_dir / f"{username}_profile.json"
        
        try:
            with filepath.open('w') as f:
                json.dump(user_data, f, indent=2)
            return filepath
        except Exception as e:
            raise IOError(f"Failed to save user profile: {e}")
    
    def load_user_profile(self, username):
        """
        Load user profile from JSON file
        
        Args:
            username: User's username
        
        Returns:
            Dictionary with user data, or None if file doesn't exist
        """
        filepath = self.data_dir / f"{username}_profile.json"
        
        if not filepath.exists():
            return None
        
        try:
            with filepath.open('r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted user profile file: {e}")
        except Exception as e:
            raise IOError(f"Failed to load user profile: {e}")
    
    def import_transactions_from_csv(self, csv_filepath):
        """
        Import transactions from a CSV file
        
        Expected CSV format:
        date,description,amount,category
        2024-01-15,Grocery Store,150.00,Food
        
        Args:
            csv_filepath: Path to CSV file
        
        Returns:
            List of transaction dictionaries
        """
        csv_path = Path(csv_filepath)
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_filepath}")
        
        transactions = []
        
        try:
            with csv_path.open('r') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                required_headers = {'date', 'description', 'amount', 'category'}
                if not required_headers.issubset(reader.fieldnames):
                    raise ValueError(f"CSV must have headers: {required_headers}")
                
                for row in reader:
                    # Validate and convert data
                    try:
                        transaction = {
                            'date': row['date'].strip(),
                            'description': row['description'].strip(),
                            'amount': float(row['amount']),
                            'category': row['category'].strip()
                        }
                        
                        # Basic validation
                        if transaction['amount'] <= 0:
                            raise ValueError("Amount must be positive")
                        
                        transactions.append(transaction)
                    
                    except ValueError as e:
                        print(f"Warning: Skipping invalid row: {row} - {e}")
                        continue
            
            return transactions
        
        except Exception as e:
            raise IOError(f"Failed to import CSV: {e}")
    
    def export_transactions_to_csv(self, transactions, csv_filepath):
        """
        Export transactions to CSV file
        
        Args:
            transactions: List of transaction dictionaries
            csv_filepath: Path where CSV should be saved
        
        Returns:
            Path to exported file
        """
        csv_path = Path(csv_filepath)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with csv_path.open('w', newline='') as f:
                if not transactions:
                    # Write headers only
                    writer = csv.DictWriter(f, fieldnames=['date', 'description', 'amount', 'category'])
                    writer.writeheader()
                else:
                    fieldnames = transactions[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(transactions)
            
            return csv_path
        
        except Exception as e:
            raise IOError(f"Failed to export CSV: {e}")
    
    def export_monthly_report(self, username, month, year, transactions, after_tax_income):
        """
        Export a monthly spending report as JSON
        
        Args:
            username: User's username
            month: Month number (1-12)
            year: Year
            transactions: List of transactions for the month
            after_tax_income: User's after-tax income
        
        Returns:
            Path to report file
        """
        total_spent = sum(t['amount'] for t in transactions)
        remaining = after_tax_income - total_spent
        
        # Calculate category breakdown
        categories = {}
        for t in transactions:
            cat = t['category']
            categories[cat] = categories.get(cat, 0) + t['amount']
        
        report = {
            "username": username,
            "month": month,
            "year": year,
            "after_tax_income": after_tax_income,
            "total_spent": total_spent,
            "remaining": remaining,
            "category_breakdown": categories,
            "transaction_count": len(transactions),
            "generated_date": datetime.now().isoformat()
        }
        
        filename = f"{username}_report_{year}_{month:02d}.json"
        filepath = self.data_dir / "reports" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with filepath.open('w') as f:
                json.dump(report, f, indent=2)
            return filepath
        except Exception as e:
            raise IOError(f"Failed to export report: {e}")
    
    def list_users(self):
        """
        List all users with saved profiles
        
        Returns:
            List of usernames
        """
        json_files = self.data_dir.glob("*_profile.json")
        usernames = [f.stem.replace("_profile", "") for f in json_files]
        return sorted(usernames)
    
    def delete_user_profile(self, username):
        """
        Delete a user's profile file
        
        Args:
            username: User's username
        
        Returns:
            True if deleted, False if file didn't exist
        """
        filepath = self.data_dir / f"{username}_profile.json"
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
