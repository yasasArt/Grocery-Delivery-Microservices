from fastapi import FastAPI
from routers.product_proxy import router as product_proxy_router
from routers.customer_proxy import router as customer_proxy_router
from routers.order_proxy import router as order_proxy_router
from routers.delivery_proxy import router as delivery_proxy_router

app = FastAPI(
    title="API Gateway",
    description="Gateway for Grocery Delivery Microservices",
    version="1.0.0"
)

app.include_router(product_proxy_router, prefix="/api/products", tags=["Gateway - Products"])
app.include_router(customer_proxy_router, prefix="/api/customers", tags=["Gateway - Customers"])
app.include_router(order_proxy_router, prefix="/api", tags=["Gateway - Orders"])
app.include_router(delivery_proxy_router, prefix="/api/deliveries", tags=["Gateway - Deliveries"])


@app.get("/")
def health_check():
    return {
        "service": "api-gateway",
        "status": "running"
    }