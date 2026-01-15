from typing import List, Optional
from model.account import Account
from model.bank_account import BankAccount
from model.wallet_account import WalletAccount
from model.savings_account import SavingsAccount
from utils.enums import AccountType, Currency
from database.db_connection import DatabaseConnection

class AccountDAO:
    
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create(self, account: Account) -> None:
        account_type = account.accountType.value if hasattr(account, "accountType") else AccountType.BANK.value
        currency = account.currency.value if hasattr(account, "currency") else Currency.USD.value

        with self.db as conn:
            conn.execute(
                """
                INSERT INTO accounts (id, name, account_type, currency)
                VALUES (?, ?, ?, ?)
                """,
                (account.id, account.name, account_type, currency),
            )

    def read(self, account_id: int) -> Optional[Account]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, name, account_type, currency
                FROM accounts
                WHERE id = ?
                """,
                (account_id,),
            )
            row = cur.fetchone()

        if row is None:
            return None
        return self._row_to_account(row)

    def read_all(self) -> List[Account]:
        with self.db as conn:
            cur = conn.execute(
                """
                SELECT id, name, account_type, currency
                FROM accounts
                ORDER BY id
                """
            )
            rows = cur.fetchall()

        return [self._row_to_account(r) for r in rows]

    def update(self, account: Account) -> None:
        account_type = account.accountType.value if hasattr(account, "accountType") else AccountType.BANK.value
        currency = account.currency.value if hasattr(account, "currency") else Currency.USD.value

        with self.db as conn:
            cur = conn.execute(
                """
                UPDATE accounts
                SET name = ?, account_type = ?, currency = ?
                WHERE id = ?
                """,
                (account.name, account_type, currency, account.id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Account with ID {account.id} not found")

    def delete(self, account_id: int) -> None:
        with self.db as conn:
            cur = conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Account with ID {account_id} not found")

    def exists(self, account_id: int) -> bool:
        with self.db as conn:
            cur = conn.execute("SELECT 1 FROM accounts WHERE id = ?", (account_id,))
            return cur.fetchone() is not None

    def _row_to_account(self, row) -> Account:
        account_id = row["id"]
        name = row["name"]
        account_type = AccountType(row["account_type"])
        currency = Currency(row["currency"])

        if account_type == AccountType.BANK:
            return BankAccount(account_id, name, currency)
        elif account_type == AccountType.WALLET:
            return WalletAccount(account_id, name, currency)
        elif account_type == AccountType.SAVINGS:
            return SavingsAccount(account_id, name, currency)
        else:
            return BankAccount(account_id, name, currency)