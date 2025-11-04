#!/bin/bash
set -e
#replaced with docker compose healthy check
# Wait for MariaDB to be ready
#echo "Waiting for MariaDB to be ready..."
#until nc -z db 3306; do
#  sleep 1
#done
#echo "MariaDB is ready"

#since python slim doesn't include mysqlclient
# apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

python manage.py migrate
python manage.py collectstatic --noinput
exec "$@"
