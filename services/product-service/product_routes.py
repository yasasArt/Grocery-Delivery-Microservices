from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from product_schema import ProductCreate, ProductUpdate, ProductResponse
from product_service import *

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/", response_model=list[ProductResponse])
def get_all_products_endpoint(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/available-list", response_model=list[ProductResponse])
def get_available_products_endpoint(db:Session =Depends(get_db)):
    return get_available_products(db)

@router.get("/search", response_model=list[ProductResponse])
def search_products_endpoint(
    q: str = Query(..., min_length=1, description="Search keyword for product name"),
    db: Session = Depends(get_db)):

    return search_products(db, q)

@router.get("/category/{category_name}", response_model=list[ProductResponse])
def get_products_by_category_endpoint(category_name: str, db: Session = Depends(get_db)):
    return get_products_by_category(db, category_name)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int, 
    product_data: ProductUpdate,
    db: Session = Depends(get_db)):

    updated_product = update_product(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
