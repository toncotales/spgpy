"""Character shuffling for spgpy."""

import secrets

from .classify import get_char_type


def shuffle_by_type(text: str) -> str | None:
    """
    Shuffle characters such that no two adjacent characters share the same type.
    """
    
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    
    if not text:
        return ""
    
    groups: dict[str, list[str]] = {}
    for char in text:
        groups.setdefault(get_char_type(char), []).append(char)
        
    total = len(text)
    
    largest = max(len(group) for group in groups.values())
    if largest > (total + 1) // 2:
        return None
    
    rng = secrets.SystemRandom()
    for group in groups.values():
        rng.shuffle(group)
        
    ordered_groups = sorted(groups.values(), key=len, reverse=True)
    # Fill even positions first, then odd ones, largest group first.
    slots = list(range(0, total, 2)) + list(range(1, total, 2))
    
    result = [""] * total
    index = 0
    for group in ordered_groups:
        for char in group:
            result[slots[index]] = char
            index += 1
            
    return "".join(result)
