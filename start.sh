#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput --settings=MCart.settings

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 MCart.wsgi:application