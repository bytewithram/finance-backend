from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from routers import users, records, dashboard
from auth import verify_password, create_access_token, hash_password
from schemas import LoginRequest, Token
import models

# Create all database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="A backend system for managing financial records with role based access control",
    version="1.0.0"
)

# Include all routers
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to Finance Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Login route
@app.post("/auth/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive"
        )

    # Create and return token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Create first admin user (only works if no users exist)
@app.post("/setup")
def setup_admin(db: Session = Depends(get_db)):
    existing = db.query(models.User).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Setup already done. Users already exist."
        )

    admin = models.User(
        name="Super Admin",
        email="admin@finance.com",
        password=hash_password("admin123"),
        role="admin",
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {
        "message": "Admin created successfully",
        "email": "admin@finance.com",
        "password": "admin123",
        "role": "admin"
    }
