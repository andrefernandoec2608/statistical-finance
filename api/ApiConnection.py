from flask import Flask
from app_state import AppState
from manager.account_manager import AccountManager
from manager.transaction_manager import TransactionManager
from manager.budget_manager import BudgetManager
from api.routes.account_routes import account_bp
from api.routes.transaction_routes import transaction_bp
from api.routes.budget_routes import budget_bp

class ApiConnection:
    def __init__(self, app_state: AppState):
        self.app = Flask(__name__)
        
        # Store managers in app config for access in routes
        account_manager = AccountManager(app_state.account_dao)
        transaction_manager = TransactionManager(app_state.transaction_dao)
        budget_manager = BudgetManager(app_state.budget_dao)
        
        self.app.config['account_manager'] = account_manager
        self.app.config['transaction_manager'] = transaction_manager
        self.app.config['budget_manager'] = budget_manager
        
        # Register blueprints
        self.app.register_blueprint(account_bp, url_prefix='/api')
        self.app.register_blueprint(transaction_bp, url_prefix='/api')
        self.app.register_blueprint(budget_bp, url_prefix='/api')

    def run_app(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)