from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    product_id: UUID
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderIn(BaseModel):
    customer_id: UUID
    customer_name: str = Field(..., min_length=1, max_length=255)
    items: List[OrderItemIn] = Field(..., min_length=1)


class OrderItemOut(BaseModel):
    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: UUID
    customer_id: UUID
    customer_name: str
    status: str
    total: float
    items_count: int

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    data: List[OrderOut]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    errorCode: str
    errorMessage: str
    userError: str
    info: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
