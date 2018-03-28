FROM python:3.5-alpine as baseimg
RUN apk add --no-cache ca-certificates postgresql-dev build-base linux-headers
RUN pip install -U setuptools pip wheel
ARG SECRET_KEY
ENV DJANGO_SECRET_KEY=$SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=fee_calculator.settings.docker

ADD . /app
WORKDIR /app
RUN pip install -r requirements/base.txt
RUN python manage.py collectstatic

FROM python:3.5-alpine as deployimg
RUN apk add --no-cache ca-certificates postgresql-dev uwsgi-python bash
COPY --from=baseimg /app /app
COPY --from=baseimg /usr/local/lib/python3.5 /usr/local/lib/python3.5
WORKDIR /app
CMD python manage.py migrate --no-input && uwsgi --ini uwsgi.ini
