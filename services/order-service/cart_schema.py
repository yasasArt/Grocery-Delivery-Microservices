from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CartCreate(BaseModel):
    customer_id: int = Field(..., gt=0)


class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    items: List[CartItemResponse] = []

    class Config:
        from_attributes = True