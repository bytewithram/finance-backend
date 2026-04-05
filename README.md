# Finance Dashboard Backend

A backend system for managing financial records with role-based access control, built with FastAPI and SQLite.

## Tech Stack
- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT

## Setup Instructions

1. Install dependencies:
pip install fastapi uvicorn sqlalchemy PyJWT python-multipart passlib

2. Run the server:
python -m uvicorn main:app --reload



## First Time Setup

1. Call POST /setup to create the first admin user
2. Login using POST /auth/login with:
   - email: admin@finance.com
   - password: admin123
3. Copy the token and use it to authorize all requests

## Roles & Access Control

| Role    | View Records | Create/Edit Records | Manage Users | View Analytics |
|---------|-------------|--------------------:|-------------|----------------|
| Admin   | ✅          | ✅                  | ✅          | ✅             |
| Analyst | ✅          | ❌                  | ❌          | ✅             |
| Viewer  | ✅          | ❌                  | ❌          | ❌             |

## API Endpoints

### Auth
- POST /setup - Create first admin
- POST /auth/login - Login and get token

### Users (Admin only)
- POST /users/ - Create user
- GET /users/ - Get all users
- GET /users/{id} - Get user by ID
- PUT /users/{id} - Update user
- DELETE /users/{id} - Delete user

### Financial Records
- POST /records/ - Create record (Admin)
- GET /records/ - Get all records with filters (All)
- GET /records/{id} - Get single record (All)
- PUT /records/{id} - Update record (Admin)
- DELETE /records/{id} - Soft delete record (Admin)

### Dashboard
- GET /dashboard/summary - Total income, expense, balance (All)
- GET /dashboard/category-totals - Totals by category (Analyst+)
- GET /dashboard/recent-activity - Last 10 transactions (All)
- GET /dashboard/monthly-trends - Monthly breakdown (Analyst+)
- GET /dashboard/breakdown - Income vs expense count (All)

## Assumptions
- SQLite used for simplicity - can be replaced with PostgreSQL
- Passwords hashed using SHA256
- JWT tokens expire after 60 minutes
- Soft delete used for financial records
- First admin created via /setup endpoint

## Database Models

### User
- id, name, email, password, role, is_active, created_at

### FinancialRecord
- id, amount, type, category, date, notes, is_deleted, created_at, created_by