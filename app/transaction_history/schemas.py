from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TransactionHistorySchema(BaseModel):
    id: int
    user_id: int
    transaction_date: datetime
    transaction_type: str
    amount: float
    balance_after_transaction: Optional[float] = None
    category: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
