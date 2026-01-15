from dataclasses import dataclass, field
from datetime import date
from utils.enums import Category, TransactionType

@dataclass
class Transaction:
    _id: int
    _account_id: int
    _date: date
    _amount: float
    _description: str = field(default="")
    _category: Category = field(default=Category.OTHER)
    _transaction_type: TransactionType = field(default=TransactionType.EXPENSE)

    @property
    def id(self) -> int:
        return self._id

    @property
    def account_id(self) -> int:
        return self._account_id

    @property
    def date(self) -> date:
        return self._date

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, value: Category) -> None:
        self._category = value

    @property
    def transaction_type(self) -> TransactionType:
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, value: TransactionType) -> None:
        self._transaction_type = value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)