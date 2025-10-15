FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY src/ ./src
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --no-cache
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "./src/main.py"]