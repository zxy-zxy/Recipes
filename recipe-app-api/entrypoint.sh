#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z recipes-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate

echo "Migrations complete"

python manage.py runserver 0.0.0.0:8000