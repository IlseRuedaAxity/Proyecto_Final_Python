from uuid import uuid4

import pytest

from src.orders.domain.entities.order import Order, OrderItem, OrderStatus


def test_order_total_calculates_correctly():
    order = Order(customer_id=uuid4(), customer_name="Cliente Test")
    item1 = OrderItem(product_id=uuid4(), product_name="Prod A", quantity=2, unit_price=10.0)
    item2 = OrderItem(product_id=uuid4(), product_name="Prod B", quantity=1, unit_price=5.5)
    order.add_item(item1)
    order.add_item(item2)
    assert order.total() == 25.5


def test_order_confirm_changes_status():
    order = Order(customer_id=uuid4(), customer_name="Test")
    order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=1, unit_price=1.0))
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_order_cannot_confirm_empty_order():
    order = Order(customer_id=uuid4(), customer_name="Test")
    with pytest.raises(ValueError, match="sin items"):
        order.confirm()


def test_order_cannot_confirm_if_already_confirmed():
    order = Order(customer_id=uuid4(), customer_name="Test")
    order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=1, unit_price=1.0))
    order.confirm()
    with pytest.raises(ValueError):
        order.confirm()


def test_order_item_invalid_quantity():
    with pytest.raises(ValueError, match="cantidad"):
        order = Order(customer_id=uuid4(), customer_name="Test")
        order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=0, unit_price=10.0))


def test_order_cancel():
    order = Order(customer_id=uuid4(), customer_name="Test")
    order.cancel()
    assert order.status == OrderStatus.CANCELLED


def test_order_cannot_cancel_delivered():
    order = Order(customer_id=uuid4(), customer_name="Test")
    order.add_item(OrderItem(product_id=uuid4(), product_name="P", quantity=1, unit_price=1.0))
    order.confirm()
    order.deliver()
    with pytest.raises(ValueError):
        order.cancel()
