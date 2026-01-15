from flask import Blueprint, request, jsonify, current_app
from datetime import date
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
)
from api.serializers import transaction_to_dict
from utils.enums import Category, TransactionType
from manager.statistics_manager import transaction_amount_statistics, transaction_category_summary, monthly_amount_forecast_linear

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def list_all_transactions():
    try:
        transaction_manager = current_app.config['transaction_manager']
        transactions = transaction_manager.get_all_transactions()

        return jsonify({
            'success': True,
            'transactions': [transaction_to_dict(transaction) for transaction in transactions],
            'count': len(transactions)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction_by_id(transaction_id: int):
    try:
        transaction_manager = current_app.config['transaction_manager']
        transaction = transaction_manager.get_transaction_by_id(transaction_id)
        
        return jsonify({
            'success': True,
            'transaction': transaction_to_dict(transaction)
        }), 200
    except NotFoundIDException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        required_fields = ['id', 'account_id', 'date', 'amount', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Parse date from ISO format string
        try:
            trx_date = date.fromisoformat(data['date'])
        except (ValueError, TypeError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
            }), 400
        
        # Parse category enum
        try:
            category = Category(data['category'])
        except (ValueError, KeyError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid category. Valid categories: {[c.value for c in Category]}'
            }), 400
        
        # Parse transaction_type enum (optional, defaults to EXPENSE)
        transaction_type = TransactionType.EXPENSE
        if 'transaction_type' in data:
            try:
                transaction_type = TransactionType(data['transaction_type'])
            except (ValueError, KeyError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid transaction_type. Valid types: {[t.value for t in TransactionType]}'
                }), 400
        
        transaction_manager = current_app.config['transaction_manager']
        
        # Create transaction using manager
        transaction_manager.create_transaction(
            transaction_id=data['id'],
            account_id=data['account_id'],
            trx_date=trx_date,
            amount=float(data['amount']),
            description=data.get('description', ''),
            category=category,
            transaction_type=transaction_type,
        )
        
        # Fetch the created transaction to return using manager method
        transaction = transaction_manager.get_transaction_by_id(data['id'])
        
        return jsonify({
            'success': True,
            'message': 'Transaction created successfully',
            'transaction': transaction_to_dict(transaction)
        }), 201
    
    except DuplicateIDException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 409
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id: int):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        required_fields = ['description', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Parse category enum
        try:
            category = Category(data['category'])
        except (ValueError, KeyError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid category. Valid categories: {[c.value for c in Category]}'
            }), 400
        
        # Parse transaction_type enum (optional)
        transaction_type = None
        if 'transaction_type' in data:
            try:
                transaction_type = TransactionType(data['transaction_type'])
            except (ValueError, KeyError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid transaction_type. Valid types: {[t.value for t in TransactionType]}'
                }), 400
        
        transaction_manager = current_app.config['transaction_manager']
        transaction_manager.modify_transaction(
            transaction_id=transaction_id,
            description=data['description'],
            category=category,
            transaction_type=transaction_type,
        )
        
        # Fetch the updated transaction to return using manager method
        transaction = transaction_manager.get_transaction_by_id(transaction_id)
        
        return jsonify({
            'success': True,
            'message': 'Transaction updated successfully',
            'transaction': transaction_to_dict(transaction)
        }), 200
    
    except NotFoundIDException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id: int):
    try:
        transaction_manager = current_app.config['transaction_manager']
        transaction_manager.delete_transaction(transaction_id)
        
        return jsonify({
            'success': True,
            'message': f'Transaction with ID {transaction_id} deleted successfully'
        }), 200
    
    except NotFoundIDException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/statistics', methods=['GET'])
def get_transaction_statistics():
    try:
        # Parse query parameters
        start_date = None
        end_date = None
        transaction_type = None
        
        if 'start_date' in request.args:
            try:
                start_date = date.fromisoformat(request.args['start_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid start_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        if 'end_date' in request.args:
            try:
                end_date = date.fromisoformat(request.args['end_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid end_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        if 'transaction_type' in request.args:
            try:
                transaction_type = TransactionType(request.args['transaction_type'])
            except (ValueError, KeyError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid transaction_type. Valid types: {[t.value for t in TransactionType]}'
                }), 400
        
        # Validate date range
        if start_date is not None and end_date is not None and start_date > end_date:
            return jsonify({
                'success': False,
                'error': 'start_date must be before or equal to end_date'
            }), 400
        
        transaction_manager = current_app.config['transaction_manager']
        
        # Get filtered transactions
        transactions = transaction_manager.get_filtered_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type
        )
        
        # Calculate statistics
        statistics = transaction_amount_statistics(transactions)
        
        return jsonify({
            'success': True,
            'statistics': statistics,
            'filter': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None,
                'transaction_type': transaction_type.value if transaction_type else None,
            },
            'transaction_count': len(transactions)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/category-summary', methods=['GET'])
def get_transaction_category_summary():
    try:
        # Parse query parameters
        start_date = None
        end_date = None
        
        if 'start_date' in request.args:
            try:
                start_date = date.fromisoformat(request.args['start_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid start_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        if 'end_date' in request.args:
            try:
                end_date = date.fromisoformat(request.args['end_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid end_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        # Validate date range
        if start_date is not None and end_date is not None and start_date > end_date:
            return jsonify({
                'success': False,
                'error': 'start_date must be before or equal to end_date'
            }), 400
        
        transaction_manager = current_app.config['transaction_manager']
        
        # Get filtered transactions
        transactions = transaction_manager.get_filtered_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=None
        )
        
        # Calculate category summary
        category_summary = transaction_category_summary(transactions)
        
        return jsonify({
            'success': True,
            'category_summary': category_summary,
            'filter': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None,
            },
            'transaction_count': len(transactions)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@transaction_bp.route('/transactions/monthly-forecast', methods=['GET'])
def get_monthly_forecast():
    try:
        # Parse query parameters
        start_date = None
        end_date = None
        
        # transaction_type is required for forecast
        if 'transaction_type' not in request.args:
            return jsonify({
                'success': False,
                'error': 'transaction_type is required. Valid types: Income, Expense'
            }), 400
        
        try:
            transaction_type = TransactionType(request.args['transaction_type'])
        except (ValueError, KeyError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid transaction_type. Valid types: {[t.value for t in TransactionType]}'
            }), 400
        
        # months_to_predict is required
        if 'months_to_predict' not in request.args:
            return jsonify({
                'success': False,
                'error': 'months_to_predict is required and must be > 0'
            }), 400
        
        try:
            months_to_predict = int(request.args['months_to_predict'])
            if months_to_predict <= 0:
                return jsonify({
                    'success': False,
                    'error': 'months_to_predict must be > 0'
                }), 400
        except (ValueError, TypeError) as e:
            return jsonify({
                'success': False,
                'error': f'Invalid months_to_predict. Must be a positive integer: {str(e)}'
            }), 400
        
        if 'start_date' in request.args:
            try:
                start_date = date.fromisoformat(request.args['start_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid start_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        if 'end_date' in request.args:
            try:
                end_date = date.fromisoformat(request.args['end_date'])
            except (ValueError, TypeError) as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid end_date format. Expected ISO format (YYYY-MM-DD): {str(e)}'
                }), 400
        
        # Validate date range
        if start_date is not None and end_date is not None and start_date > end_date:
            return jsonify({
                'success': False,
                'error': 'start_date must be before or equal to end_date'
            }), 400
        
        transaction_manager = current_app.config['transaction_manager']
        
        # Get filtered transactions (filter by transaction_type since it's required for forecast)
        transactions = transaction_manager.get_filtered_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=transaction_type
        )
        
        # Calculate monthly forecast
        forecast_result = monthly_amount_forecast_linear(
            transactions,
            transaction_type,
            months_to_predict
        )
        
        return jsonify({
            'success': True,
            'forecast': forecast_result,
            'filter': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None,
                'transaction_type': transaction_type.value,
            },
            'months_to_predict': months_to_predict,
            'transaction_count': len(transactions)
        }), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500