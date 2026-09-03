#!/usr/bin/env bash
# Stop execution if anything fails
set -e

# # Wait for the DB to be ready (Postgres might still be waking up)
# echo "Checking database connection..."
# ./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up!"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply migrations (The image HAS the new migration files inside it!)
echo "Running migrations..."
python manage.py migrate --noinput

# Start the actual web server
echo "Starting web server..."

if [[ "$ENV_STATE" == "production" ]]; then
    gunicorn django_blog_project.wsgi --workers $GUNICORN_WORKERS --forwarded-allow-ips "*"
else
    python manage.py runserver 0.0.0.0:8000
fi

exec "$@"  # executes whatever CMD (or runtime override)
