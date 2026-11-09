"""SQLite financial ledger storage."""
import sqlite3
from typing import List, Dict, Optional, Tuple
from budget_lens.models import Transaction


class Ledger:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cur = self._conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_trans_date ON transactions(date)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_trans_category ON transactions(category)")
        self._conn.commit()

    def add_transaction(self, t: Transaction) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
            (t.date, t.description, t.amount, t.category)
        )
        self._conn.commit()
        return cur.lastrowid

    def list_transactions(self, limit: int = 100) -> List[Transaction]:
        cur = self._conn.cursor()
        cur.execute("SELECT id, date, description, amount, category FROM transactions ORDER BY date DESC LIMIT ?", (limit,))
        return [
            Transaction(id=r["id"], date=r["date"], description=r["description"], amount=r["amount"], category=r["category"])
            for r in cur.fetchall()
        ]

    def get_summary(self) -> Dict[str, float]:
        cur = self._conn.cursor()
        cur.execute("SELECT SUM(amount) FROM transactions WHERE amount > 0")
        income = cur.fetchone()[0] or 0.0
        cur.execute("SELECT SUM(amount) FROM transactions WHERE amount < 0")
        expenses = abs(cur.fetchone()[0] or 0.0)
        return {
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "net_savings": round(income - expenses, 2)
        }

    def get_category_breakdown(self) -> Dict[str, float]:
        cur = self._conn.cursor()
        cur.execute("SELECT category, SUM(ABS(amount)) as total FROM transactions WHERE amount < 0 GROUP BY category ORDER BY total DESC")
        return {r["category"]: round(r["total"], 2) for r in cur.fetchall()}

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
