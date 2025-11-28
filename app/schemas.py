from datetime import datetime
from pydantic import BaseModel, EmailStr


# ===== JWT / Auth Schemas =====

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ===== User Schemas =====

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ===== Calculation Schemas =====

class CalculationBase(BaseModel):
    operand1: float
    operand2: float
    operation: str


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operand1: float | None = None
    operand2: float | None = None
    operation: str | None = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    created_at: datetime

    class Config:
        orm_mode = True
