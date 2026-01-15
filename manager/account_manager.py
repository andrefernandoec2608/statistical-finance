from typing import List
from model.account import Account
from model.bank_account import BankAccount
from model.savings_account import SavingsAccount
from model.wallet_account import WalletAccount
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
    FinanceManagerException,
)
from utils.enums import AccountType, Currency
from database.account_dao import AccountDAO

class AccountManager:
    def __init__(self, account_dao: AccountDAO) -> None:
        self._account_dao = account_dao

    def create_account(
        self,
        account_id: int,
        name: str,
        account_type: str,
        currency: str,
    ) -> None:
        if self._account_dao.exists(account_id):
            raise DuplicateIDException(account_id)
        
        if account_type == AccountType.BANK.value:
            account = BankAccount(account_id, name, Currency(currency))
        elif account_type == AccountType.SAVINGS.value:
            account = SavingsAccount(account_id, name, Currency(currency))
        elif account_type == AccountType.WALLET.value:
            account = WalletAccount(account_id, name, Currency(currency))
        else:
            raise FinanceManagerException(
                "Unsupported account type. Use 'CashAccount' or 'BankAccount'."
            )
        self._account_dao.create(account)

    def modify_account(self, account_id: int, name: str) -> None:
        account = self._account_dao.read(account_id)
        if account is None:
            raise NotFoundIDException(account_id)

        account.name = name
        self._account_dao.update(account)

    def delete_account(self, account_id: int) -> None:
        try:
            self._account_dao.delete(account_id)
        except ValueError:
            raise NotFoundIDException(account_id)

    def get_all_accounts(self) -> List[Account]:
        return self._account_dao.read_all()

    def get_account_by_id(self, account_id: int) -> Account:
        account = self._account_dao.read(account_id)
        if account is None:
            raise NotFoundIDException(account_id)
        return account