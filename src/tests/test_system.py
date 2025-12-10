import unittest
import sys
from pathlib import Path
import tempfile
import shutil
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from user import User
from budget_analyzer import BudgetAnalyzer

class TestSystem(unittest.TestCase):
    """System tests - complete end-to-end workflows"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.file_handler = FileHandler(self.test_dir)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
    
    def test_complete_monthly_budget_workflow(self):
        """
        Test the complete workflow:
        1. Create new user
        2. Set income
        3. Add expenses
        4. Calculate budget
        5. Save data
        6. Generate report
        """
        # Step 1-2: Create user
        user = User("monthly_user", "Texas", 5000)
        
        # Step 3: Add monthly expenses
        expenses = [
            ("2024-01-05", "Rent", 1200, "Housing"),
            ("2024-01-10", "Groceries", 300, "Food"),
            ("2024-01-12", "Electric Bill", 100, "Utilities"),
            ("2024-01-15", "Gas", 150, "Transport"),
            ("2024-01-20", "Restaurant", 75, "Food"),
            ("2024-01-25", "Movie", 30, "Entertainment")
        ]
        
        for date, desc, amount, cat in expenses:
            user.add_transaction(date, desc, amount, cat)
        
        # Step 4: Calculate budget
        after_tax = user.calculate_after_tax_income()
        total_spent = sum(t.amount for t in user.transactions)
        remaining = after_tax - total_spent
        
        # Step 5: Save data
        self.file_handler.save_user(user)
        
        # Step 6: Generate report
        analyzer = BudgetAnalyzer()
        report = analyzer.generate_monthly_report(user)
        
        # Verify complete workflow
        self.assertEqual(len(user.transactions), 6)
        self.assertGreater(after_tax, 0)
        self.assertGreater(remaining, 0)
        self.assertIn("Housing", report['categories'])
        
        # Verify data was saved
        loaded = self.file_handler.load_user("monthly_user")
        self.assertIsNotNone(loaded)
        self.assertEqual(len(loaded.transactions), 6)
    
    def test_multi_month_tracking_and_trends(self):
        """
        Test tracking across multiple months:
        1. Add transactions for 3 months
        2. Analyze spending trends
        3. Export summary
        """
        user = User("trend_user", "California", 6000)
        
        # January spending
        user.add_transaction("2024-01-15", "Grocery", 400, "Food")
        user.add_transaction("2024-01-20", "Rent", 1500, "Housing")
        
        # February spending (increased food)
        user.add_transaction("2024-02-15", "Grocery", 500, "Food")
        user.add_transaction("2024-02-20", "Rent", 1500, "Housing")
        
        # March spending (decreased food)
        user.add_transaction("2024-03-15", "Grocery", 350, "Food")
        user.add_transaction("2024-03-20", "Rent", 1500, "Housing")
        
        # Analyze trends
        analyzer = BudgetAnalyzer()
        trends = analyzer.analyze_spending_trends(user.transactions)
        
        # Export summary
        export_path = Path(self.test_dir) / "trend_summary.json"
        analyzer.export_summary(trends, export_path)
        
        # Verify
        self.assertEqual(len(user.transactions), 6)
        self.assertIn("Food", trends)
        self.assertTrue(export_path.exists())
    
    def test_data_persistence_across_sessions(self):
        """
        Test that data persists across multiple program sessions:
        Session 1: Create user and add data
        Session 2: Load user, verify data, add more
        Session 3: Load again and verify all data
        """
        # Session 1: Initial setup
        user = User("persistent_user", "Florida", 5500)
        user.add_transaction("2024-01-15", "Initial Purchase", 100, "Shopping")
        self.file_handler.save_user(user)
        del user  # Simulate ending session
        
        # Session 2: Load and add more
        loaded_user = self.file_handler.load_user("persistent_user")
        self.assertIsNotNone(loaded_user)
        self.assertEqual(len(loaded_user.transactions), 1)
        
        loaded_user.add_transaction("2024-01-20", "Second Purchase", 50, "Food")
        self.file_handler.save_user(loaded_user)
        del loaded_user  # Simulate ending session
        
        # Session 3: Load and verify all data
        final_user = self.file_handler.load_user("persistent_user")
        self.assertEqual(len(final_user.transactions), 2)
        self.assertEqual(final_user.transactions[0].amount, 100)
        self.assertEqual(final_user.transactions[1].amount, 50)
    
    def test_csv_import_to_analysis_to_export(self):
        """
        Complete workflow with CSV:
        1. Import bank statement CSV
        2. Categorize transactions
        3. Analyze spending
        4. Export categorized report
        """
        # Create sample bank statement CSV
        csv_path = Path(self.test_dir) / "bank_statement.csv"
        with open(csv_path, 'w') as f:
            f.write("date,description,amount,category\n")
            f.write("2024-01-05,Walmart,125.50,Food\n")
            f.write("2024-01-07,Shell Gas,45.00,Transport\n")
            f.write("2024-01-10,Netflix,15.99,Entertainment\n")
            f.write("2024-01-12,Starbucks,8.50,Food\n")
        
        # Import to user
        user = User("csv_user", "Texas", 4000)
        imported = self.file_handler.import_csv(csv_path)
        for t in imported:
            user.add_transaction(t['date'], t['description'], 
                               t['amount'], t['category'])
        
        # Analyze
        analyzer = BudgetAnalyzer()
        category_breakdown = analyzer.get_category_breakdown(user.transactions)
        
        # Export categorized report
        report_path = Path(self.test_dir) / "spending_report.csv"
        self.file_handler.export_category_report(category_breakdown, report_path)
        
        # Verify complete workflow
        self.assertEqual(len(user.transactions), 4)
        self.assertIn("Food", category_breakdown)
        self.assertTrue(report_path.exists())
        
        # Verify Food category has highest spending
        self.assertGreater(category_breakdown["Food"], 
                          category_breakdown["Transport"])
    
    def test_error_recovery_missing_file(self):
        """
        Test system handles missing files gracefully:
        1. Try to load non-existent user
        2. Try to import non-existent CSV
        3. Verify appropriate error handling
        """
        # Try to load user that doesn't exist
        user = self.file_handler.load_user("nonexistent_user")
        self.assertIsNone(user)
        
        # Try to import non-existent file
        with self.assertRaises(FileNotFoundError):
            self.file_handler.import_csv("nonexistent.csv")

if __name__ == '__main__':
    unittest.main()
