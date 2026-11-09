# Budget-Lens

Personal finance tracker, CSV bank transaction categorizer, budget tracker, and financial report engine with zero external dependencies.

## Key Features
- **CSV Transaction Ingest:** Ingests varied bank export formats (dates, descriptions, debit/credit amounts).
- **Rule-Based Auto-Categorization:** Maps keywords and merchant patterns to budget buckets (Food, Utilities, Software, Rent, Health).
- **SQLite Ledger:** Stores transactions with indices, balance tracking, and category aggregation.
- **Spending Trend Visualizer:** Produces standalone HTML visual reports with category breakdowns and expense proportions.
- **Zero Third-Party Dependencies:** Pure Python 3.12 standard library (`sqlite3`, `csv`, `json`, `datetime`).

## Usage
```bash
python -m budget_lens.cli import-csv statement.csv --db finance.db
python -m budget_lens.cli summary --db finance.db
python -m budget_lens.cli report --db finance.db --html monthly-report.html
```
