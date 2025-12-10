import unittest
from budget import calculate_money_available_after_tax, what_state

class TestBudgetFunctions(unittest.TestCase):
    def test_calculate_tax(self):
        """Test tax calculation for known values"""
        result = calculate_money_available_after_tax(50000, "California")
        self.assertAlmostEqual(result, 41234.50, places=2)
    
    def test_invalid_state(self):
        """Test handling of invalid state"""
        result = what_state("InvalidState")
        self.assertFalse(result)
    
    def test_username_creation(self):
        """Test username validation"""
        # Test valid username
        # Test duplicate username
        # Test empty username