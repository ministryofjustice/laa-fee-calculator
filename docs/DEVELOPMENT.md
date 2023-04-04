# Development

## Requirements

* Python 3.10.x
* Django 3.2.x

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

---
**Quick start**

```
make setup
make dbreload
make server
```
---

Alternatively, these commands can be run individually to set up the service step-by-step:

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

* Run the test suite

```
venv/bin/python manage.py test
```

* Run the test suite and report on code coverage metrics

```
venv/bin/python -m coverage run manage.py test
venv/bin/python -m coverage report
```

* Run an individual test

```
venv/bin/python manage.py test calculator.tests.test_calculation_05_agfs_12
```

## Running locally using docker

Tested using:
* Docker Desktop version 4.4.2
* Docker version 20.10.12
* docker-compose version 1.29.2


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


### Secret management

Secrets should _not_ be kept in this repository. In the past `git-crypt` has been used to encrypt secrets within the repo however due to the difficulty of rotating the symmetric key used for encryption following a security breach, this approach has now been deprecated.

Secrets are held as Kubernetes Secret objects in the cluster. These can be accessed by executing 

```bash
kubectl -n laa-fee-calculator-<env> get secrets
```

when authenticated to the cluster to view a list of all secrets.

To view the contents of a Secret, execute:

```bash
kubectl -n laa-fee-calculator-<env> get secrets <secret-name> -o json
```

For more details on how to add or update Kubernetes Secrets, see the [Cloud Platform documentation](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/deploying-an-app/add-secrets-to-deployment.html#adding-a-secret-to-an-application).

Secrets are also held securely in a password management service. This provides redundancy in the event that a Kubernetes Secret is deleted from the cluster; it can be recreated using the data held in the backup.

There is no automatic syncing of secrets between these backups and Kubernetes. If secret data is added or changed in one, it must be manually reflected in the other. Please refer to this [Confluence document](https://dsdmoj.atlassian.net/wiki/spaces/CFP/pages/4273504650/Secrets+Strategy+Post+Git-Crypt#Where-We-Are-Storing-Secrets-Now) for more information.
