from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status, Query

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


@router.get("/monthly",
            response_model=List[TransactionHistorySchema],
            status_code=status.HTTP_200_OK)
async def get_monthly_transaction_history(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, le=datetime.now().year, description="Year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_auth_user),
):
    """
    Retrieve transaction history for the current user for a specified month and year,
    sorted by the most recent entry first.

    Returns:
    - A list of transaction history entries for the specified month and year.
    """
    try:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        transactions = db.query(TransactionHistory).filter(
            TransactionHistory.user_id == current_user.id,
            TransactionHistory.transaction_date >= start_date,
            TransactionHistory.transaction_date < end_date
        ).order_by(TransactionHistory.transaction_date.desc()).all()

        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No transaction history found for the specified month and year."
            )

        return transactions

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the transaction history."
        )
