from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserSchema(BaseModel):
    user_id: Optional[int] = None
    user_email: str
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
    user_email: str
    password: str


class UserSignIn(BaseModel):
    user_email: str
    password: str
