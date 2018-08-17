#!/bin/bash

# Install packages for local
pip3 install -r requirements/local.txt

# Set environment for local
export DJANGO_SETTINGS_MODULE=config.settings.local

# Prepare database
python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', 'admin@example.com', 'adminpass');"

# Start runserver
python3 manage.py runserver 0.0.0.0:8000
