from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: int
    line_total: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: int
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True