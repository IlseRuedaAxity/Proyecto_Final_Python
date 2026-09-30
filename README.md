# Orders Service 🛒

Servicio de gestión de órdenes con Arquitectura Hexagonal/Limpia.

## Tecnologías
- **Python 3.14** + **FastAPI** + **SQLAlchemy** (async)
- **Alembic** para migraciones
- **JWT** para autenticación
- **Docker** multistage (sin root)
- **GitHub Actions** CI/CD
- **pytest** con 90% de cobertura

## Arquitectura
src/orders/
├── domain/ ← Entidades y puertos (interfaces)
├── application/ ← Casos de uso y DTOs
├── infrastructure/ ← Adaptadores (BD, HTTP)
└── api/ ← Routers FastAPI y esquemas Pydantic

## Levantar en local

```bash
poetry install
call ".venv\Scripts\activate.bat"
uvicorn src.orders.main:app --reload
Accede a la documentación: http://localhost:8000/docs

Endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/v1/auth/token | Obtener token JWT |
| POST | /api/v1/orders | Crear orden |
| GET | /api/v1/orders | Listar órdenes |
| GET | /api/v1/orders/{id} | Obtener orden |
| DELETE | /api/v1/orders/{id} | Eliminar orden |
| GET | /health | Health check |

Ejecutar pruebas
pytest --cov=src --cov-report=term-missing -v

Calidad de código
black src tests
python -m isort src tests
python -m ruff check src tests
python -m mypy src

Auditoría de seguridad
pip-audit

Migraciones
alembic revision --autogenerate -m "descripcion"
alembic upgrade head

Docker
docker build -t orders-service .
docker run -p 8000:8000 orders-service

Credenciales de prueba
Usuario: admin
Contraseña: admin123
```