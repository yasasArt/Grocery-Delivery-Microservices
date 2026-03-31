from fastapi import FastAPI
from database import Base, engine
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from routers.order_routes import router as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service",
    description="Cart and order management microservice",
    version="1.0.0"
)

app.include_router(order_router, tags=["Orders"])


@app.get("/")
def health_check():
    return {
        "service": "order-service",
        "status": "running"
    }