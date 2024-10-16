FROM python:3.13-rc-slim AS base
ENV PYTHONUNBUFFERED=1

RUN ["mkdir", "-p", "/etc/db"]
RUN ["touch", "/etc/db/db.json"]

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "user_management_service.py"]
