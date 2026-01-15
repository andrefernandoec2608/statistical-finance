from typing import List, Optional
from datetime import date

from model.transaction import Transaction
from utils.enums import Category, TransactionType
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
)
from database.transaction_dao import TransactionDAO

class TransactionManager:
    def __init__(self, transaction_dao: TransactionDAO) -> None:
        self._transaction_dao = transaction_dao

    def create_transaction(
        self,
        transaction_id: int,
        account_id: int,
        trx_date: date,
        amount: float,
        description: str,
        category: Category,
        transaction_type: TransactionType,
    ) -> None:
        if self._transaction_dao.exists(transaction_id):
            raise DuplicateIDException(transaction_id)
        
        transaction = Transaction(
            transaction_id,
            account_id,
            trx_date,
            amount,
            description,
            category,
            transaction_type,
        )
        self._transaction_dao.create(transaction)

    def modify_transaction(
        self,
        transaction_id: int,
        description: str,
        category: Category,
        transaction_type: Optional[TransactionType],
    ) -> None:
        transaction = self._transaction_dao.read(transaction_id)
        if transaction is None:
            raise NotFoundIDException(transaction_id)

        transaction.description = description
        if transaction_type is not None:
            transaction.transaction_type = transaction_type
        transaction.category = category
        self._transaction_dao.update(transaction)

    def delete_transaction(self, transaction_id: int) -> None:
        try:
            self._transaction_dao.delete(transaction_id)
        except ValueError:
            raise NotFoundIDException(transaction_id)

    def get_all_transactions(self) -> List[Transaction]:
        return self._transaction_dao.read_all()

    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        transaction = self._transaction_dao.read(transaction_id)
        if transaction is None:
            raise NotFoundIDException(transaction_id)
        return transaction

    def get_filtered_transactions(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[TransactionType] = None,
    ) -> List[Transaction]:
        return self._transaction_dao.read_filtered(start_date, end_date, transaction_type)