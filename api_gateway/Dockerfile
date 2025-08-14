FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv pip install --system -e .

COPY . .
COPY docker-entrypoint.sh /docker-entrypoint.sh

ENV PYTHONPATH=/app/src

EXPOSE 8003

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]