from fastapi import FastAPI
from database import Base, engine
from models.product_model import Product
from product_routes import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service",
    description="Product catalog management microservice",
    version="1.0.0"
)

app.include_router(
    product_router,
    prefix="/products",
    tags=["Products"]
)

@app.get("/")
def health_check():
    return {
        "service": "product-service",
        "status": "running"
    }
