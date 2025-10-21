# docker build -f docker/Dockerfile -t mysite-dev .
FROM python:3.13.7

WORKDIR /app

# Install netcat for health checks / wait-for-db
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY .. .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["bash", "/app/docker/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]


