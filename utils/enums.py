from enum import Enum

class Category(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    UTILITIES = "Utilities"
    OTHER = "Other"

class AccountType(Enum):
    BANK = "Bank"
    SAVINGS = "Savings"
    WALLET = "Wallet"

class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"