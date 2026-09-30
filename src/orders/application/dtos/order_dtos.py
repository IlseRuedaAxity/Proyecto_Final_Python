from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class CreateOrderItemDTO:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float


@dataclass
class CreateOrderDTO:
    customer_id: UUID
    customer_name: str
    items: List[CreateOrderItemDTO]


@dataclass
class OrderResponseDTO:
    id: UUID
    customer_id: UUID
    customer_name: str
    status: str
    total: float
    items_count: int
