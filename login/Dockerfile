FROM python:3.13-rc-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn aio-pika pydantic

EXPOSE 5000

CMD python3 -m uvicorn login_service:app --host 0.0.0.0 --port 5000
