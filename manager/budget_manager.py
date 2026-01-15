from typing import List

from model.budget import Budget
from utils.enums import Category
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
)
from database.budget_dao import BudgetDAO

class BudgetManager:
    def __init__(self, budget_dao: BudgetDAO) -> None:
        self._budget_dao = budget_dao

    def create_budget(
        self,
        budget_id: int,
        month: str,
        category: Category,
        limit_amount: float,
    ) -> None:
        if self._budget_dao.exists(budget_id):
            raise DuplicateIDException(budget_id)
        
        budget = Budget(budget_id, month, category, limit_amount)
        self._budget_dao.create(budget)

    def modify_budget(
        self,
        budget_id: int,
        limit_amount: float,
    ) -> None:
        budget = self._budget_dao.read(budget_id)
        if budget is None:
            raise NotFoundIDException(budget_id)

        budget.limit_amount = limit_amount
        self._budget_dao.update(budget)

    def delete_budget(self, budget_id: int) -> None:
        try:
            self._budget_dao.delete(budget_id)
        except ValueError:
            raise NotFoundIDException(budget_id)

    def get_all_budgets(self) -> List[Budget]:
        return self._budget_dao.read_all()

    def get_budget_by_id(self, budget_id: int) -> Budget:
        budget = self._budget_dao.read(budget_id)
        if budget is None:
            raise NotFoundIDException(budget_id)
        return budget