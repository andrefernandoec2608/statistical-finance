# Personal Finance Manager 💸

This is the final project for my last midterm of the **Python Practical Classes** in the **Master's Program at ELTE** 🏦.

It is a **REST API** application built with Flask for managing personal finance: accounts, transactions, and budgets. The project uses **virtual environments**, **SQLite database**, and a modular architecture following the DAO (Data Access Object) pattern.

---

## 📦 Project Structure

```
personalfinance/
│
├── api/
│   ├── ApiConnection.py       # Flask application setup
│   ├── routes/
│   │   ├── account_routes.py  # Account API endpoints
│   │   ├── transaction_routes.py  # Transaction API endpoints
│   │   └── budget_routes.py   # Budget API endpoints
│   └── serializers.py         # JSON serialization utilities
│
├── database/
│   ├── db_connection.py       # Database connection management
│   ├── account_dao.py         # Account data access layer
│   ├── transaction_dao.py     # Transaction data access layer
│   ├── budget_dao.py          # Budget data access layer
│   └── personalfinance.db     # SQLite database file
│
├── manager/
│   ├── account_manager.py     # Account business logic
│   ├── transaction_manager.py # Transaction business logic
│   ├── budget_manager.py      # Budget business logic
│   └── statistics_manager.py  # Statistics and forecasting
│
├── model/
│   ├── account.py             # Base account model
│   ├── bank_account.py        # Bank account model
│   ├── savings_account.py     # Savings account model
│   ├── wallet_account.py      # Wallet account model
│   ├── transaction.py         # Transaction model
│   └── budget.py              # Budget model
│
├── exceptions/
│   └── finance_manager_exception.py  # Custom exceptions
│
├── utils/
│   └── enums.py               # Enumerations (Category, AccountType, etc.)
│
├── app_state.py               # Application state management
├── main.py                    # Application entry point
└── requirements.txt           # Python dependencies

```

---

## 📥 Install Dependencies

Once the virtual environment is activated:

```bash
pip install -r requirements.txt
```

This installs all required packages (Flask, pytest, etc.).

---

## ▶️ Running the Application

With the virtual environment activated:

```bash
python main.py
```

This starts the Flask API server on `http://0.0.0.0:5000`.

The API endpoints are available under the `/api` prefix:
- Accounts: `http://localhost:5000/api/accounts`
- Transactions: `http://localhost:5000/api/transactions`
- Budgets: `http://localhost:5000/api/budgets`

For detailed API documentation, see [API.md](./API.md).

---

## 🟠 APIs developed for POSTMAN

Postman's project:

- personal_finance.postman_collection.json


---

## 👨‍💻 Author
[![LinkedIn](https://img.shields.io/badge/LinkedIn-André%20Llumiquinga-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/andre-llc/)
[![GitHub](https://img.shields.io/badge/GitHub-André%20Llumiquinga-black?style=flat&logo=github)](https://github.com/andrefernandoec2608)