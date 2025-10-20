# docker build -f docker/Dockerfile -t mysite-dev .
FROM python:3.13.7

WORKDIR /app

COPY .. .
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["docker/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]


