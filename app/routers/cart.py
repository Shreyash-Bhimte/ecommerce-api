from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/cart")
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # current_user is the logged in user
    pass