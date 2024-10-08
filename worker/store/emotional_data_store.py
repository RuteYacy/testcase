import logging

from database import get_db
from sqlalchemy.future import select

from models.emotional_data import EmotionalData

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def update_processed_score(
    emotional_data_id: int,
    processed_score: float,
):
    db = next(get_db())
    try:
        result = db.execute(select(EmotionalData).
                            filter(EmotionalData.id == emotional_data_id))
        emotional_data = result.scalar_one_or_none()

        if emotional_data:
            emotional_data.processed_score = processed_score
            db.commit()
        else:
            logging.warning(f"EmotionalData with ID {emotional_data_id} not found.")

    except Exception as e:
        logging.error(
            f"Error updating score for EmotionalData ID {emotional_data_id}: {e}",
        )
        db.rollback()
