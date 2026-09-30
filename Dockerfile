# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install poetry==2.5.1
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-root

# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Usuario sin root — seguridad
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini* ./

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.orders.main:app", "--host", "0.0.0.0", "--port", "8000"]