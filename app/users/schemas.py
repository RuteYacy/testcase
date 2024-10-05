from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    user_id: int
    score: int
    approved_date: date | None
    denied_date: date | None
    credit_limit: int | None
    interest_rate: float | None
    loan_term: int | None

    class Config:
        orm_mode = True
