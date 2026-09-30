from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.orders.infrastructure.db.models.order_model import Base


def create_engine(database_url: str):
    return create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
    )


def create_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
