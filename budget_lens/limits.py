"""limits.py — Category budget limits and variance alert evaluation for budget-lens."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from budget_lens.models import Transaction


@dataclass
class BudgetAlert:
    category: str
    limit: float
    actual_spent: float
    percentage_used: float
    is_exceeded: bool


class BudgetLimitManager:
    """Configures monthly category spending caps and flags exceeded budgets."""

    def __init__(self, limits: Optional[Dict[str, float]] = None):
        self.limits: Dict[str, float] = limits or {}

    def set_limit(self, category: str, monthly_limit: float) -> None:
        self.limits[category] = monthly_limit

    def evaluate_month(self, transactions: List[Transaction], month: str) -> List[BudgetAlert]:
        """
        Evaluate actual expense spending against limits for a given month (YYYY-MM).
        """
        category_spent: Dict[str, float] = {}
        for t in transactions:
            if t.date.startswith(month) and t.amount < 0:
                cat = t.category or "Uncategorized"
                category_spent[cat] = category_spent.get(cat, 0.0) + abs(t.amount)

        alerts = []
        for cat, limit in self.limits.items():
            spent = category_spent.get(cat, 0.0)
            pct = (spent / limit * 100.0) if limit > 0 else 0.0
            alerts.append(
                BudgetAlert(
                    category=cat,
                    limit=limit,
                    actual_spent=round(spent, 2),
                    percentage_used=round(pct, 1),
                    is_exceeded=(spent > limit),
                )
            )
        return alerts
