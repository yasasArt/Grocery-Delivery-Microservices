from fastapi import FastAPI
from database import Base, engine
from models.order import Order
from models.order_item import OrderItem
# from routers import order_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service",
    description="Order and address management microservice",
    version="1.0.0"
)

# app.include_router(order_router, prefix="/Orders", tags=["Orders"])


@app.get("/")
def health_check():
    return {
        "service": "Order-service",
        "status": "running"
    }