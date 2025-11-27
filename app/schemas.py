# FILE: app/schemas.py
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


# ------------- User Schemas ------------- #

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ------------- Calculation Schemas ------------- #

class CalculationBase(BaseModel):
    operation: str
    operand1: float
    operand2: float


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    owner_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True
