# Contributing

## Setup

```bash
git clone https://github.com/MonumentoSoftware/monugstore.git
cd monugstore
poetry install --with dev --extras "images mongo"
```

Requires Python 3.10+.

## Checks

Run the same gates CI runs:

```bash
poetry run ruff check src tests
poetry run mypy src
poetry run bandit -r src
poetry run pip-audit
poetry run pytest
```

Pytest fails the run if coverage of `monugstore` is under 85%.

## Pull requests

1. Branch from `main`.
2. Keep the change scoped; add or update tests with the behavior change.
3. Add a `CHANGELOG.md` entry under `[Unreleased]`.
4. Open a PR. GitHub Actions must be green.
