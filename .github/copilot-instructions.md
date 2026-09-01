# LAA Fee Calculator

Django 6 app with a PostgreSQL database in deployed/local Docker environments and SQLite for simple
local development. It calculates Legal Aid Agency Crown Court fee amounts for AGFS and LGFS schemes
and exposes the calculator through a Django REST Framework API, with Swagger documentation at
`/api/v1/docs/`.

## Build & test

Run commands from the repository root.

```sh
brew install pyenv
pyenv install 3.14.2
pyenv local 3.14.2
make setup-local
pipenv shell
make dbreload
make server
```

Useful checks:

```sh
pipenv run flake8
make test
pipenv run python3 manage.py test
pipenv run python3 manage.py test fee_calculator.apps.calculator.tests.test_calculation_05_agfs_12
pipenv run python3 -m coverage run manage.py test
pipenv run python3 -m coverage report
docker-compose build
docker-compose up
docker build --check .
```

- CI uses Python 3.14 and `pipenv sync --dev`.
- CI runs `pipenv run flake8`, shards calculator tests under
  `fee_calculator/apps/calculator/tests`, then runs viewer/API tests separately.
- Prefer focused Django test modules before running the full suite.
- Local Docker serves the app at port 8000 and maps to uWSGI on port 8080 in the container.
- Pre-commit hooks come from `ministryofjustice/devsecops-hooks`; install and run `prek install` /
  `prek run` per [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md).

## Architecture

- **Calculator app**: `fee_calculator/apps/calculator` owns fee scheme data, models, calculation
  behaviour, fixtures, management commands, and calculator tests.
- **API app**: `fee_calculator/apps/api` contains DRF serializers, filters, views, and URL routing
  for the versioned calculator API.
- **Viewer app**: `fee_calculator/apps/viewer` contains the lightweight browser UI, presenters,
  templates, static assets, and viewer tests.
- **Settings**: environment-specific Django settings live under `fee_calculator/settings`.
- **Deployment**: Kubernetes manifests live under `kubernetes_deploy`; the runtime image is built
  from `Dockerfile` and runs `uwsgi.ini` as a non-root user.

### Fee data and fixtures

- Core fee data is fixture-driven under `fee_calculator/apps/calculator/fixtures`.
- Price fixtures use names such as `price_14_agfs_17.json`; keep the existing naming pattern when
  adding schemes or prices.
- `scheme.json`, `feetype.json`, `scenario.json`, `unit.json`, `modifier.json`, `modifiertype.json`,
  `offenceclass.json`, and `advocatetype.json` define the calculator reference data.
- `loadalldata.py` controls which fixtures are loaded; update it when adding a new price fixture.
- Management commands such as `copyscheme`, `copyfeetype`, `dumpprices`, `cleardata`, and
  `loadalldata` are the preferred tools for scheme and fee-type changes. See [README.md](../README.md)
  before editing fixture data manually.

### Deployment

- Build/deploy runs through `.github/workflows/ci_cd.yml`.
- A push to `main` builds and tags an image as `app-latest` after tests pass.
- Docker build arguments include `DJANGO_SECRET_KEY`, version, commit, build date, and build tag.
- Secrets are Kubernetes Secret objects and backed up externally; do not add secrets to the repo.
  See [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md).

## Conventions

- Use Pipenv for dependency and command execution; keep `Pipfile` and `Pipfile.lock` in sync.
- Python style is enforced with Flake8 in `setup.cfg`; max line length is 120 and migrations/settings
  paths are excluded.
- Do not edit generated migrations casually; calculator data changes usually happen through fixtures
  and management commands.
- Keep fee scheme dates contiguous when adding schemes: set the old scheme `end_date` and new scheme
  `start_date` together.
- After fixture changes, run `pipenv run python3 manage.py cleardata` and
  `pipenv run python3 manage.py loadalldata` before testing calculations.
- Commit messages should use British English. The title should be imperative and the body should use
  present tense. Filenames, code, and other technical references should be in backticks.
- Keep commits focused and preserve unrelated user changes. Do not rewrite history, commit, or push
  unless explicitly instructed by the user.
- When changing build, test, deployment, architecture, or major workflow conventions, update this
  file in the same PR if its guidance would become stale.

## Additional information

- Setup/runtime docs: [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md)
- API usage and fee scheme workflows: [README.md](../README.md)
- CI/CD workflow: [.github/workflows/ci_cd.yml](workflows/ci_cd.yml)
- Docker/local services: [Dockerfile](../Dockerfile), [docker-compose.yaml](../docker-compose.yaml),
  and [uwsgi.ini](../uwsgi.ini)
