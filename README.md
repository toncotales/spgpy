# spgpy

**S**ecure **P**assword **G**enerator for **Py**thon.

A modular Python password generator that uses Python's `secrets` module for cryptographically secure randomness.

## Features

- Command-line interface and Python API.
- Configurable password length (12 to 128 characters).
- Every password has at least 2 uppercase letters, 2 lowercase letters, 2 digits and 2 punctuation characters.
- Optional "no duplicates" mode: no character appears twice.
- Optional "alternate case" mode: no two neighbouring characters are of the same type.
- Safe punctuation by default; optionally use all punctuation.
- Password validation.
- Automated tests using `unittest`.

## Requirements

- Python 3.10 or newer.

## Installation

```bash
pip install spgpy
```

After installation, the `spgpy` command is available:

```bash
spgpy
```

You can also run the package directly:

```bash
python -m spgpy
```

## Command-line usage

Generate one password using the defaults:

```bash
spgpy
```

Generate a 24-character password:

```bash
spgpy --length 24
```

Generate three passwords:

```bash
spgpy --count 3
```

Use all punctuation characters:

```bash
spgpy --use-all-punctuation
```

Never repeat a character:

```bash
spgpy --no-duplicates
```

Never put two characters of the same type next to each other:

```bash
spgpy --alternate-case
```

Combine options:

```bash
spgpy --length 24 --count 5 --alternate-case --no-duplicates
```

See all options:

```bash
spgpy --help
```

| Option | Short | Description |
| --- | --- | --- |
| `--length N` | `-l` | Password length, 12 to 128 (default 16). |
| `--count N` | `-n` | Number of passwords, 1 to 1000 (default 1). |
| `--use-all-punctuation` | `-a` | Include every punctuation character. |
| `--alternate-case` | `-t` | No two adjacent characters of the same type. |
| `--no-duplicates` | `-d` | No character is used twice. |
| `--version` | `-V` | Show the version. |

By default these punctuation characters are left out because they often cause trouble in shells, URLs and config files: `' " \ / ` < > [ ] { } ( ) . , : ; + = ~ ^ |`.

## Python API

```python
from spgpy import PasswordGenerator

generator = PasswordGenerator(length=24, alternate_case=True)

password = generator.generate()
print(password)

print(generator.generate_many(3))
print(PasswordGenerator.is_valid_password(password, alternate_case=True))
```

Settings can be changed later and are checked each time:

```python
generator.length = 32
generator.no_duplicates = True
generator.set_excluded_punctuation("!?")
```

Invalid settings raise `TypeError` or `ValueError`. Settings that cannot produce a password (for example `no_duplicates=True` with a very long `length`) raise `ValueError` from `generate()`.

## Upgrading from 1.x

Version 2.0.0 replaces the 1.x API.

| 1.x | 2.0 |
| --- | --- |
| `PasswordPolicy(length=24, all_symbols=True, alternate_types=True)` | `PasswordGenerator(length=24, use_all_punctuation=True, alternate_case=True)` |
| `generate_password(policy)` | `generator.generate()` |
| `is_password_strong(pw, alternate_types=True)` | `PasswordGenerator.is_valid_password(pw, alternate_case=True)` |
| `--all-symbols` | `--use-all-punctuation` |
| `--alternate-types` | `--alternate-case` |
| `--validate PASSWORD` | Removed. Use `is_valid_password()` in Python. |

See [CHANGELOG.md](CHANGELOG.md) for the full list of changes.

## Testing

Run the complete test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

## Security note

The generator uses `secrets.choice()` and `secrets.SystemRandom()` rather than the ordinary `random` module. This is appropriate for generating passwords intended for security-sensitive use.

Using `no_duplicates` slightly reduces the number of possible passwords, because characters cannot repeat.

No password is stored by the application.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
