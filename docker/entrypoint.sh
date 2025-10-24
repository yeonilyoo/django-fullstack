#!/bin/bash

#replaced with docker compose healthy check
# Wait for MariaDB to be ready
#echo "Waiting for MariaDB to be ready..."
#until nc -z db 3306; do
#  sleep 1
#done
#echo "MariaDB is ready"


python manage.py migrate
python manage.py collectstatic --noinput
exec "$@"
