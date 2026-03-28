FROM python:3.11-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# install build deps for C extensions (e.g. psutil on aarch64 when no wheel is available)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpython3.11-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY ./requirements-prod.txt .
COPY ./requirements.txt .
RUN pip install -r requirements-prod.txt

# copy project
COPY . .

# Copy seeded school images to media directory for Railway deployment
RUN mkdir -p /usr/src/app/media/gallery && \
    cp -r /usr/src/app/static/img/school/. /usr/src/app/media/gallery/ 2>/dev/null || true

RUN chmod +x pre-deploy.sh

# Run collectstatic at build time (uses dummy values since DB/secrets not needed for static files)
RUN SECRET_KEY=build-time-placeholder DATABASE_URL=sqlite:////tmp/build.db python manage.py collectstatic --noinput --settings=config.settings.production

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=./config/wsgi.py

EXPOSE 8000

CMD python manage.py migrate --noinput --settings=config.settings.production && python manage.py create_superuser_if_none --settings=config.settings.production && python manage.py seed_nechilibi --settings=config.settings.production && python manage.py seed_site --settings=config.settings.production && python manage.py seed_calendar --settings=config.settings.production && python manage.py seed_results --settings=config.settings.production && python manage.py seed_fees --settings=config.settings.production && python manage.py seed_subjects --settings=config.settings.production && python manage.py seed_sports --settings=config.settings.production && python manage.py seed_teachers --settings=config.settings.production && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
