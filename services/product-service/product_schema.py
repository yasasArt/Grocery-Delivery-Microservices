from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    category: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    is_available: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=3, max_length=255)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    stock_quantity: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True