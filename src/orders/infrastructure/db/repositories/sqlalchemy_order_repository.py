from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.orders.domain.entities.order import Order, OrderItem, OrderStatus
from src.orders.infrastructure.db.models.order_model import OrderItemModel, OrderModel


class SQLAlchemyOrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, order: Order) -> Order:
        model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            status=order.status.value,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                OrderItemModel(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in order.items
            ],
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        stmt = (
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.id == order_id)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, limit: int = 25, offset: int = 0) -> List[Order]:
        stmt = (
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()]

    async def update(self, order: Order) -> Order:
        model = await self._session.get(OrderModel, order.id)
        if model:
            model.status = order.status.value  # type: ignore[assignment]
            model.updated_at = order.updated_at  # type: ignore[assignment]
            await self._session.commit()
            await self._session.refresh(model)
        return order

    async def delete(self, order_id: UUID) -> bool:
        model = await self._session.get(OrderModel, order_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
            return True
        return False

    def _to_entity(self, model: OrderModel) -> Order:
        order = Order(
            id=UUID(str(model.id)),
            customer_id=UUID(str(model.customer_id)),
            customer_name=str(model.customer_name),
            status=OrderStatus(str(model.status)),
            created_at=datetime.fromisoformat(str(model.created_at)),
            updated_at=datetime.fromisoformat(str(model.updated_at)),
        )
        order.items = [
            OrderItem(
                id=UUID(str(item.id)),
                product_id=UUID(str(item.product_id)),
                product_name=str(item.product_name),
                quantity=int(str(item.quantity)),
                unit_price=float(str(item.unit_price)),
            )
            for item in model.items
        ]
        return order