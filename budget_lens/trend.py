"""trend.py — Monthly spend trends and temporal aggregation engine for budget-lens."""

from __future__ import annotations
from typing import Dict, List, Any
from collections import defaultdict
from budget_lens.models import Transaction


class MonthlyTrendAnalyzer:
    """Analyzes income vs expenses over calendar months."""

    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions

    def monthly_breakdown(self) -> Dict[str, Dict[str, float]]:
        """
        Group transactions by YYYY-MM.
        Returns dict: month -> {'income': float, 'expenses': float, 'net': float}.
        """
        months: Dict[str, Dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expenses": 0.0, "net": 0.0})

        for t in self.transactions:
            month_key = t.date[:7] if len(t.date) >= 7 else "Unknown"
            if t.amount >= 0:
                months[month_key]["income"] += t.amount
            else:
                months[month_key]["expenses"] += abs(t.amount)
            months[month_key]["net"] += t.amount

        # Round values for cleanliness
        result = {}
        for m, stats in sorted(months.items()):
            result[m] = {
                "income": round(stats["income"], 2),
                "expenses": round(stats["expenses"], 2),
                "net": round(stats["net"], 2),
            }
        return result

    def render_ascii_trend(self) -> str:
        """Render ASCII summary table of monthly trends."""
        breakdown = self.monthly_breakdown()
        lines = [
            "=" * 65,
            " MONTHLY FINANCIAL TREND SUMMARY",
            "=" * 65,
            f"{'Month':<10} | {'Income':>12} | {'Expenses':>12} | {'Net Savings':>12}",
            "-" * 65,
        ]
        for m, vals in breakdown.items():
            lines.append(
                f"{m:<10} | ${vals['income']:>11.2f} | ${vals['expenses']:>11.2f} | ${vals['net']:>11.2f}"
            )
        lines.append("=" * 65)
        return "\n".join(lines)
