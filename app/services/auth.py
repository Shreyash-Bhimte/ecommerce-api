# import os
# from passlib.context import CryptContext
# from jose import jwt

# pwd_context = CryptContext(schemes=["bcrypt"])


# def hash_password(password: str):
#     hashed_password = pwd_context.hash(password)

#     return hashed_password

 
# def verify_password(password: str, hashed_password: str ):
        
#     is_match = pwd_context.verify(password, hashed_password)
#     return is_match

# def create_token(user_id: int):

#     token = jwt.encode({"user_id": user_id}, key=os.getenv("SECRET_KEY"), algorithm="HS256")

#     return token

# def decode_token(token: str):

#     payload = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])

#     return payload



from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

# Use Argon2 instead of bcrypt to avoid version conflicts
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = "your-secret-key"  # Change this to a real secret in production!

def hash_password(password: str) -> str:
    """
    Hash password with Argon2.
    No byte length limit like bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_token(user_id: int) -> str:
    """
    Create JWT token for user.
    Token expires in 24 hours.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str) -> dict:
    """
    Decode JWT token and return payload.
    Raises jwt.InvalidTokenError if token is invalid.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload