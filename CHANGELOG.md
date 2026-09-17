# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `GCSManager.from_env()` to load service-account JSON from a named environment variable.
- Optional extras: `images` (Pillow) and `mongo` (pymongo).
- Typed package marker (`py.typed`) and a `src/` layout.
- GitHub Actions CI: ruff, mypy, bandit, pip-audit, and pytest on Python 3.10–3.12.

### Changed
- Packaging uses uv and PEP 621 (`pyproject.toml` + `uv.lock`) instead of Poetry.
- `find_files(..., verbose=True)` replaces the `print` argument that shadowed the builtin.
- `from_json_file` takes a file path; `from_json_string` takes JSON content.
- `create_bucket` is keyword-only and defaults to a private bucket (`public=False`).
- Missing buckets raise `google.cloud.exceptions.NotFound`; missing local files raise `FileNotFoundError`.
- Supported Python range is `^3.10` (Pillow 12 and python-dotenv 1.2 require it).

### Fixed
- `make dump_key` runs `uv run mgs-dump-key` instead of a missing repo-root script.

### Removed
- Unused `pydantic` dependency.
- Unused `GCSManagerInterface`, `BucketExistsDecorator`, and the extra `BucketManager` client on `GCSManager`.

### Security
- New buckets are private unless `public=True` is passed.
- Pillow 12.3 and python-dotenv 1.2.2+ close previously reported CVEs on the old pins.

## [0.1.0] - 2024-10-04

### Added
- Initial `GCSManager`, credential helpers, and the `mgs-dump-key` CLI.

[Unreleased]: https://github.com/MonumentoSoftware/monugstore/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MonumentoSoftware/monugstore/releases/tag/v0.1.0
