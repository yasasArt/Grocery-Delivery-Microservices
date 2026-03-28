from pydantic import BaseModel, Field
from datetime import datetime


class AddressCreate(BaseModel):
    label: str = Field(..., min_length=2, max_length=50)
    address_line: str = Field(..., min_length=5, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)


class AddressResponse(BaseModel):
    id: int
    customer_id: int
    label: str
    address_line: str
    city: str
    postal_code: str
    created_at: datetime

    class Config:
        from_attributes = True