import os
import jwt
from typing import Optional
from datetime import datetime, timedelta, timezone


# The algorithm to use for signing the JWT tokens
ALGORITHM = os.getenv("ALGORITHM")

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_DURATION = os.getenv('ACCESS_TOKEN_DURATION')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Function to create a JWT access token.

    Returns:
    - encoded_jwt: The JWT token as a string.
    """
    try:
        to_encode = data.copy()  # Make a copy of the data to avoid altering the original

        # If a custom expiration time is provided, use that
        # Otherwise, use the default expiration time of 30 minutes
        if expires_delta:
            expire = datetime.now(tz=timezone.utc) + expires_delta
        else:
            expire = datetime.now(tz=timezone.utc) + timedelta(
                hours=int(ACCESS_TOKEN_DURATION),
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    except Exception:
        raise ValueError("An error occurred while creating the access token")


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

    except Exception:
        raise ValueError("An error occurred while verifying the token")
