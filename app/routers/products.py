from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductResponse,ProductCreate

router = APIRouter()


@router.get("/products",response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()
    return all_products

@router.post("/products",response_model=ProductResponse)
def create_products(product: ProductCreate ,db: Session = Depends(get_db)):
    new_product = Product(name= product.name ,description= product.description ,price= product.price ,stock_quantity= product.stock_quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int,db: Session = Depends(get_db)):
    product_by_id = db.query(Product).filter(Product.id == id).first()
    if not product_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return product_by_id

@router.put("/products/{id}",response_model=ProductResponse)
def update_products(id: int,product: ProductCreate ,db: Session = Depends(get_db)):
    product_by_id = db.query(Product).filter(Product.id == id).first()
    if not product_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    
    product_by_id.name= product.name 
    product_by_id.description= product.description 
    product_by_id.price= product.price 
    product_by_id.stock_quantity= product.stock_quantity

    db.commit()
    db.refresh(product_by_id)

    return product_by_id

@router.delete("/products/{id}")
def delete_products(id: int ,db: Session = Depends(get_db)):
    product_by_id = db.query(Product).filter(Product.id == id).first()
    if not product_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

    db.delete(product_by_id)
    db.commit()

    return {"message": "product deleted"}