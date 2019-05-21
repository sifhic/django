#!/usr/bin/env bash

set -e
set -o pipefail

export DJANGO_SETTINGS_MODULE=settings_local
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python ./manage.py reset_db --router=default --noinput

python manage.py makemigrations
python manage.py migrate



