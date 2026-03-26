from fastapi import FastAPI
from app.routers import auth, products, cart, orders
from app.database import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine) # startup code here
    yield
    # shutdown code here

app = FastAPI(lifespan=lifespan,title="E-commerce API", description="Backend API for an e-commerce platform with authentication, products, cart, and orders")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)