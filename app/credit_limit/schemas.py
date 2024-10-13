from datetime import datetime
from pydantic import BaseModel


class CreditLimitSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    risk_score: float
    credit_limit: float
    emotional_data_id: int
    primary_emotion: str

    model_config = {
        "from_attributes": True
    }
