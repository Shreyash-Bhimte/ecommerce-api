from datetime import datetime
from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str  # usually "bearer"
    
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name : str
    description : str
    price : float
    stock_quantity : int

class ProductResponse(BaseModel):
    id: int
    name : str
    description : str
    price : float
    stock_quantity : int
    created_at : datetime
    
    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at : datetime

    class Config:
        from_attributes = True