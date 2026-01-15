from dataclasses import dataclass
from utils.enums import Category

@dataclass(eq=False)
class Budget:
    _id: int
    _month: str
    _category: Category
    _limit_amount: float

    @property
    def id(self) -> int:
        return self._id

    @property
    def month(self) -> str:
        return self._month

    @property
    def category(self) -> Category:
        return self._category

    @property
    def limit_amount(self) -> float:
        return self._limit_amount

    @limit_amount.setter
    def limit_amount(self, value: float) -> None:
        self._limit_amount = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Budget):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)