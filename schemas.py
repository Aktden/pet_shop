from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: float = Field(..., ge=0)
    in_stock: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True