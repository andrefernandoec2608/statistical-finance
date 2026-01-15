from flask import Blueprint, request, jsonify, current_app
from exceptions.finance_manager_exception import (
    DuplicateIDException,
    NotFoundIDException,
)
from api.serializers import budget_to_dict
from utils.enums import Category

budget_bp = Blueprint('budgets', __name__)

@budget_bp.route('/budgets', methods=['GET'])
def list_all_budgets():
    """Get all budgets."""
    try:
        budget_manager = current_app.config['budget_manager']
        budgets = budget_manager.get_all_budgets()
        
        return jsonify({
            'success': True,
            'budgets': [budget_to_dict(budget) for budget in budgets],
            'count': len(budgets)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@budget_bp.route('/budgets/<int:budget_id>', methods=['GET'])
def get_budget_by_id(budget_id: int):
    """Get a budget by ID."""
    try:
        budget_manager = current_app.config['budget_manager']
        budget = budget_manager.get_budget_by_id(budget_id)
        
        return jsonify({
            'success': True,
            'budget': budget_to_dict(budget)
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

@budget_bp.route('/budgets', methods=['POST'])
def create_budget():
    """Create a new budget."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        required_fields = ['id', 'month', 'category', 'limit_amount']
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
        
        budget_manager = current_app.config['budget_manager']
        
        # Create budget using manager
        budget_manager.create_budget(
            budget_id=data['id'],
            month=data['month'],
            category=category,
            limit_amount=float(data['limit_amount']),
        )
        
        # Fetch the created budget to return using manager method
        budget = budget_manager.get_budget_by_id(data['id'])
        
        return jsonify({
            'success': True,
            'message': 'Budget created successfully',
            'budget': budget_to_dict(budget)
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

@budget_bp.route('/budgets/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id: int):
    """Update a budget (limit_amount modification)."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        if 'limit_amount' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: limit_amount'
            }), 400
        
        budget_manager = current_app.config['budget_manager']
        budget_manager.modify_budget(
            budget_id=budget_id,
            limit_amount=float(data['limit_amount']),
        )
        
        # Fetch the updated budget to return using manager method
        budget = budget_manager.get_budget_by_id(budget_id)
        
        return jsonify({
            'success': True,
            'message': 'Budget updated successfully',
            'budget': budget_to_dict(budget)
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

@budget_bp.route('/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id: int):
    """Delete a budget."""
    try:
        budget_manager = current_app.config['budget_manager']
        budget_manager.delete_budget(budget_id)
        
        return jsonify({
            'success': True,
            'message': f'Budget with ID {budget_id} deleted successfully'
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

