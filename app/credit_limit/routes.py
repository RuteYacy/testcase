from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

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
