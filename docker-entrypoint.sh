#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate 

# Start Gunicorn processes
echo Starting Gunicorn.

celery -A config worker -l info & celery -A config beat -l info &
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gevent \
    --timeout 200 \
    "$@"

