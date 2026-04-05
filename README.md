# Finance Dashboard Backend

A backend system for managing financial records with role-based access control, built with FastAPI and SQLite.

## Tech Stack
- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT

## How to Run Locally

1. Install dependencies:
   pip install fastapi uvicorn sqlalchemy PyJWT python-multipart

2. Start the server:
   python -m uvicorn main:app --reload

## First Time Setup

1. Call POST /setup to create the first admin user
2. Login using POST /auth/login with:
   - email: admin@finance.com
   - password: admin123
3. Copy the token and use it to authorize all requests

## Roles and Access Control

| Role    | View Records | Create/Edit Records | Manage Users | View Analytics |
|---------|-------------|---------------------|-------------|----------------|
| Admin   | Yes         | Yes                 | Yes         | Yes            |
| Analyst | Yes         | No                  | No          | Yes            |
| Viewer  | Yes         | No                  | No          | No             |

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
- POST /records/ - Create record (Admin only)
- GET /records/ - Get all records with filters (All roles)
- GET /records/{id} - Get single record (All roles)
- PUT /records/{id} - Update record (Admin only)
- DELETE /records/{id} - Soft delete record (Admin only)

### Dashboard
- GET /dashboard/summary - Total income, expense, balance (All roles)
- GET /dashboard/category-totals - Totals by category (Analyst and Admin)
- GET /dashboard/recent-activity - Last 10 transactions (All roles)
- GET /dashboard/monthly-trends - Monthly breakdown (Analyst and Admin)
- GET /dashboard/breakdown - Income vs expense count (All roles)

## Assumptions
- SQLite used for simplicity
- Passwords hashed using SHA256
- JWT tokens expire after 60 minutes
- Soft delete used for financial records
- First admin created via /setup endpoint

## Database Models

### User
- id, name, email, password, role, is_active, created_at

### Financial Record
- id, amount, type, category, date, notes, is_deleted, created_at, created_by