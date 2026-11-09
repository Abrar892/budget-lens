"""HTML and text reporting generator for budget-lens."""
from typing import Dict, List
from budget_lens.models import Transaction


def generate_html_report(summary: Dict[str, float], breakdown: Dict[str, float], recent: List[Transaction]) -> str:
    total_exp = max(1.0, summary.get("expenses", 1.0))
    cat_bars = []
    for cat, total in breakdown.items():
        pct = (total / total_exp) * 100
        cat_bars.append(f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:4px;">
                <span><strong>{cat}</strong></span>
                <span>${total:,.2f} ({pct:.1f}%)</span>
            </div>
            <div style="background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                <div style="background:#38bdf8;width:{pct:.1f}%;height:100%;"></div>
            </div>
        </div>
        """)

    table_rows = []
    for t in recent:
        color = "#34d399" if t.amount > 0 else "#f87171"
        amt_str = f"+${t.amount:,.2f}" if t.amount > 0 else f"-${abs(t.amount):,.2f}"
        table_rows.append(f"""
        <tr>
            <td>{t.date}</td>
            <td>{t.description}</td>
            <td><span style="background:#1e293b;padding:2px 8px;border-radius:4px;font-size:12px;">{t.category}</span></td>
            <td style="color:{color};font-weight:bold;text-align:right;">{amt_str}</td>
        </tr>
        """)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Budget-Lens Financial Health</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #0b0f19; color: #f8fafc; padding: 24px; }}
        h1 {{ color: #38bdf8; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }}
        .stat-card {{ background: #111827; border: 1px solid #1f2937; padding: 18px; border-radius: 8px; text-align: center; }}
        .stat-val {{ font-size: 24px; font-weight: bold; margin-top: 6px; }}
        .card {{ background: #111827; border: 1px solid #1f2937; padding: 20px; border-radius: 8px; margin-bottom: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #1f2937; text-align: left; font-size: 14px; }}
        th {{ background: #030712; color: #9ca3af; }}
    </style>
</head>
<body>
    <h1>Budget-Lens Financial Health Report</h1>
    <div class="grid">
        <div class="stat-card">
            <div style="color:#9ca3af;">Total Income</div>
            <div class="stat-val" style="color:#34d399;">${summary['income']:,.2f}</div>
        </div>
        <div class="stat-card">
            <div style="color:#9ca3af;">Total Expenses</div>
            <div class="stat-val" style="color:#f87171;">${summary['expenses']:,.2f}</div>
        </div>
        <div class="stat-card">
            <div style="color:#9ca3af;">Net Savings</div>
            <div class="stat-val" style="color:#38bdf8;">${summary['net_savings']:,.2f}</div>
        </div>
    </div>

    <div class="card">
        <h2>Expense Category Breakdown</h2>
        {''.join(cat_bars)}
    </div>

    <div class="card">
        <h2>Recent Transactions</h2>
        <table>
            <thead><tr><th>Date</th><th>Description</th><th>Category</th><th style="text-align:right;">Amount</th></tr></thead>
            <tbody>{''.join(table_rows)}</tbody>
        </table>
    </div>
</body>
</html>"""
