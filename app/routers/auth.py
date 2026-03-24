from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserRegister, UserResponse, TokenResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.services.auth import hash_password, verify_password, create_token
router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(data: UserRegister , db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user already exists")
    hashed_password = hash_password(password= data.password)
    new_user = User(email=data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.post("/login", response_model=TokenResponse)
def login(data: UserRegister , db: Session = Depends(get_db)):
    user =  db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    is_match = verify_password(data.password, user.hashed_password)

    if not is_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password")

    token = create_token(user.id)
    return TokenResponse(access_token=token, token_type="bearer")