from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.users.models import User
from app.core.database import get_db
from app.core.dependencies import get_auth_user

from app.transaction_history.models import TransactionHistory
from app.transaction_history.schemas import TransactionHistorySchema


router = APIRouter(
    prefix="/transaction-history",
    tags=["transaction-history"],
)


@router.get("/",
            response_model=List[TransactionHistorySchema],
            status_code=status.HTTP_200_OK)
def get_transaction_history(
    current_user: User = Depends(get_auth_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the transaction history for the authenticated user.
    """
    transactions = (
        db.query(TransactionHistory)
        .filter(TransactionHistory.user_id == current_user.id)
        .all()
    )

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transaction history found for the current user."
        )

    return transactions
