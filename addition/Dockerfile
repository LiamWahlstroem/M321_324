FROM python:3.13-rc-slim AS base
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m", "uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "5000"]
