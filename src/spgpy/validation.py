from collections import Counter
from collections.abc import Iterable

from .classifier import classify_character
from .constants import (
    MINIMUM_LENGTH,
    MAXIMUM_LENGTH,
    MINIMUM_PER_TYPE,
    CHARACTER_POOLS,
    SPECIAL_CHARACTER,
    MAXIMUM_GENERATION_COUNT,
)


def validate_length(length: int) -> None:
    """Validate that length is an integer within the allowed range."""
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("length must be an integer.")

    if not MINIMUM_LENGTH <= length <= MAXIMUM_LENGTH:
        raise ValueError(
            f"length must be between {MINIMUM_LENGTH} "
            f"and {MAXIMUM_LENGTH} characters."
        )


def validate_boolean(name: str, value: bool) -> None:
    """Validate the given value is a boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean.")


def validate_excluded_punctuation(
    punctuation_characters: Iterable[str],
) -> frozenset[str]:
    """Validate and return excluded punctuation characters as a frozenset."""
    try:
        items = list(punctuation_characters)
    except TypeError:
        raise TypeError("punctuation_characters must be iterable.") from None

    if any(not isinstance(item, str) or len(item) != 1 for item in items):
        raise ValueError(
            "punctuation_characters must contain single characters."
        )

    if any(
        item not in CHARACTER_POOLS["PUNCTUATION"] for item in items
    ):
        raise ValueError(
            "punctuation_characters must only contain punctuation characters."
        )

    return frozenset(items)


def validate_count(count: int) -> None:
    """Validate that count is an integer within the allowed limit."""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("count must be an integer.")

    if not 1 <= count <= MAXIMUM_GENERATION_COUNT:
        raise ValueError(
            f"count must be between 1 and {MAXIMUM_GENERATION_COUNT}"
        )


def is_valid_password(
    password: str,
    alternate_case: bool = False,
    no_duplicates: bool = False,
) -> bool:
    """Check password length, character composition, and optional rules."""
    if not isinstance(password, str):
        return False

    if (
        not isinstance(alternate_case, bool) or
        not isinstance(no_duplicates, bool)
    ):
        return False

    if not MINIMUM_LENGTH <= len(password) <= MAXIMUM_LENGTH:
        return False

    if no_duplicates and len(password) != len(set(password)):
        return False

    types = [classify_character(char) for char in password]

    if SPECIAL_CHARACTER in types:
        return False

    counts = Counter(types)

    if any(counts[name] < MINIMUM_PER_TYPE for name in CHARACTER_POOLS):
        return False

    if alternate_case and any(a == b for a, b in zip(types, types[1:])):
        return False

    return True
