from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    id: UUID = field(default_factory=uuid4)

    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    customer_id: UUID
    customer_name: str
    items: List[OrderItem] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def total(self) -> float:
        return round(sum(item.subtotal() for item in self.items), 2)

    def add_item(self, item: OrderItem) -> None:
        if item.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if item.unit_price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        self.items.append(item)

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"No se puede confirmar una orden en estado {self.status}")
        if not self.items:
            raise ValueError("No se puede confirmar una orden sin items")
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now(timezone.utc)

    def cancel(self) -> None:
        if self.status == OrderStatus.DELIVERED:
            raise ValueError("No se puede cancelar una orden entregada")
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)

    def deliver(self) -> None:
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Solo se pueden entregar órdenes confirmadas")
        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now(timezone.utc)
