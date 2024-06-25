pr=pipenv run
py=python3
man=manage.py
pyman=${py} ${man}

default: help

help: #: Show help topics
	@grep "#:" Makefile* | grep -v "@grep" | sort | sed "s/\([A-Za-z_ -]*\):.*#\(.*\)/$$(tput setaf 3)\1$$(tput sgr0)\2/g"

setup: #: Install virtual environment and requirements
	pip3 install pipenv
	pipenv shell
	pipenv install
setup-local: #: Install virtual environment and requirements for local development environment
	pip3 install pipenv
	pipenv shell
	pipenv install --dev
server: # run app server
	DEBUG="True" ${pr} ${pyman} runserver 8000
db: #: open db console
	sqlite3 fee_calculator/db.sqlite3
dbreload: #: migrate, clear and load data
	${pr} ${pyman} migrate
	${pr} ${pyman} cleardata
	${pr} ${pyman} loadalldata
dbreset: #: clear data and drop app tables
	${pr} ${pyman} flush --no-input
	${pr} ${pyman} migrate calculator zero
test: #: run test suite
	${pr} ${py} -m coverage run ${man} test --verbosity=1 --noinput
	${pr} ${py} -m coverage report
