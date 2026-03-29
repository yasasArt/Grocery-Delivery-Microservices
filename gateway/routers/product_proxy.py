from fastapi import APIRouter, HTTPException, Request
import httpx
from core.config import PRODUCT_SERVICE_URL

router = APIRouter()


@router.post("/")
async def create_product(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PRODUCT_SERVICE_URL}/products", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/")
async def get_all_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/available/list")
async def get_available_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/available/list")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/search")
async def search_products(q: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/search", params={"q": q})

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/category/{category_name}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.put("/{product_id}")
async def update_product(product_id: int, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{PRODUCT_SERVICE_URL}/products/{product_id}", json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()