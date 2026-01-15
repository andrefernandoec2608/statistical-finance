# Personal Finance Manager API Documentation 📚

This document describes the REST API endpoints for the Personal Finance Manager application. The API is built with Flask and provides endpoints for managing accounts, transactions, and budgets.

## Base URL

All API endpoints are prefixed with `/api`:
```
http://localhost:5000/api
```

## Response Format

All API responses follow a consistent JSON format:

**Success Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

---

## Account API

The Account API allows you to manage financial accounts (Bank, Savings, and Wallet accounts).

### Base Endpoint
```
/api/accounts
```

### 1. List All Accounts

Retrieves a list of all accounts.

**Endpoint:** `GET /api/accounts`

**Response:**
```json
{
  "success": true,
  "accounts": [
    {
      "id": 1,
      "name": "Main Bank Account",
      "account_type": "Bank",
      "currency": "USD"
    }
  ],
  "count": 1
}
```

**Status Codes:**
- `200 OK`: Success
- `500 Internal Server Error`: Server error

---

### 2. Get Account by ID

Retrieves a specific account by its ID.

**Endpoint:** `GET /api/accounts/<account_id>`

**Parameters:**
- `account_id` (path parameter, integer): The unique identifier of the account

**Example Request:**
```
GET /api/accounts/1
```

**Response:**
```json
{
  "success": true,
  "account": {
    "id": 1,
    "name": "Main Bank Account",
    "account_type": "Bank",
    "currency": "USD"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Account not found
- `500 Internal Server Error`: Server error

---

### 3. Create Account

Creates a new account.

**Endpoint:** `POST /api/accounts`

**Request Body:**
```json
{
  "id": 1,
  "name": "Main Bank Account",
  "account_type": "Bank",
  "currency": "USD"
}
```

**Required Fields:**
- `id` (integer): Unique identifier for the account
- `name` (string): Name of the account
- `account_type` (string): Type of account - valid values: `"Bank"`, `"Savings"`, `"Wallet"`
- `currency` (string): Currency code - valid values: `"USD"`, `"EUR"`

**Response:**
```json
{
  "success": true,
  "message": "Account created successfully",
  "account": {
    "id": 1,
    "name": "Main Bank Account",
    "account_type": "Bank",
    "currency": "USD"
  }
}
```

**Status Codes:**
- `201 Created`: Account created successfully
- `400 Bad Request`: Invalid request data or missing required fields
- `409 Conflict`: Account with this ID already exists
- `500 Internal Server Error`: Server error

---

### 4. Update Account

Updates an existing account's name.

**Endpoint:** `PUT /api/accounts/<account_id>`

**Parameters:**
- `account_id` (path parameter, integer): The unique identifier of the account

**Request Body:**
```json
{
  "name": "Updated Account Name"
}
```

**Required Fields:**
- `name` (string): New name for the account

**Example Request:**
```
PUT /api/accounts/1
Content-Type: application/json

{
  "name": "Updated Account Name"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account updated successfully",
  "account": {
    "id": 1,
    "name": "Updated Account Name",
    "account_type": "Bank",
    "currency": "USD"
  }
}
```

**Status Codes:**
- `200 OK`: Account updated successfully
- `400 Bad Request`: Missing required field `name`
- `404 Not Found`: Account not found
- `500 Internal Server Error`: Server error

---

### 5. Delete Account

Deletes an account by its ID.

**Endpoint:** `DELETE /api/accounts/<account_id>`

**Parameters:**
- `account_id` (path parameter, integer): The unique identifier of the account

**Example Request:**
```
DELETE /api/accounts/1
```

**Response:**
```json
{
  "success": true,
  "message": "Account with ID 1 deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Account deleted successfully
- `404 Not Found`: Account not found
- `500 Internal Server Error`: Server error

---

## Transaction API

The Transaction API allows you to manage financial transactions (income and expenses) associated with accounts.

### Base Endpoint
```
/api/transactions
```

### 1. List All Transactions

Retrieves a list of all transactions.

**Endpoint:** `GET /api/transactions`

**Response:**
```json
{
  "success": true,
  "transactions": [
    {
      "id": 1,
      "account_id": 1,
      "date": "2024-01-15",
      "amount": 50.00,
      "description": "Grocery shopping",
      "category": "Food",
      "transaction_type": "Expense"
    }
  ],
  "count": 1
}
```

**Status Codes:**
- `200 OK`: Success
- `500 Internal Server Error`: Server error

---

### 2. Get Transaction by ID

Retrieves a specific transaction by its ID.

**Endpoint:** `GET /api/transactions/<transaction_id>`

**Parameters:**
- `transaction_id` (path parameter, integer): The unique identifier of the transaction

**Example Request:**
```
GET /api/transactions/1
```

**Response:**
```json
{
  "success": true,
  "transaction": {
    "id": 1,
    "account_id": 1,
    "date": "2024-01-15",
    "amount": 50.00,
    "description": "Grocery shopping",
    "category": "Food",
    "transaction_type": "Expense"
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Transaction not found
- `500 Internal Server Error`: Server error

---

### 3. Create Transaction

Creates a new transaction.

**Endpoint:** `POST /api/transactions`

**Request Body:**
```json
{
  "id": 1,
  "account_id": 1,
  "date": "2024-01-15",
  "amount": 50.00,
  "description": "Grocery shopping",
  "category": "Food",
  "transaction_type": "Expense"
}
```

**Required Fields:**
- `id` (integer): Unique identifier for the transaction
- `account_id` (integer): ID of the associated account
- `date` (string): Transaction date in ISO format (YYYY-MM-DD)
- `amount` (float): Transaction amount (must be positive)
- `category` (string): Transaction category - valid values: `"Food"`, `"Transport"`, `"Entertainment"`, `"Health"`, `"Utilities"`, `"Other"`

**Optional Fields:**
- `description` (string): Transaction description (defaults to empty string)
- `transaction_type` (string): Type of transaction - valid values: `"Income"`, `"Expense"` (defaults to `"Expense"`)

**Response:**
```json
{
  "success": true,
  "message": "Transaction created successfully",
  "transaction": {
    "id": 1,
    "account_id": 1,
    "date": "2024-01-15",
    "amount": 50.00,
    "description": "Grocery shopping",
    "category": "Food",
    "transaction_type": "Expense"
  }
}
```

**Status Codes:**
- `201 Created`: Transaction created successfully
- `400 Bad Request`: Invalid request data, missing required fields, or invalid date/category format
- `409 Conflict`: Transaction with this ID already exists
- `500 Internal Server Error`: Server error

---

### 4. Update Transaction

Updates an existing transaction's description, category, and optionally transaction type.

**Endpoint:** `PUT /api/transactions/<transaction_id>`

**Parameters:**
- `transaction_id` (path parameter, integer): The unique identifier of the transaction

**Request Body:**
```json
{
  "description": "Updated description",
  "category": "Transport",
  "transaction_type": "Expense"
}
```

**Required Fields:**
- `description` (string): Updated transaction description
- `category` (string): Updated transaction category - valid values: `"Food"`, `"Transport"`, `"Entertainment"`, `"Health"`, `"Utilities"`, `"Other"`

**Optional Fields:**
- `transaction_type` (string): Updated transaction type - valid values: `"Income"`, `"Expense"`

**Example Request:**
```
PUT /api/transactions/1
Content-Type: application/json

{
  "description": "Updated description",
  "category": "Transport"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "transaction": {
    "id": 1,
    "account_id": 1,
    "date": "2024-01-15",
    "amount": 50.00,
    "description": "Updated description",
    "category": "Transport",
    "transaction_type": "Expense"
  }
}
```

**Status Codes:**
- `200 OK`: Transaction updated successfully
- `400 Bad Request`: Missing required fields or invalid category/transaction_type
- `404 Not Found`: Transaction not found
- `500 Internal Server Error`: Server error

---

### 5. Delete Transaction

Deletes a transaction by its ID.

**Endpoint:** `DELETE /api/transactions/<transaction_id>`

**Parameters:**
- `transaction_id` (path parameter, integer): The unique identifier of the transaction

**Example Request:**
```
DELETE /api/transactions/1
```

**Response:**
```json
{
  "success": true,
  "message": "Transaction with ID 1 deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Transaction deleted successfully
- `404 Not Found`: Transaction not found
- `500 Internal Server Error`: Server error

---

### 6. Get Transaction Statistics

Retrieves statistical information about transactions with optional filtering.

**Endpoint:** `GET /api/transactions/statistics`

**Query Parameters:**
- `start_date` (optional, string): Start date in ISO format (YYYY-MM-DD) for filtering transactions
- `end_date` (optional, string): End date in ISO format (YYYY-MM-DD) for filtering transactions
- `transaction_type` (optional, string): Filter by transaction type - valid values: `"Income"`, `"Expense"`

**Example Request:**
```
GET /api/transactions/statistics?start_date=2024-01-01&end_date=2024-01-31&transaction_type=Expense
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total": 500.00,
    "average": 50.00,
    "min": 10.00,
    "max": 100.00,
    "count": 10
  },
  "filter": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "transaction_type": "Expense"
  },
  "transaction_count": 10
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid date format or invalid date range (start_date > end_date)
- `500 Internal Server Error`: Server error

---

### 7. Get Transaction Category Summary

Retrieves a summary of transactions grouped by category.

**Endpoint:** `GET /api/transactions/category-summary`

**Query Parameters:**
- `start_date` (optional, string): Start date in ISO format (YYYY-MM-DD) for filtering transactions
- `end_date` (optional, string): End date in ISO format (YYYY-MM-DD) for filtering transactions

**Example Request:**
```
GET /api/transactions/category-summary?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
{
  "success": true,
  "category_summary": {
    "Food": 200.00,
    "Transport": 150.00,
    "Entertainment": 100.00,
    "Utilities": 50.00
  },
  "filter": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  },
  "transaction_count": 10
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid date format or invalid date range
- `500 Internal Server Error`: Server error

---

### 8. Get Monthly Forecast

Retrieves a linear forecast of monthly transaction amounts.

**Endpoint:** `GET /api/transactions/monthly-forecast`

**Query Parameters:**
- `transaction_type` (required, string): Type of transaction to forecast - valid values: `"Income"`, `"Expense"`
- `months_to_predict` (required, integer): Number of months to forecast (must be > 0)
- `start_date` (optional, string): Start date in ISO format (YYYY-MM-DD) for filtering historical transactions
- `end_date` (optional, string): End date in ISO format (YYYY-MM-DD) for filtering historical transactions

**Example Request:**
```
GET /api/transactions/monthly-forecast?transaction_type=Expense&months_to_predict=3&start_date=2024-01-01&end_date=2024-03-31
```

**Response:**
```json
{
  "success": true,
  "forecast": {
    "predicted_monthly_amounts": [500.00, 520.00, 540.00],
    "slope": 20.00,
    "intercept": 480.00
  },
  "filter": {
    "start_date": "2024-01-01",
    "end_date": "2024-03-31",
    "transaction_type": "Expense"
  },
  "months_to_predict": 3,
  "transaction_count": 90
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Missing required parameters, invalid date format, or invalid months_to_predict value
- `500 Internal Server Error`: Server error

---

## Valid Enum Values

### Account Types
- `"Bank"`
- `"Savings"`
- `"Wallet"`

### Currencies
- `"USD"`
- `"EUR"`

### Transaction Types
- `"Income"`
- `"Expense"`

### Categories
- `"Food"`
- `"Transport"`
- `"Entertainment"`
- `"Health"`
- `"Utilities"`
- `"Other"`

---

## Example Usage

### Using cURL

**Create an Account:**
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Main Bank Account",
    "account_type": "Bank",
    "currency": "USD"
  }'
```

**Create a Transaction:**
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "account_id": 1,
    "date": "2024-01-15",
    "amount": 50.00,
    "description": "Grocery shopping",
    "category": "Food",
    "transaction_type": "Expense"
  }'
```

**Get Transaction Statistics:**
```bash
curl "http://localhost:5000/api/transactions/statistics?start_date=2024-01-01&end_date=2024-01-31&transaction_type=Expense"
```

### Using Python requests

```python
import requests

base_url = "http://localhost:5000/api"

# Create an account
account_data = {
    "id": 1,
    "name": "Main Bank Account",
    "account_type": "Bank",
    "currency": "USD"
}
response = requests.post(f"{base_url}/accounts", json=account_data)
print(response.json())

# Create a transaction
transaction_data = {
    "id": 1,
    "account_id": 1,
    "date": "2024-01-15",
    "amount": 50.00,
    "description": "Grocery shopping",
    "category": "Food",
    "transaction_type": "Expense"
}
response = requests.post(f"{base_url}/transactions", json=transaction_data)
print(response.json())

# Get statistics
response = requests.get(
    f"{base_url}/transactions/statistics",
    params={
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "transaction_type": "Expense"
    }
)
print(response.json())
```

