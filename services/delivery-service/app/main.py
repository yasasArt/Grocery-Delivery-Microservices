from fastapi import FastAPI
from .db.database import Base, engine
from .models.delivery import Delivery
from .routers.delivery_routes import router as delivery_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delivery Service",
    description="Delivery management microservice",
    version="1.0.0"
)

app.include_router(delivery_router, prefix="/deliveries", tags=["Deliveries"])


@app.get("/")
def health_check():
    return {
        "service": "delivery-service",
        "status": "running"
    }