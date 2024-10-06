from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.sessions.models import Sessions


def create_session(
    db: Session,
    user_id: int,
    refresh_token: str,
    client_ip: str,
    refresh_token_expires: timedelta,
) -> Sessions:
    """
    Create a new session for the user and store it in the database.

    Returns:
    - The created session object.
    """
    new_session = Sessions(
        user_id=user_id,
        refresh_token=refresh_token,
        client_ip=client_ip,
        expires_at=datetime.now(timezone.utc) + refresh_token_expires,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session
