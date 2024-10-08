import logging
from datetime import datetime, timezone

from models.user import User
from database import get_db

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def update_credit_limit(user_id, new_credit_limit):
    db = next(get_db())
    try:
        # Query the user by user_id
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.credit_limit = new_credit_limit

            # Set the approved or denied date based on the new credit limit value
            if new_credit_limit > 0:
                user.approved_date = datetime.now(timezone.utc)
                user.denied_date = None
            elif new_credit_limit <= 0:
                user.denied_date = datetime.now(timezone.utc)
                user.approved_date = None

            db.commit()
            logging.info(f"Credit limit updated for user {user_id} to {new_credit_limit}")

        else:
            logging.warning(f"User with ID {user_id} not found.")

    except Exception as e:
        logging.error(f"Error updating credit limit for user {user_id}: {e}")
        db.rollback()

    finally:
        db.close()
