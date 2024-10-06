from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: str
    approved_date: Optional[date] = None
    denied_date: Optional[date] = None
    credit_limit: Optional[int] = None
    interest_rate: Optional[float] = None
    loan_term: Optional[int] = None
    score: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class UserSignUp(BaseModel):
    email: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str
