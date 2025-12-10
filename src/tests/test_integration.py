import unittest
from pathlib import Path
import tempfile
import shutil
from classes.User import User
from classes.Transaction import Transaction
from classes.BudgetAnalyzer import BudgetAnalyzer

class TestIntegration(unittest.TestCase):
    """Integration tests - testing how components work together"""
    
    def setUp(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
        self.file_handler = FileHandler(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_user_save_and_load(self):
        """Test that user data can be saved and loaded correctly"""
        user = User("integration_test", "Texas", 6000)
        user.add_transaction("2024-01-15", "Grocery", 100, "Food")
        user.add_transaction("2024-01-16", "Gas", 50, "Transport")
        
        self.file_handler.save_user(user)
        loaded_user = self.file_handler.load_user("integration_test")
        
        self.assertEqual(loaded_user.username, user.username)
        self.assertEqual(loaded_user.state, user.state)
        self.assertEqual(len(loaded_user.transactions), 2)
    
    def test_import_and_analyze_workflow(self):
        """Test importing CSV and analyzing the data"""
        csv_path = Path(self.test_dir) / "test_transactions.csv"
        with open(csv_path, 'w') as f:
            f.write("date,description,amount,category\n")
            f.write("2024-01-15,Grocery Store,150.00,Food\n")
            f.write("2024-01-16,Coffee Shop,5.50,Food\n")
            f.write("2024-01-17,Gas Station,40.00,Transport\n")
        
        user = User("import_test", "Florida", 5000)
        transactions = self.file_handler.import_csv(csv_path)
        for t in transactions:
            user.add_transaction(t['date'], t['description'], t['amount'], t['category'])
        
        analyzer = BudgetAnalyzer()
        most_frequent = analyzer.get_most_frequent_category(user.transactions)
        
        self.assertEqual(most_frequent, "Food")
        self.assertEqual(len(user.transactions), 3)
    
    def test_multi_user_data_integrity(self):
        """Test that multiple users' data doesn't interfere"""
        user1 = User("user1", "California", 5000)
        user1.add_transaction("2024-01-15", "Grocery", 100, "Food")
        
        user2 = User("user2", "Texas", 6000)
        user2.add
