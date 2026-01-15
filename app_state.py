from database import DatabaseConnection, AccountDAO, TransactionDAO, BudgetDAO

class AppState:
    def __init__(self):
        # Database connection
        self._db = DatabaseConnection()

        # DAO objects
        self.account_dao = AccountDAO(self._db)
        self.transaction_dao = TransactionDAO(self._db)
        self.budget_dao = BudgetDAO(self._db)