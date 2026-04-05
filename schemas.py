from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ─── USER SCHEMAS ───────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "viewer"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ─── AUTH SCHEMAS ───────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ─── FINANCIAL RECORD SCHEMAS ───────────────────

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str] = None

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class RecordOut(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str]
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True