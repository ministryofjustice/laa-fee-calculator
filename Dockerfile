FROM python:3.5-alpine as baseimg
RUN apk add --no-cache ca-certificates postgresql-dev build-base linux-headers
RUN pip install -U setuptools pip wheel
ARG SECRET_KEY
ENV DJANGO_SECRET_KEY=$SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=fee_calculator.settings.docker

WORKDIR /app
ADD requirements/base.txt /app/requirements/base.txt
RUN pip install -r requirements/base.txt

ADD . /app
RUN python manage.py collectstatic

FROM python:3.5-alpine as deployimg
RUN apk add --no-cache ca-certificates postgresql-dev uwsgi-python bash
COPY --from=baseimg /app /app
COPY --from=baseimg /usr/local/lib/python3.5 /usr/local/lib/python3.5
WORKDIR /app
ENTRYPOINT python manage.py loaddata advocatetype feetype offenceclass price scenario scheme unit modifier modifiertype && python manage.py migrate --no-input && uwsgi --ini uwsgi.ini
