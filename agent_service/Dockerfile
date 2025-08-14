FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for ML packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv pip install --system -e .

COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 8005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]