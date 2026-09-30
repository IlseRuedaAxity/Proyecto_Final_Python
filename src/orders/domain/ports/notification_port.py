from typing import Protocol
from uuid import UUID


class NotificationPort(Protocol):
    """Puerto de salida: notificaciones externas"""

    async def notify_order_created(self, order_id: UUID, customer_name: str) -> None: ...

    async def notify_order_confirmed(self, order_id: UUID) -> None: ...
