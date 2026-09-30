from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = "sqlite+aiosqlite:///./orders.db"

    # JWT
    SECRET_KEY: str = "cambia-esto-en-produccion-usa-variable-de-entorno"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Notificaciones
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8001"

    # App
    APP_NAME: str = "Orders Service"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
