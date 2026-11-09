"""Transaction models and auto-categorization heuristics."""
import re
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Transaction:
    id: Optional[int] = None
    date: str = ""           # YYYY-MM-DD
    description: str = ""
    amount: float = 0.0      # negative for expenses, positive for income
    category: str = "Uncategorized"


DEFAULT_RULES: Dict[str, List[str]] = {
    "Groceries & Food": ["supermarket", "walmart", "grocery", "food", "restaurant", "cafe", "uber eats"],
    "Utilities & Bills": ["electric", "water", "internet", "telecom", "utility", "gas", "bill"],
    "Software & Tech": ["github", "aws", "google", "cloud", "digitalocean", "apple", "subscription"],
    "Transportation": ["uber", "lyft", "fuel", "gas station", "metro", "transit", "parking"],
    "Housing & Rent": ["rent", "mortgage", "property", "hoa"],
    "Income & Salary": ["salary", "payroll", "dividend", "interest", "deposit", "transfer in"],
}


class Categorizer:
    def __init__(self, rules: Optional[Dict[str, List[str]]] = None):
        self.rules = rules or DEFAULT_RULES

    def categorize(self, description: str, amount: float) -> str:
        desc_lower = description.lower()
        if amount > 0 and any(k in desc_lower for k in ("salary", "payroll", "deposit")):
            return "Income & Salary"

        for category, keywords in self.rules.items():
            for kw in keywords:
                if re.search(r"\b" + re.escape(kw) + r"\b", desc_lower):
                    return category
        return "Miscellaneous"
