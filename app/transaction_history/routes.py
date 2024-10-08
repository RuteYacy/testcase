from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.users.models import User
from app.core.database import get_db
from app.core.dependencies import get_auth_user

from app.transaction_history.models import TransactionHistory
from app.transaction_history.schemas import TransactionHistorySchema

router = APIRouter(
    prefix="/transaction-history",
    tags=["transaction-history"],
)


@router.get("/transaction_history", response_model=List[TransactionHistorySchema])
def get_transaction_history(
    current_user: User = Depends(get_auth_user),
    db: Session = Depends(get_db)
):
    transactions = (
        db.query(TransactionHistory)
        .filter(TransactionHistory.user_id == current_user.id)
        .all()
    )
    return transactions
