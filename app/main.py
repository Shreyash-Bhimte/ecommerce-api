from fastapi import FastAPI
from app.routers import auth, products, cart, orders, pages
from app.database import Base, engine
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine) # startup code here
    yield
    # shutdown code here

app = FastAPI(lifespan=lifespan,title="E-commerce API", description="Backend API for an e-commerce platform with authentication, products, cart, and orders")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router, prefix="/auth")
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(pages.router)