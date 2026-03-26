#!/bin/bash
set -e

python manage.py migrate --noinput --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
