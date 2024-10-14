from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    approved_date: Optional[date] = None
    denied_date: Optional[date] = None
    credit_limit: Optional[float] = None
    balance: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


class UserSignUp(BaseModel):
    email: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
