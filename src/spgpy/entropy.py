"""Cryptographically secure random helpers used by spgpy.

Everything in this module is backed by the standard-library ``secrets``
module, so the rest of the package never touches the insecure ``random``
module.
"""

import secrets
from collections.abc import MutableSequence, Sequence
from typing import TypeVar

T = TypeVar("T")

_system_random = secrets.SystemRandom()


def choice(items: Sequence[T]) -> T:
    """Return one random item from a non-empty sequence."""
    return secrets.choice(items)


def sample(items: Sequence[T], count: int) -> list[T]:
    """Return count different random items (no repeats)."""
    return _system_random.sample(items, count)


def shuffle(items: MutableSequence[T]) -> None:
    """Shuffle a list in place."""
    _system_random.shuffle(items)


def weighted_index(weights: Sequence[int]) -> int:
    """Return a random index proportional to the given integer weights."""
    total = sum(weights)

    if total <= 0 or any(weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative and not all zero.")

    point = secrets.randbelow(total)

    for index, weight in enumerate(weights):
        if point < weight:
            return index
        point -= weight

    raise AssertionError("unreachable")
