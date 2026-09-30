from typing import Optional
from uuid import UUID

from src.orders.application.dtos.order_dtos import OrderResponseDTO
from src.orders.domain.ports.order_repository import OrderRepositoryPort


class GetOrderUseCase:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        order = await self._repository.get_by_id(order_id)
        if not order:
            return None

        return OrderResponseDTO(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            status=order.status.value,
            total=order.total(),
            items_count=len(order.items),
        )
