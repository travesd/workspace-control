FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    "duckdb>=1.1,<2" \
    "psycopg[binary]>=3.2,<4" \
    "pyarrow>=16,<23"

WORKDIR /workspace

