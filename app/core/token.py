import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = os.getenv('SECRET_KEY')

# The algorithm to use for signing the JWT tokens
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Function to create a JWT access token.

    Returns:
    - encoded_jwt: The JWT token as a string.
    """
    to_encode = data.copy()  # Make a copy of the data to avoid altering the original

    # If a custom expiration time is provided, use that
    # Otherwise, use the default expiration time of 30 minutes
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Function to verify the JWT token and decode its payload.

    Returns:
    - payload: The decoded data from the token if it is valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
