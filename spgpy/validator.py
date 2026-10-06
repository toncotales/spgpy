"""Password strength validation for spgpy."""

from collections import Counter

from .classify import get_char_type
from .constants import MIN_LENGTH, MIN_PER_TYPE, REQUIRED_TYPES


def is_password_strong(password: str, alternate_types: bool = False) -> bool:
    """
    Return True if the password meets all strength and structural requirements.
    """
    
    if not isinstance(password, str) or not isinstance(alternate_types, bool):
        return False
    
    if len(password) < MIN_LENGTH:
        return False
    
    char_types = [get_char_type(char) for char in password]
    if "special_character" in char_types:
        return False
    
    counts = Counter(char_types)
    if any(counts[t] < MIN_PER_TYPE for t in REQUIRED_TYPES):
        return False
    
    if alternate_types:
        return all(a != b for a, b in zip(char_types, char_types[1:]))
    
    return True
