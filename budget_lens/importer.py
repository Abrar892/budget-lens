"""CSV parser and transaction importer."""
import csv
from typing import List
from budget_lens.models import Transaction, Categorizer


class StatementImporter:
    @staticmethod
    def import_csv(filepath: str, categorizer: Categorizer) -> List[Transaction]:
        transactions = []
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            # Find date, description, amount headers case-insensitively
            for row in reader:
                lower_keys = {k.lower(): k for k in row.keys() if k}
                date_k = lower_keys.get("date", "")
                desc_k = lower_keys.get("description", lower_keys.get("memo", lower_keys.get("name", "")))
                amt_k = lower_keys.get("amount", "")

                if not (date_k and desc_k and amt_k):
                    continue

                date_val = row[date_k].strip()
                desc_val = row[desc_k].strip()
                try:
                    amt_val = float(row[amt_k].replace("$", "").replace(",", "").strip())
                except ValueError:
                    continue

                category = categorizer.categorize(desc_val, amt_val)
                transactions.append(Transaction(date=date_val, description=desc_val, amount=amt_val, category=category))

        return transactions
