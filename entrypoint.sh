#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$DB_PASSWORD python manage.py createsuperuser --username $DB_USER --email $SUPER_USER_EMAIL --noinput

gunicorn sso_server.wsgi:application --bind 0.0.0.0:8000