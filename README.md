# spgpy

**S**ecure **P**assword **G**enerator for **Py**thon.

A modular Python password generator that uses Python's `secrets` module for cryptographically secure randomness.

## Features

- Command-line interface.
- Password strength validation.
- Configurable password length.
- Optional use of all punctuation symbols.
- Optional character-type alternation to avoid adjacent characters of the same type.
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

You can also run the package directly without installing the command-line entry point:

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

Use all punctuation symbols:

```bash
spgpy --all-symbols
```

Require adjacent characters to have different types:

```bash
spgpy --alternate-types
```

Combine options:

```bash
spgpy --length 24 --count 5 --alternate-types
```

Validate a password:

```bash
spgpy --validate 'Aa12!Bb34@Cc'
```

See all options:

```bash
spgpy --help
```

## Python API

```python
from spgpy import PasswordPolicy, generate_password, is_password_strong

policy = PasswordPolicy(
    length=24,
    alternate_types=True,
)

password = generate_password(policy)
print(password)
print(is_password_strong(password, alternate_types=True))
```

## Testing

Run the complete test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

## Security note

The generator uses `secrets.choice()` and `secrets.SystemRandom()` rather than the ordinary `random` module. This is appropriate for generating passwords intended for security-sensitive use.

No password is stored by the application.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
