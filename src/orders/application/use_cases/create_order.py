from src.orders.application.dtos.order_dtos import CreateOrderDTO, OrderResponseDTO
from src.orders.domain.entities.order import Order, OrderItem
from src.orders.domain.ports.notification_port import NotificationPort
from src.orders.domain.ports.order_repository import OrderRepositoryPort


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepositoryPort,
        notification: NotificationPort,
    ) -> None:
        self._repository = repository
        self._notification = notification

    async def execute(self, dto: CreateOrderDTO) -> OrderResponseDTO:
        order = Order(
            customer_id=dto.customer_id,
            customer_name=dto.customer_name,
        )

        for item_dto in dto.items:
            item = OrderItem(
                product_id=item_dto.product_id,
                product_name=item_dto.product_name,
                quantity=item_dto.quantity,
                unit_price=item_dto.unit_price,
            )
            order.add_item(item)

        saved_order = await self._repository.save(order)

        await self._notification.notify_order_created(
            order_id=saved_order.id,
            customer_name=saved_order.customer_name,
        )

        return OrderResponseDTO(
            id=saved_order.id,
            customer_id=saved_order.customer_id,
            customer_name=saved_order.customer_name,
            status=saved_order.status.value,
            total=saved_order.total(),
            items_count=len(saved_order.items),
        )
