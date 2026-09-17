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

## Release

Tag `v*` on `main` to build with `uv`, create a GitHub release, and publish to PyPI via trusted publishing.

1. Move `[Unreleased]` notes in `CHANGELOG.md` under a dated version heading.
2. Bump `version` in `pyproject.toml`.
3. Merge to `main`, then `git tag -a vX.Y.Z -m "Release vX.Y.Z"` and push the tag.
4. Configure the GitHub `release` environment and a PyPI trusted publisher for this workflow before the first publish.

## Pull requests

1. Branch from `main`.
2. Keep the change scoped; add or update tests with the behavior change.
3. Add a `CHANGELOG.md` entry under `[Unreleased]`.
4. Open a PR. GitHub Actions must be green.
