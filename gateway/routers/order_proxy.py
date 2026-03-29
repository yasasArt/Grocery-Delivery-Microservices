from fastapi import APIRouter, HTTPException, Request
import httpx
from core.config import ORDER_SERVICE_URL

router = APIRouter()


@router.post("/carts")
async def create_cart(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ORDER_SERVICE_URL}/carts", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/carts/{customer_id}")
async def get_cart(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/carts/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.post("/carts/{customer_id}/items")
async def add_item_to_cart(customer_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ORDER_SERVICE_URL}/carts/{customer_id}/items",
            json=payload
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.put("/carts/{customer_id}/items/{product_id}")
async def update_cart_item(customer_id: int, product_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{ORDER_SERVICE_URL}/carts/{customer_id}/items/{product_id}",
            json=payload
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.delete("/carts/{customer_id}/items/{product_id}")
async def delete_cart_item(customer_id: int, product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{ORDER_SERVICE_URL}/carts/{customer_id}/items/{product_id}"
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.post("/orders/place/{customer_id}")
async def place_order(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ORDER_SERVICE_URL}/orders/place/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/orders")
async def get_all_orders():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/orders/customer/{customer_id}")
async def get_orders_by_customer(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/customer/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/orders/{order_id}")
async def get_order_by_id(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()