from .constants import CHARACTER_POOLS, SPECIAL_CHARACTER


def classify_character(char: str) -> str:
    """Return the character-pool name for one character."""
    if not isinstance(char, str):
        raise TypeError("char must be a string.")

    if len(char) != 1:
        raise ValueError("char must be a single character.")

    for character_type, pool in CHARACTER_POOLS.items():

        if char in pool:
            return character_type

    return SPECIAL_CHARACTER
