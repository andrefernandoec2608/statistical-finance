from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
    FinanceManagerException,
)
from api.serializers import account_to_dict

account_bp = Blueprint('accounts', __name__)

@account_bp.route('/accounts', methods=['GET'])
def list_all_accounts():
    try:
        account_manager = current_app.config['account_manager']
        accounts = account_manager.get_all_accounts()
        
        return jsonify({
            'success': True,
            'accounts': [account_to_dict(account) for account in accounts],
            'count': len(accounts)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@account_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id: int):
    try:
        account_manager = current_app.config['account_manager']
        account = account_manager.get_account_by_id(account_id)
        
        return jsonify({
            'success': True,
            'account': account_to_dict(account)
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

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        required_fields = ['id', 'name', 'account_type', 'currency']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        account_manager = current_app.config['account_manager']
        
        # Create account using manager
        account_manager.create_account(
            account_id=data['id'],
            name=data['name'],
            account_type=data['account_type'],
            currency=data['currency']
        )
        
        # Fetch the created account to return using manager method
        account = account_manager.get_account_by_id(data['id'])
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'account': account_to_dict(account)
        }), 201
    
    except DuplicateIDException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 409
    
    except FinanceManagerException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@account_bp.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id: int):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        if 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: name'
            }), 400
        
        account_manager = current_app.config['account_manager']
        account_manager.modify_account(account_id, data['name'])
        
        # Fetch the updated account to return using manager method
        account = account_manager.get_account_by_id(account_id)
        
        return jsonify({
            'success': True,
            'message': 'Account updated successfully',
            'account': account_to_dict(account)
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

@account_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id: int):
    try:
        account_manager = current_app.config['account_manager']
        account_manager.delete_account(account_id)
        
        return jsonify({
            'success': True,
            'message': f'Account with ID {account_id} deleted successfully'
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