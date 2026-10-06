"""Character classification for spgpy."""

from .constants import UPPERCASE, LOWERCASE, DIGITS, PUNCTUATION


def get_char_type(char: str) -> str:
    """Return the character's type."""
    
    if not isinstance(char, str):
        raise TypeError("char must be a string.")
    
    if len(char) != 1:
        raise ValueError("char must contain exactly one character.")
    
    if char in UPPERCASE:
        return "uppercase"
    if char in LOWERCASE:
        return "lowercase"
    if char in DIGITS:
        return "digit"
    if char in PUNCTUATION:
        return "symbol"
    
    return "special_character"
