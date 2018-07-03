FROM buildpack-deps:xenial

ENV \
  LANG=en_GB.UTF-8 \
  TZ=Europe/London

ARG DJANGO_SECRET_KEY

# pre-create directories
WORKDIR /app

# setup environment
RUN \
  set -ex \
  && apt-get update \
  && apt-get install \
    -y \
    --no-install-recommends \
    locales \
    tzdata \
    software-properties-common \
    build-essential \
    rsync \
    gettext \
    python3-all-dev \
    python3-pip \
    libpq-dev \
    netcat \
  && echo en_GB.UTF-8 UTF-8 > /etc/locale.gen \
  && locale-gen \
  && timedatectl set-timezone Europe/London || true \
  && pip3 install -U setuptools pip wheel

# cache python packages, unless requirements change
ADD ./requirements requirements
RUN pip3 install -r requirements/base.txt

# add app
ADD . /app

# run uwsgi on 8080
EXPOSE 8080
ENV DJANGO_SETTINGS_MODULE=fee_calculator.settings.docker

RUN python3 manage.py migrate --no-input \
    && python3 manage.py loadalldata \
    && python3 manage.py collectstatic --no-input

CMD uwsgi --ini uwsgi.ini
