"""Full automated test suite for budget-lens."""
import unittest
import tempfile
import os
import csv
from budget_lens.models import Categorizer, Transaction
from budget_lens.ledger import Ledger
from budget_lens.importer import StatementImporter
from budget_lens.reporter import generate_html_report


class TestBudgetLens(unittest.TestCase):
    def test_auto_categorization(self):
        cat = Categorizer()
        self.assertEqual(cat.categorize("WALMART SUPERCENTER", -85.20), "Groceries & Food")
        self.assertEqual(cat.categorize("GITHUB COPILOT SUB", -10.00), "Software & Tech")
        self.assertEqual(cat.categorize("MONTHLY SALARY TRANSFER", 4500.00), "Income & Salary")
        self.assertEqual(cat.categorize("UNKNOWN STORE", -15.00), "Miscellaneous")

    def test_ledger_and_summaries(self):
        ledger = Ledger(":memory:")
        ledger.add_transaction(Transaction(date="2026-11-01", description="Salary", amount=3000.0, category="Income & Salary"))
        ledger.add_transaction(Transaction(date="2026-11-02", description="Groceries", amount=-150.0, category="Groceries & Food"))
        ledger.add_transaction(Transaction(date="2026-11-03", description="Server bill", amount=-50.0, category="Software & Tech"))

        summary = ledger.get_summary()
        self.assertEqual(summary["income"], 3000.0)
        self.assertEqual(summary["expenses"], 200.0)
        self.assertEqual(summary["net_savings"], 2800.0)

        breakdown = ledger.get_category_breakdown()
        self.assertEqual(breakdown["Groceries & Food"], 150.0)
        self.assertEqual(breakdown["Software & Tech"], 50.0)
        ledger.close()

    def test_csv_importer_and_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "statement.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Date", "Description", "Amount"])
                writer.writeheader()
                writer.writerow({"Date": "2026-11-05", "Description": "Electric Utility Co", "Amount": "-120.00"})
                writer.writerow({"Date": "2026-11-06", "Description": "Client Deposit", "Amount": "500.00"})

            cat = Categorizer()
            items = StatementImporter.import_csv(csv_path, cat)
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0].category, "Utilities & Bills")

            ledger = Ledger(":memory:")
            for it in items:
                ledger.add_transaction(it)

            html = generate_html_report(ledger.get_summary(), ledger.get_category_breakdown(), ledger.list_transactions())
            self.assertIn("Budget-Lens Financial Health", html)
            self.assertIn("Electric Utility Co", html)
            ledger.close()


if __name__ == "__main__":
    unittest.main()
