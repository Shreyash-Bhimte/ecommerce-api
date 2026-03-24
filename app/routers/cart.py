from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Cart,CartItem, User
from app.dependencies import get_current_user
from app.schemas import CartItemCreate,ProductCreate


router = APIRouter()



@router.post("/cart",response_model=CartItemCreate)
def add_item( item: CartItemCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id= current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    new_item = CartItem(cart_id=cart.id, product_id= item.product_id, quantity= item.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

@router.get("/cart")
def get_all_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return items


@router.delete("/cart/{id}")
def delete_products(id: int ,db: Session = Depends(get_db)):
    product_by_id = db.query(Product).filter(Product.id == id).first()
    if not product_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

    db.delete(product_by_id)
    db.commit()

    return {"message": "product deleted"}