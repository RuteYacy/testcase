from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.users.models import User
from app.core.database import get_db
from app.core.dependencies import get_auth_user
from app.emotional_data.models import EmotionalData
from app.emotional_data.schemas import EmotionalDataInput

router = APIRouter(
    prefix="/emotional-data",
    tags=["emotional-data"],
)


@router.post("/save-emotional-data",
             response_model=dict,
             status_code=status.HTTP_201_CREATED)
async def save_emotional_data(
    emotion_data: EmotionalDataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_auth_user),
):
    """
    Submit user's emotional data to be stored.

    Returns:
    - A dictionary containing the stored emotional data details.
    """
    try:
        new_emotional_data = EmotionalData(
            user_id=current_user.id,
            timestamp=datetime.now(),
            primary_emotion=emotion_data.primary_emotion,
            intensity=emotion_data.intensity,
            context=emotion_data.context,
        )

        db.add(new_emotional_data)
        db.commit()
        db.refresh(new_emotional_data)

        return {
            "id": new_emotional_data.id,
            "user_id": current_user.id,
            "primary_emotion": emotion_data.primary_emotion,
            "intensity": emotion_data.intensity,
            "context": emotion_data.context,
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the emotional data."
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or request format."
        )


@router.get("/monthly",
            response_model=List[dict],
            status_code=status.HTTP_200_OK)
async def get_monthly_emotional_data(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, le=datetime.now().year, description="Year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_auth_user),
):
    """
    Retrieve emotional data for the current user for a specified month and year,
    sorted by the most recent entry first.

    Returns:
    - A list of emotional data entries for a specified month and year.
    """
    try:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        emotional_data_entries = db.query(EmotionalData).filter(
            EmotionalData.user_id == current_user.id,
            EmotionalData.timestamp >= start_date,
            EmotionalData.timestamp < end_date
        ).order_by(EmotionalData.timestamp.desc()).all()

        return [
            {
                "id": entry.id,
                "user_id": entry.user_id,
                "timestamp": entry.timestamp,
                "primary_emotion": entry.primary_emotion,
                "intensity": entry.intensity,
                "context": entry.context,
            }
            for entry in emotional_data_entries
        ]

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the emotional data."
        )
