from typing import List, Optional
from datetime import date
from model.transaction import Transaction
from utils.enums import Category, TransactionType
from database.db_connection import DatabaseConnection

class TransactionDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create(self, transaction: Transaction) -> None:
        with self.db as conn:
            conn.execute(
                """
                INSERT INTO transactions (id, account_id, date, amount, description, category, transaction_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.id,
                    transaction.account_id,
                    transaction.date.isoformat(),
                    transaction.amount,
                    transaction.description,
                    transaction.category.value,
                    transaction.transaction_type.value,
                ),
            )

    def read(self, transaction_id: int) -> Optional[Transaction]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, account_id, date, amount, description, category, transaction_type
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            )
            row = cur.fetchone()

        if row is None:
            return None
        return self._row_to_transaction(row)

    def read_all(self) -> List[Transaction]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, account_id, date, amount, description, category, transaction_type
                FROM transactions
                ORDER BY date DESC, id DESC
                """
            )
            rows = cur.fetchall()
        return [self._row_to_transaction(r) for r in rows]

    def read_by_account(self, account_id: int) -> List[Transaction]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, account_id, date, amount, description, category, transaction_type
                FROM transactions
                WHERE account_id = ?
                ORDER BY date DESC, id DESC
                """,
                (account_id,),
            )
            rows = cur.fetchall()
        return [self._row_to_transaction(r) for r in rows]

    def read_filtered(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[TransactionType] = None,
    ) -> List[Transaction]:
        with self.db as conn:
            query = """
                SELECT id, account_id, date, amount, description, category, transaction_type
                FROM transactions
                WHERE 1=1
            """
            params = []
            
            if start_date is not None:
                query += " AND date >= ?"
                params.append(start_date.isoformat())
            
            if end_date is not None:
                query += " AND date <= ?"
                params.append(end_date.isoformat())
            
            if transaction_type is not None:
                query += " AND transaction_type = ?"
                params.append(transaction_type.value)
            
            query += " ORDER BY date DESC, id DESC"
            
            cur = conn.execute(query, tuple(params))
            rows = cur.fetchall()
        return [self._row_to_transaction(r) for r in rows]

    def update(self, transaction: Transaction) -> None:
        with self.db as conn:
            cur = conn.execute(
                """
                UPDATE transactions
                SET account_id = ?, date = ?, amount = ?, description = ?, category = ?, transaction_type = ?
                WHERE id = ?
                """,
                (
                    transaction.account_id,
                    transaction.date.isoformat(),
                    transaction.amount,
                    transaction.description,
                    transaction.category.value,
                    transaction.transaction_type.value,
                    transaction.id,
                ),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Transaction with ID {transaction.id} not found")

    def delete(self, transaction_id: int) -> None:
        with self.db as conn:
            cur = conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Transaction with ID {transaction_id} not found")

    def exists(self, transaction_id: int) -> bool:
        with self.db as conn:
            cur = conn.execute("SELECT 1 FROM transactions WHERE id = ?", (transaction_id,))
            return cur.fetchone() is not None

    def _row_to_transaction(self, row) -> Transaction:
        transaction_id = row["id"]
        account_id = row["account_id"]
        trx_date = date.fromisoformat(row["date"])
        amount = row["amount"]
        description = row["description"] or ""
        category = Category(row["category"])
        transaction_type = TransactionType(row["transaction_type"])

        return Transaction(
            transaction_id,
            account_id,
            trx_date,
            amount,
            description,
            category,
            transaction_type,
        )