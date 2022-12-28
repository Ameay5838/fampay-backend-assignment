#!/bin/sh

echo "Apply database migrations"
python manage.py migrate

# create superuser if not exists
echo "Create super user"
python manage.py createsuperuser --no-input --username ganesh --email ganesh@ganesh.com

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000