from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeliveryCreate(BaseModel):
    order_id: int = Field(..., gt=0)
    rider_name: str = Field(..., min_length=2, max_length=100)
    contact_number: str = Field(..., min_length=8, max_length=20)
    estimated_time: Optional[str] = Field(default=None, max_length=50)
    delivery_address: str = Field(..., min_length=5, max_length=255)


class DeliveryStatusUpdate(BaseModel):
    delivery_status: str = Field(..., min_length=3, max_length=30)


class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    rider_name: str
    contact_number: str
    delivery_status: str
    estimated_time: Optional[str]
    delivery_address: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True