from fastapi import APIRouter, Depends
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
def post_products(product: ProductCreate ,db: Session = Depends(get_db)):
    new_product = Product(name= product.name ,description= product.description ,price= product.price ,stock_quantity= product.stock_quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/products/{id}")
def get_product(product: ProductCreate ,db: Session = Depends(get_db)):
    product_by_name = db.query(Product).filter(Product.name == product.name).first()
    return product_by_name