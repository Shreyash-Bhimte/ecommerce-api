import os
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    hashed_password = pwd_context.hash(password)

    return hashed_password

 
def verify_password(password: str, hashed_password: str ):
        
    is_match = pwd_context.verify(password, hashed_password)
    return is_match

def create_token(user_id: int):

    token = jwt.encode({"user_id": user_id}, key=os.getenv("SECRET_KEY"), algorithm="HS256")

    return token

def decode_token(token: str):

    payload = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])

    return payload
