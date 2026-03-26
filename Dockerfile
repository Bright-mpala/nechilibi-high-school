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

RUN chmod +x pre-deploy.sh

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=./config/wsgi.py

EXPOSE 8000

CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
