#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# create superuser if not exists
python manage.py createsuperuser --no-input

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000