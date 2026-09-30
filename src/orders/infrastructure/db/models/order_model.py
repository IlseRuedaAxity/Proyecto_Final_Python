import uuid
import uuid as uuid_module
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.types import CHAR, TypeDecorator


class UUIDType(TypeDecorator):
    """UUID compatible con SQLite"""

    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid_module.UUID(value)


class Base(DeclarativeBase):
    pass


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    order_id = Column(UUIDType, ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUIDType, nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("OrderModel", back_populates="items")


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUIDType, nullable=False)
    customer_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan", lazy="selectin"
    )
