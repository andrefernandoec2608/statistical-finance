from dataclasses import dataclass, field
from typing import List

from model.account import Account
from utils.enums import AccountType, Currency

@dataclass(eq=False)
class BankAccount(Account):
    _accountType: AccountType = field(init=False, default=AccountType.BANK)
    _currency: Currency

    def __init__(self, id: int, name: str, currency: Currency):
        super().__init__(id, name)
        self._currency = currency

    @property
    def accountType(self) -> AccountType:
        return self._accountType

    @property
    def currency(self) -> Currency:
        return self._currency

    def __str__(self) -> str:
        return (
            f"BankAccount(id={self.id}, "
            f"name='{self.name}', "
            f"accountType={self.accountType.value}, "
            f"currency={self.currency.value})"
        )

    def transform_to_csv(self) -> List[str]:
        return [
            str(self.id),
            self.name,
            self.accountType.value,
            self.currency.value,
        ]