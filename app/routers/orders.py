from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Order, User,Cart,CartItem,OrderItem,Product
from app.schemas import OrderResponse
from app.dependencies import get_current_user


router = APIRouter()

@router.post("/order",response_model= OrderResponse)
def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    new_order = Order(user_id= current_user.id, total_amount=0,status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


    for item in items:
        product  = db.query(Product).filter(Product.id == item.product_id ).first()
        order = OrderItem(order_id= new_order.id ,quantity=item.quantity, price_at_purchase= product.price)
        db.add(order)
        new_order.total_amount += product.price * item.quantity
    db.commit()
    db.refresh(new_order)
    
    for item in items:
        db.delete(item)
    db.commit()

    return new_order