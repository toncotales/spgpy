"""Character arrangement for spgpy: order characters by type."""

from . import entropy
from .classifier import classify_character


def arrange_alternating(sequence: list[str]) -> str | None:
    """Arrange characters so that adjacent characters differ in type.

    Args:
        sequence: A list of single-character strings.

    Returns:
        str | None: The arranged characters joined into one string, or None
        if no arrangement exists (one type has more than half the characters,
        rounded up).

    Raises:
        TypeError: If sequence is not a list of strings.
        ValueError: If an item is not a single character.
    """
    if not isinstance(sequence, list):
        raise TypeError("sequence must be a list.")

    if not sequence:
        return ""

    groups: dict[str, list[str]] = {}

    for char in sequence:
        try:
            char_type = classify_character(char)
        except TypeError:
            raise TypeError("list must contain string objects.") from None
        except ValueError:
            raise ValueError(
                "list must contain a single character string."
            ) from None

        groups.setdefault(char_type, []).append(char)

    total = len(sequence)
    max_count = (total + 1) // 2

    if max(map(len, groups.values())) > max_count:
        return None

    for group in groups.values():
        entropy.shuffle(group)

    # Fill even positions first, then odd ones, largest group first.
    ordered_groups = sorted(groups.values(), key=len, reverse=True)
    slots = list(range(0, total, 2)) + list(range(1, total, 2))

    result = [""] * total
    index = 0

    for group in ordered_groups:
        for char in group:
            result[slots[index]] = char
            index += 1

    return "".join(result)
