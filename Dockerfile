FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN chmod +x startup.sh && ./startup.sh

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
