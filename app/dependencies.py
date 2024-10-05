import os
import jwt
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.core.database import get_db
from app.users.models import User


api_key_header = APIKeyHeader(
    name="Authorization",
    description="Enter the value in this format: `bearer accesstoken`"
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(api_key_header)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )

    try:
        scheme, _, token = token.partition(" ")
        if scheme.lower() != "bearer":
            raise credentials_exception

        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.user_email == user_email).first()
    if user is None:
        raise credentials_exception

    return user
