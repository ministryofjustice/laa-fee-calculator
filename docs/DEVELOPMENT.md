# Development

## Requirements

* Python 3

**NOTE:** Python 3.7 is not currently compatible with Django version in use [see here for more info](https://stackoverflow.com/a/48822656).

## OS Dependencies


* libxml2

```bash
# For Mac users with brew:
brew unlink libxml2
brew uninstall libxml2 --ignore-dependencies --force
brew install --with-python libxml2
brew link libxml2 --force
```

## Setup

* Install virtual environment

```
`which python3` -m venv venv
venv/bin/pip install -U setuptools pip wheel
```

* Install application dependencies

```
venv/bin/pip install -r requirements/base.txt
```

* Create/Migrate database

```
venv/bin/python manage.py migrate --no-input
```

* Seed database

```
venv/bin/python manage.py loadalldata
```

* reseed database
```
venv/bin/python manage.py migrate
venv/bin/python manage.py cleardata
venv/bin/python manage.py loadalldata
```

* Run the server

By default bounds to port 8080

```
DEBUG="True" venv/bin/python manage.py runserver 8000
```

* Run test suite

```
cd laa-fee-calculator
venv/bin/python manage.py test
```

or, using pyenv
```
cd laa-fee-calculator
pyenv activate laa-fee-calculator
./manage.py test
```

run individual test
```
venv/bin/python manage.py test calculator.tests.test_calculation_agfs_12
```


## Running locally using docker

Tested using:
```
Docker Desktop version 3.5.2
Docker version 20.10.7
docker-compose version 1.29.2
```

### build
```shell
docker-compose build
```

### run locally
```shell
docker-compose up
```

### Open interactive API (swagger) documentation
[localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

