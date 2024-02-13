px=venv/bin/pip
py=venv/bin/python
man=manage.py
pyman=${py} ${man}

default: help

help: #: Show help topics
	@grep "#:" Makefile* | grep -v "@grep" | sort | sed "s/\([A-Za-z_ -]*\):.*#\(.*\)/$$(tput setaf 3)\1$$(tput sgr0)\2/g"

setup: #: Install virtual environment and requirements
	`which python3` -m venv venv
	${px} install -U setuptools pip wheel
	${px} install -r requirements/base.txt
setup-local: #: Install virtual environment and requirements for local development environment
	`which python3` -m venv venv
	${px} install -U setuptools pip wheel
	${px} install -r requirements/local.txt
server: # run app server
	DEBUG="True" ${pyman} runserver 8000
db: #: open db console
	sqlite3 fee_calculator/db.sqlite3
dbreload: #: migrate, clear and load data
	${pyman} migrate
	${pyman} cleardata
	${pyman} loadalldata
dbreset: #: clear data and drop app tables
	${pyman} flush --no-input
	${pyman} migrate calculator zero
test: #: run test suite
	${py} -m coverage run ${man} test --verbosity=1 --noinput
	${py} -m coverage report
