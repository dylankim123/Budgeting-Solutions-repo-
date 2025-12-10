import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from user import User
from transaction import Transaction
from budget_analyzer import BudgetAnalyzer

class TestUser(unittest.TestCase):
    """Unit tests for User class"""
    
    def setUp(self):
        """Run before each test"""
        self.user = User("testuser", "California", 5000)
    
    def tearDown(self):
        """Run after each test - cleanup"""
        # Delete any test files created
        pass
    
    def test_user_creation(self):
        """Test that user is created with correct attributes"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.state, "California")
        self.assertEqual(self.user.monthly_income, 5000)
    
    def test_add_transaction(self):
        """Test adding a single transaction"""
        self.user.add_transaction("2024-01-15", "Grocery Store", 150.00, "Food")
        self.assertEqual(len(self.user.transactions), 1)
        self.assertEqual(self.user.transactions[0].amount, 150.00)
    
    def test_calculate_after_tax_income(self):
        """Test after-tax income calculation"""
        after_tax = self.user.calculate_after_tax_income()
        self.assertLess(after_tax, self.user.monthly_income)
        self.assertGreater(after_tax, 0)

class TestTransaction(unittest.TestCase):
    """Unit tests for Transaction class"""
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        t = Transaction("2024-01-15", "Coffee Shop", 5.50, "Food")
        self.assertEqual(t.amount, 5.50)
        self.assertEqual(t.category, "Food")
    
    def test_transaction_validation(self):
        """Test transaction amount must be positive"""
        with self.assertRaises(ValueError):
            Transaction("2024-01-15", "Invalid", -10.00, "Food")

class TestBudgetAnalyzer(unittest.TestCase):
    """Unit tests for BudgetAnalyzer class"""
    
    def test_category_breakdown_empty(self):
        """Test category breakdown with no transactions"""
        analyzer = BudgetAnalyzer()
        breakdown = analyzer.get_category_breakdown([])
        self.assertEqual(breakdown, {})
    
    def test_most_frequent_category(self):
        """Test finding most frequent category"""
        transactions = [
            Transaction("2024-01-15", "Grocery", 100, "Food"),
            Transaction("2024-01-16", "Restaurant", 50, "Food"),
            Transaction("2024-01-17", "Gas", 40, "Transport")
        ]
        analyzer = BudgetAnalyzer()
        most_frequent = analyzer.get_most_frequent_category(transactions)
        self.assertEqual(most_frequent, "Food")

if __name__ == '__main__':
    unittest.main()
