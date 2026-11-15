"""Tests for budget_lens trend analysis and budget limit evaluation."""

import unittest
from budget_lens.models import Transaction
from budget_lens.trend import MonthlyTrendAnalyzer
from budget_lens.limits import BudgetLimitManager, BudgetAlert


class TestTrendAndLimits(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            Transaction(date="2026-11-01", description="Monthly Salary", amount=5000.0, category="Income & Salary"),
            Transaction(date="2026-11-03", description="Supermarket Groceries", amount=-150.0, category="Groceries & Food"),
            Transaction(date="2026-11-10", description="Restaurant Dinner", amount=-60.0, category="Groceries & Food"),
            Transaction(date="2026-11-05", description="Electric Utility", amount=-80.0, category="Utilities & Bills"),
            Transaction(date="2026-10-15", description="October Grocery", amount=-120.0, category="Groceries & Food"),
        ]

    def test_monthly_trend_breakdown(self):
        analyzer = MonthlyTrendAnalyzer(self.transactions)
        breakdown = analyzer.monthly_breakdown()
        
        self.assertIn("2026-11", breakdown)
        self.assertIn("2026-10", breakdown)
        
        nov = breakdown["2026-11"]
        self.assertEqual(nov["income"], 5000.0)
        self.assertEqual(nov["expenses"], 290.0) # 150 + 60 + 80
        self.assertEqual(nov["net"], 4710.0)
        
        ascii_table = analyzer.render_ascii_trend()
        self.assertIn("MONTHLY FINANCIAL TREND SUMMARY", ascii_table)
        self.assertIn("2026-11", ascii_table)

    def test_budget_limit_manager(self):
        manager = BudgetLimitManager({"Groceries & Food": 200.0, "Utilities & Bills": 100.0})
        alerts = manager.evaluate_month(self.transactions, "2026-11")
        
        alerts_by_cat = {a.category: a for a in alerts}
        self.assertIn("Groceries & Food", alerts_by_cat)
        self.assertIn("Utilities & Bills", alerts_by_cat)
        
        # Groceries: 150 + 60 = 210 > 200 (exceeded)
        g_alert = alerts_by_cat["Groceries & Food"]
        self.assertEqual(g_alert.actual_spent, 210.0)
        self.assertTrue(g_alert.is_exceeded)
        self.assertEqual(g_alert.percentage_used, 105.0)

        # Utilities: 80 <= 100 (not exceeded)
        u_alert = alerts_by_cat["Utilities & Bills"]
        self.assertEqual(u_alert.actual_spent, 80.0)
        self.assertFalse(u_alert.is_exceeded)


if __name__ == "__main__":
    unittest.main()
