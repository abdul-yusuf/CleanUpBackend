#!/bin/bash
python3 manage.py collectstatic --noinput

gunicorn --env DJANGO_SETTINGS_MODULE=CleanUpBackend.settings CleanUpBackend.wsgi:application --bind 0.0.0.0:8080