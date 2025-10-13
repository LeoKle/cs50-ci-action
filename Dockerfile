FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY src/ ./src
COPY pyproject.toml .

RUN uv sync

ENTRYPOINT ["python", "./src/main.py"]