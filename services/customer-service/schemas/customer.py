from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from schemas.address import AddressResponse


class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=8, max_length=20)


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=8, max_length=20)


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerWithAddressesResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime
    addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True