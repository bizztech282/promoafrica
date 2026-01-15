#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- Building project ---"

echo "--- Upgrading pip ---"
python -m pip install --upgrade pip

echo "--- Installing dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static files ---"
# Ensure we use production settings for collectstatic to get the right storage/root
export DJANGO_SETTINGS_MODULE=app.settings.production
python manage.py collectstatic --noinput --clear

echo "--- Build complete ---"
