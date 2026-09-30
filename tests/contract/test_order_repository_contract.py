from uuid import uuid4

from src.orders.domain.entities.order import Order, OrderItem
from src.orders.infrastructure.db.repositories.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)


async def test_save_and_get_order(test_session):
    repo = SQLAlchemyOrderRepository(test_session)
    order = Order(customer_id=uuid4(), customer_name="Test Contract")
    order.add_item(OrderItem(product_id=uuid4(), product_name="Prod", quantity=2, unit_price=15.0))

    saved = await repo.save(order)
    fetched = await repo.get_by_id(saved.id)

    assert fetched is not None
    assert fetched.customer_name == "Test Contract"
    assert len(fetched.items) == 1


async def test_delete_order(test_session):
    repo = SQLAlchemyOrderRepository(test_session)
    order = Order(customer_id=uuid4(), customer_name="To Delete")
    order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=1, unit_price=1.0))
    saved = await repo.save(order)

    result = await repo.delete(saved.id)
    assert result is True

    fetched = await repo.get_by_id(saved.id)
    assert fetched is None


async def test_get_all_orders(test_session):
    repo = SQLAlchemyOrderRepository(test_session)
    order = Order(customer_id=uuid4(), customer_name="Lista Test")
    order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=1, unit_price=5.0))
    await repo.save(order)

    orders = await repo.get_all(limit=10, offset=0)
    assert len(orders) >= 1
