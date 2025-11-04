# docker build -f docker/Dockerfile -t mysite-dev .
# Stage 1
FROM python:3.13.7 AS builder

COPY ../requirements.txt .

RUN pip install --upgrade pip && pip install --user --no-cache-dir -r requirements.txt


# Install netcat for health checks / wait-for-db
# replaced with docker-compose healthy check
#RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Stage 2
FROM python:3.13.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY .. .

ENTRYPOINT ["bash", "/app/docker/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]


