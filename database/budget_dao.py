from typing import List, Optional
from model.budget import Budget
from utils.enums import Category
from database.db_connection import DatabaseConnection

class BudgetDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create(self, budget: Budget) -> None:
        with self.db as conn:
            conn.execute(
                """
                INSERT INTO budgets (id, month, category, limit_amount)
                VALUES (?, ?, ?, ?)
                """,
                (
                    budget.id,
                    budget.month,
                    budget.category.value,
                    budget.limit_amount,
                ),
            )

    def read(self, budget_id: int) -> Optional[Budget]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, month, category, limit_amount
                FROM budgets
                WHERE id = ?
                """,
                (budget_id,),
            )
            row = cur.fetchone()

        if row is None:
            return None
        return self._row_to_budget(row)

    def read_all(self) -> List[Budget]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, month, category, limit_amount
                FROM budgets
                ORDER BY month DESC, id DESC
                """
            )
            rows = cur.fetchall()

        return [self._row_to_budget(r) for r in rows]

    def read_by_month(self, month: str) -> List[Budget]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, month, category, limit_amount
                FROM budgets
                WHERE month = ?
                ORDER BY category
                """,
                (month,),
            )
            rows = cur.fetchall()

        return [self._row_to_budget(r) for r in rows]

    def read_by_category(self, category: Category) -> List[Budget]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, month, category, limit_amount
                FROM budgets
                WHERE category = ?
                ORDER BY month DESC
                """,
                (category.value,),
            )
            rows = cur.fetchall()

        return [self._row_to_budget(r) for r in rows]

    def update(self, budget: Budget) -> None:
        with self.db as conn:
            cur = conn.execute(
                """
                UPDATE budgets
                SET month = ?, category = ?, limit_amount = ?
                WHERE id = ?
                """,
                (
                    budget.month,
                    budget.category.value,
                    budget.limit_amount,
                    budget.id,
                ),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Budget with ID {budget.id} not found")

    def delete(self, budget_id: int) -> None:
        with self.db as conn:
            cur = conn.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Budget with ID {budget_id} not found")

    def exists(self, budget_id: int) -> bool:
        with self.db as conn:
            cur = conn.execute("SELECT 1 FROM budgets WHERE id = ?", (budget_id,))
            return cur.fetchone() is not None

    def _row_to_budget(self, row) -> Budget:
        budget_id = row["id"]
        month = row["month"]
        category = Category(row["category"])
        limit_amount = row["limit_amount"]

        return Budget(budget_id, month, category, limit_amount)