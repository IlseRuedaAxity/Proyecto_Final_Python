from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.orders.api.dependencies import engine, http_client
from src.orders.api.routers import auth_router, orders_router
from src.orders.config import settings
from src.orders.infrastructure.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db(engine)
    yield
    # Shutdown
    await engine.dispose()
    await http_client.aclose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Servicio de Orders con Arquitectura Hexagonal/Limpia",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(orders_router.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}


if __name__ == "__main__":
    uvicorn.run("src.orders.main:app", host="0.0.0.0", port=8000, reload=True)
