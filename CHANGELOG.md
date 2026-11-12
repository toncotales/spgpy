# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-11-12

This release replaces the 1.x public API. See **Removed** and **Changed** for
what to update when upgrading from 1.0.0.

### Added

- `PasswordGenerator` class, the new main API. Settings (`length`,
  `no_duplicates`, `alternate_case`, `use_all_punctuation`) are validated
  properties and can be changed after the object is created.
- `PasswordGenerator.generate_many(count)` to create several passwords at once.
- `PasswordGenerator.set_excluded_punctuation()` and the
  `excluded_punctuation` property to choose which punctuation is left out.
- `PasswordGenerator.is_valid_password()` static method, with `alternate_case`
  and `no_duplicates` options.
- `no_duplicates` option and `-d` / `--no-duplicates` CLI flag: no character
  appears twice in a password.
- `CHANGELOG.md`.
- New unit tests for every module (90 tests).

### Changed

- **Breaking:** CLI flag `--all-symbols` is now `--use-all-punctuation`.
- **Breaking:** CLI flag `--alternate-types` is now `--alternate-case`.
- **Breaking:** `is_valid_password()` also checks the 128-character maximum.
- Code split into smaller modules: `arrangement`, `classifier`, `constants`,
  `entropy`, `generator`, `pools`, `sampling` and `validation`.
- All random choices go through `spgpy.entropy`, a thin wrapper over the
  `secrets` module.
- Sampling code reorganised into `_sample_unique` and `_sample_with_repeats`;
  the no-duplicates path no longer rebuilds its candidate list on every loop.
- `--length` help text shows balanced brackets and `--count` help shows its
  default.
- Code passes `flake8` and `mypy --strict`.
- README rewritten for the new API.

### Fixed

- Python 3.10 and 3.11 could not import the package because of Python 3.12-only
  syntax (`def choice[T]`) in the development code. It now uses `TypeVar`.
- `pyproject.toml` did not tell setuptools to look in `src/`, so the package
  could fail to build. Added `where = ["src"]`.
- Wrong argument names in the `build_punctuation_pool` docstring and a missing
  docstring for `build_character_pools`.
- Unused import and lost error context in `arrangement.py`.
- Return-type hints on `PasswordGenerator` methods.

### Removed

- **Breaking:** `PasswordPolicy`, `generate_password()` and
  `is_password_strong()`. Use `PasswordGenerator` and
  `PasswordGenerator.is_valid_password()` instead.
- **Breaking:** the `-v` / `--validate` CLI option.
- Modules `classify`, `policy`, `shuffle`, `symbols` and `validator`.

## [1.0.0]

- Initial release: `PasswordPolicy`, `generate_password()`,
  `is_password_strong()` and the `spgpy` command-line tool.

[2.0.0]: https://github.com/toncotales/spgpy/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/toncotales/spgpy/releases/tag/v1.0.0
