from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.users.models import User
from app.core.database import get_db
from app.core.dependencies import get_auth_user

from app.credit_limit.models import CreditLimit
from app.credit_limit.schemas import CreditLimitSchema


router = APIRouter(
    prefix="/credit-history",
    tags=["credit-history"],
)


@router.get("/",
            response_model=List[CreditLimitSchema],
            status_code=status.HTTP_200_OK)
def get_credit_limit(
    current_user: User = Depends(get_auth_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the credit limit history for the authenticated user.
    """
    credit_limit = (
        db.query(CreditLimit)
        .filter(CreditLimit.user_id == current_user.id)
        .all()
    )

    if not credit_limit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No credit limit history found for the current user."
        )

    return credit_limit


@router.get("/monthly",
            response_model=List[CreditLimitSchema],
            status_code=status.HTTP_200_OK)
async def get_monthly_credit_limit(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, le=datetime.now().year, description="Year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_auth_user)
):
    """
    Retrieves the credit limit history for the authenticated user for a specified
    month and year, sorted by the most recent entry first.

    Returns:
    - A list of credit limit history entries for the specified month and year.
    """
    try:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        credit_limits = db.query(CreditLimit).filter(
            CreditLimit.user_id == current_user.id,
            CreditLimit.created_at >= start_date,
            CreditLimit.created_at < end_date
        ).order_by(CreditLimit.created_at.desc()).all()

        if not credit_limits:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit limit history found for the specified month and year."
            )

        return credit_limits

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the credit limit history."
        )
