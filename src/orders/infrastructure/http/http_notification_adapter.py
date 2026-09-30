import logging
from uuid import UUID

import httpx

logger = logging.getLogger(__name__)


class HttpNotificationAdapter:
    def __init__(self, client: httpx.AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url

    async def notify_order_created(self, order_id: UUID, customer_name: str) -> None:
        try:
            await self._client.post(
                f"{self._base_url}/notifications",
                json={
                    "event": "order_created",
                    "order_id": str(order_id),
                    "customer": customer_name,
                },
                timeout=5.0,
            )
        except httpx.RequestError as e:
            logger.warning(f"Notificación fallida para order {order_id}: {e}")

    async def notify_order_confirmed(self, order_id: UUID) -> None:
        try:
            await self._client.post(
                f"{self._base_url}/notifications",
                json={"event": "order_confirmed", "order_id": str(order_id)},
                timeout=5.0,
            )
        except httpx.RequestError as e:
            logger.warning(f"Notificación fallida para order {order_id}: {e}")
