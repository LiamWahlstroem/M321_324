FROM python:3.13-rc-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 user_management_service.py
