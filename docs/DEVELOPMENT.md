# Development

### Requirements

* Python 3

### OS Dependencies

* Postgresql

**NOTE:** Ensure after installation the `postgres` role exists

```
> psql postgres
Type "help" for help.

postgres=# \du
                                     List of roles
   Role name   |                         Attributes                         | Member of
---------------+------------------------------------------------------------+-----------
 postgres      | Superuser, Create role, Create DB                          | {}
```

If it doesn't exist you will need to create one.
```
# For Mac users (prepend sudo if necessary):
createuser -s postgres
```

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

* Create database

```
> psql postgres
postgres=# CREATE DATABASE fee_calculator WITH OWNER postgres ENCODING 'utf-8';
CREATE DATABASE
```

* Migrate database

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
