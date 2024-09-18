FROM python:3.13-rc-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir aio-pika bcrypt tinydb

EXPOSE 5000

CMD python3 user_management_service.py
