from abc import abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass(eq=False)
class Account:
    _id: int
    _name: str

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
    
    @abstractmethod
    def transform_to_csv(self) -> List[str]:
        pass