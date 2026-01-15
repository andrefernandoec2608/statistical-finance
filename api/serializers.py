from typing import Dict, Any
from datetime import date
from model.account import Account
from model.transaction import Transaction
from model.budget import Budget

def account_to_dict(account: Account) -> Dict[str, Any]:
    """Convert an Account object to a dictionary for JSON serialization."""
    result = {
        'id': account.id,
        'name': account.name,
    }
    
    # Add account type and currency if available
    if hasattr(account, 'accountType'):
        result['account_type'] = account.accountType.value
    
    if hasattr(account, 'currency'):
        result['currency'] = account.currency.value
    
    return result

def transaction_to_dict(transaction: Transaction) -> Dict[str, Any]:
    """Convert a Transaction object to a dictionary for JSON serialization."""
    return {
        'id': transaction.id,
        'account_id': transaction.account_id,
        'date': transaction.date.isoformat(),
        'amount': transaction.amount,
        'description': transaction.description,
        'category': transaction.category.value,
        'transaction_type': transaction.transaction_type.value,
    }

def budget_to_dict(budget: Budget) -> Dict[str, Any]:
    """Convert a Budget object to a dictionary for JSON serialization."""
    return {
        'id': budget.id,
        'month': budget.month,
        'category': budget.category.value,
        'limit_amount': budget.limit_amount,
    }

def dict_to_account_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert dictionary data to account creation parameters."""
    return {
        'account_id': data['id'],
        'name': data['name'],
        'account_type': data['account_type'],
        'currency': data['currency']
    }

