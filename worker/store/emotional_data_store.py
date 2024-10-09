import logging

from database import get_db
from sqlalchemy.future import select

from models.emotional_data import EmotionalData


def update_data_score(
    emotional_data_id: int,
    risk_score: float,
    processed_limit: float,
):
    db = next(get_db())
    try:
        # Execute a query to find the EmotionalData record with the given ID
        result = db.execute(select(EmotionalData).
                            filter(EmotionalData.id == emotional_data_id))
        emotional_data = result.scalar_one_or_none()

        # If the record is found, update the risk_score and processed_limit fields
        if emotional_data:
            emotional_data.risk_score = risk_score
            emotional_data.processed_limit = processed_limit
            db.commit()
        else:
            logging.warning(f"EmotionalData with ID {emotional_data_id} not found.")

    except Exception as e:
        logging.error(
            f"Error updating score for EmotionalData ID {emotional_data_id}: {e}",
        )
        # Roll back the transaction if an error occurs
        db.rollback()
