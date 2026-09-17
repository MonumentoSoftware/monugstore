# Contributing

## Setup

```bash
git clone https://github.com/MonumentoSoftware/monugstore.git
cd monugstore
uv sync --all-extras
```

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

## Checks

Run the same gates CI runs:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src
uv run bandit -r src
uv run pip-audit
uv run pytest
```

Pytest fails the run if coverage of `monugstore` is under 85%.

## Pull requests

1. Branch from `main`.
2. Keep the change scoped; add or update tests with the behavior change.
3. Add a `CHANGELOG.md` entry under `[Unreleased]`.
4. Open a PR. GitHub Actions must be green.
