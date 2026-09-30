from typing import List, Optional, Protocol
from uuid import UUID

from src.orders.domain.entities.order import Order


class OrderRepositoryPort(Protocol):
    """Puerto de salida: define cómo persistir Orders"""

    async def save(self, order: Order) -> Order: ...

    async def get_by_id(self, order_id: UUID) -> Optional[Order]: ...

    async def get_all(self, limit: int = 25, offset: int = 0) -> List[Order]: ...

    async def update(self, order: Order) -> Order: ...

    async def delete(self, order_id: UUID) -> bool: ...
