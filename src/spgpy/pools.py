"""Character pool builders for spgpy."""

from collections.abc import Collection

from .constants import CHARACTER_POOLS


def build_punctuation_pool(
    use_all_punctuation: bool,
    excluded_punctuation: Collection[str],
) -> str:
    """Build the pool of allowed punctuation characters.

    Args:
        use_all_punctuation: If True, bypasses the exclusion filter.
        excluded_punctuation: Punctuation characters to filter out.

    Returns:
        str: A string of filtered punctuation characters.
    """
    punctuation = CHARACTER_POOLS["PUNCTUATION"]

    if use_all_punctuation:
        return punctuation

    return "".join(
        char for char in punctuation if char not in excluded_punctuation
    )


def build_character_pools(punctuation_pool: str) -> tuple[str, ...]:
    """Return every character pool a password draws from.

    Args:
        punctuation_pool: The allowed punctuation characters, as built by
            ``build_punctuation_pool``.

    Returns:
        tuple[str, ...]: Uppercase letters, lowercase letters, digits and
        the given punctuation pool, in that order.
    """
    return (
        CHARACTER_POOLS["UPPERCASE"],
        CHARACTER_POOLS["LOWERCASE"],
        CHARACTER_POOLS["DIGITS"],
        punctuation_pool,
    )
