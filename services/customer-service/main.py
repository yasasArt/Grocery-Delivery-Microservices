from fastapi import FastAPI
from database import Base, engine
from models.customer import Customer
from models.address import Address
from routers.customer_routes import router as customer_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Service",
    description="Customer and address management microservice",
    version="1.0.0"
)

app.include_router(customer_router, prefix="/customers", tags=["Customers"])


@app.get("/")
def health_check():
    return {
        "service": "customer-service",
        "status": "running"
    }