from typing import AsyncGenerator

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.application.use_cases.create_order import CreateOrderUseCase
from src.orders.application.use_cases.get_order import GetOrderUseCase
from src.orders.config import settings
from src.orders.infrastructure.db.database import create_engine, create_session_factory
from src.orders.infrastructure.db.repositories.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.orders.infrastructure.http.http_notification_adapter import HttpNotificationAdapter

engine = create_engine(settings.DATABASE_URL)
session_factory = create_session_factory(engine)
http_client = httpx.AsyncClient()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def get_order_repository(session: AsyncSession = Depends(get_db_session)):
    return SQLAlchemyOrderRepository(session)


def get_notification_adapter():
    return HttpNotificationAdapter(http_client, settings.NOTIFICATION_SERVICE_URL)


def get_create_order_use_case(
    repo=Depends(get_order_repository),
    notif=Depends(get_notification_adapter),
):
    return CreateOrderUseCase(repo, notif)


def get_get_order_use_case(repo=Depends(get_order_repository)):
    return GetOrderUseCase(repo)
