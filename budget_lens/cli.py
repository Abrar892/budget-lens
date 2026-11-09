"""CLI entry point for budget-lens."""
import argparse
from budget_lens.models import Categorizer, Transaction
from budget_lens.ledger import Ledger
from budget_lens.importer import StatementImporter
from budget_lens.reporter import generate_html_report


def main():
    parser = argparse.ArgumentParser(description="Budget-Lens - Personal Finance Tracker and Analyzer")
    parser.add_argument("--db", default="budget.db", help="Path to SQLite ledger file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # import-csv
    imp_p = subparsers.add_parser("import-csv")
    imp_p.add_argument("file", help="Path to CSV statement")

    # summary
    subparsers.add_parser("summary")

    # report
    rep_p = subparsers.add_parser("report")
    rep_p.add_argument("--html", required=True, help="Path to write standalone HTML report")

    args = parser.parse_args()
    ledger = Ledger(args.db)

    try:
        if args.command == "import-csv":
            cat = Categorizer()
            items = StatementImporter.import_csv(args.file, cat)
            for it in items:
                ledger.add_transaction(it)
            print(f"Successfully imported {len(items)} transactions into {args.db}")

        elif args.command == "summary":
            sum_data = ledger.get_summary()
            breakdown = ledger.get_category_breakdown()
            print("Financial Summary:")
            print(f"  Income:      ${sum_data['income']:,.2f}")
            print(f"  Expenses:    ${sum_data['expenses']:,.2f}")
            print(f"  Net Savings: ${sum_data['net_savings']:,.2f}")
            print("\nExpense Breakdown:")
            for c, amt in breakdown.items():
                print(f"  - {c:<22}: ${amt:,.2f}")

        elif args.command == "report":
            sum_data = ledger.get_summary()
            breakdown = ledger.get_category_breakdown()
            recent = ledger.list_transactions(limit=30)
            html = generate_html_report(sum_data, breakdown, recent)
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Financial report written to {args.html}")

    finally:
        ledger.close()


if __name__ == "__main__":
    main()
