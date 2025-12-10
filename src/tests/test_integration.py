import unittest
import sys
from pathlib import Path
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from Function_Library import (
    calculate_money_available_after_tax,
    get_most_frequent_transaction_category,
    what_state
)
from file_handler import FileHandler  # NEW


class TestIntegration(unittest.TestCase):
    """Integration tests - testing functions working together"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.file_handler = FileHandler(self.test_dir)  # NEW
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load_user_profile(self):
        """Test saving and loading complete user data"""
        # Create user data
        username = "testuser"
        income = 5000
        state = "California"
        transactions = [
            {"date": "2024-01-15", "description": "Grocery", "amount": 150, "category": "Food"},
            {"date": "2024-01-16", "description": "Gas", "amount": 50, "category": "Transport"}
        ]
        
        # Save profile
        saved_path = self.file_handler.save_user_profile(username, income, state, transactions)
        self.assertTrue(saved_path.exists())
        
        # Load profile
        loaded = self.file_handler.load_user_profile(username)
        
        # Verify
        self.assertEqual(loaded['username'], username)
        self.assertEqual(loaded['income'], income)
        self.assertEqual(loaded['state'], state)
        self.assertEqual(len(loaded['transactions']), 2)
    
    def test_import_csv_and_analyze(self):
        """Test importing CSV and analyzing categories"""
        # Create test CSV
        csv_path = Path(self.test_dir) / "test.csv"
        with csv_path.open('w') as f:
            f.write("date,description,amount,category\n")
            f.write("2024-01-15,Grocery,150.00,Food\n")
            f.write("2024-01-16,Coffee,5.50,Food\n")
            f.write("2024-01-17,Gas,40.00,Transport\n")
        
        # Import
        transactions = self.file_handler.import_transactions_from_csv(csv_path)
        
        # Analyze using your existing function
        most_frequent = get_most_frequent_transaction_category(transactions)
        
        # Verify
        self.assertEqual(len(transactions), 3)
        self.assertEqual(most_frequent, "Food")
    
    def test_tax_calculation_and_report_export(self):
        """Test calculating taxes and exporting report"""
        username = "reportuser"
        state = "Texas"
        income = 5000
        
        # Calculate after-tax
        after_tax = calculate_money_available_after_tax(income, state)
        
        # Create transactions
        transactions = [
            {"date": "2024-01-15", "description": "Rent", "amount": 1200, "category": "Housing"},
            {"date": "2024-01-20", "description": "Food", "amount": 300, "category": "Food"}
        ]
        
        # Export report
        report_path = self.file_handler.export_monthly_report(
            username, 1, 2024, transactions, after_tax
        )
        
        # Verify report exists and has correct data
        self.assertTrue(report_path.exists())
        
        import json
        with report_path.open('r') as f:
            report = json.load(f)
        
        self.assertEqual(report['username'], username)
        self.assertEqual(report['total_spent'], 1500)
        self.assertGreater(report['remaining'], 0)


if __name__ == '__main__':
    unittest.main()
