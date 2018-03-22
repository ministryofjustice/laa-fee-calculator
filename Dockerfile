FROM buildpack-deps:xenial

# setup environment
RUN apt-get update && apt-get install -y --no-install-recommends locales tzdata
RUN set -ex; echo en_GB.UTF-8 UTF-8 > /etc/locale.gen && locale-gen
ENV LANG=en_GB.UTF-8
ENV TZ=Europe/London
ARG SECRET_KEY
#ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_SECRET_KEY=$SECRET_KEY
RUN timedatectl set-timezone Europe/London || true

# install libraries
RUN apt-get install -y --no-install-recommends software-properties-common build-essential rsync gettext python3-all-dev python3-venv

# pre-create directories
WORKDIR /app

# install virtual environment
RUN /usr/bin/python3 -m venv venv
RUN venv/bin/pip install -U setuptools pip wheel

# cache python packages, unless requirements change
ADD ./requirements requirements
RUN venv/bin/pip install -r requirements/base.txt

# add app
ADD . /app

# run uwsgi on 8080
EXPOSE 8080
ENV DJANGO_SETTINGS_MODULE=fee_calculator.settings.docker

# need secret_key env var here
RUN venv/bin/python manage.py collectstatic
CMD venv/bin/python manage.py migrate --no-input && venv/bin/uwsgi --ini uwsgi.ini
