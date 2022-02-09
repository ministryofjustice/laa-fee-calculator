px=venv/bin/pip
pyman=venv/bin/python manage.py

default: help

help: #: Show help topics
	@grep "#:" Makefile* | grep -v "@grep" | sort | sed "s/\([A-Za-z_ -]*\):.*#\(.*\)/$$(tput setaf 3)\1$$(tput sgr0)\2/g"

setup: #: Install virtual environment and requirements
	`which python3` -m venv venv
	${px} install -U setuptools pip wheel
	${px} install -r requirements/base.txt
reload: #: migrate, clear and load data
	${pyman} migrate
	${pyman} cleardata
	${pyman} loadalldata
server:
	DEBUG="True" ${pyman} runserver 8000
test:
	${pyman} test --verbosity=1 --noinput
