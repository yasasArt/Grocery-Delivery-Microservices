from fastapi import APIRouter, Depends, HTTPException, status
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
