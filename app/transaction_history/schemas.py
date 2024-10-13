from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CategoryEnum(str, Enum):
    home = "home"
    other = "other"
    transactions = "transactions"
    food = "food"
    education = "education"
    personal = "personal"
    communication = "communication"
    entertainment = "entertainment"
    health = "health"
    transport = "transport"
    tax = "tax"


class TransactionHistorySchema(BaseModel):
    id: int
    user_id: int
    transaction_date: datetime
    transaction_type: str
    amount: float
    balance_after_transaction: Optional[float] = None
    category: CategoryEnum

    model_config = {
        "from_attributes": True
    }
