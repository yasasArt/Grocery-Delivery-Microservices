from fastapi import APIRouter, HTTPException, Request
import httpx
from core.config import CUSTOMER_SERVICE_URL

router = APIRouter()


@router.post("/")
async def create_customer(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CUSTOMER_SERVICE_URL}/customers", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/")
async def get_all_customers():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/with-addresses/{customer_id}")
async def get_customer_with_addresses(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers/with-addresses/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.post("/{customer_id}/addresses")
async def add_customer_address(customer_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}/addresses",
            json=payload
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/{customer_id}/addresses")
async def get_customer_addresses(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}/addresses")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/{customer_id}")
async def get_customer_by_id(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.put("/{customer_id}")
async def update_customer(customer_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()