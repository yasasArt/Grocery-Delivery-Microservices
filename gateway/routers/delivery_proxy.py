from fastapi import APIRouter, HTTPException, Request
import httpx
from core.config import DELIVERY_SERVICE_URL

router = APIRouter()


@router.post("/")
async def create_delivery(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DELIVERY_SERVICE_URL}/deliveries", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/")
async def get_all_deliveries():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DELIVERY_SERVICE_URL}/deliveries")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/order/{order_id}")
async def get_delivery_by_order(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DELIVERY_SERVICE_URL}/deliveries/order/{order_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/{delivery_id}")
async def get_delivery_by_id(delivery_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DELIVERY_SERVICE_URL}/deliveries/{delivery_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.put("/{delivery_id}/status")
async def update_delivery_status(delivery_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DELIVERY_SERVICE_URL}/deliveries/{delivery_id}/status",
            json=payload
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()