
import secrets

from .constants import (
    UPPERCASE,
    LOWERCASE,
    DIGITS,
    REQUIRED_TYPES,
    MIN_PER_TYPE,
)
from .policy import PasswordPolicy
from .shuffle import shuffle_by_type
from .symbols import build_symbol_pool


def _sample_alternating_characters(
    pools: tuple[str, str, str, str],
    length: int
) -> list[str]:
    """Sample characters ensuring counts allow strict type alternation."""
    
    counts = {char_type: MIN_PER_TYPE for char_type in REQUIRED_TYPES}
    max_per_type = (length + 1) // 2

    remaining = length - MIN_PER_TYPE * len(REQUIRED_TYPES)
    while remaining:
        available = [t for t in REQUIRED_TYPES if counts[t] < max_per_type]
        if not available:
            raise ValueError(
                "Password length cannot satisfy alternating-type requirements."
            )

        weighted = [
            t for t in available for _ in range(max_per_type - counts[t])
        ]
        counts[secrets.choice(weighted)] += 1
        remaining -= 1

    pool_by_type = dict(zip(REQUIRED_TYPES, pools))
    characters: list[str] = []
    for char_type in REQUIRED_TYPES:
        characters.extend(
            secrets.choice(pool_by_type[char_type])
            for _ in range(counts[char_type])
        )

    return characters


def _sample_characters(
    pools: tuple[str, str, str, str],
    length: int
) -> list[str]:
    """
    Sample minimum required characters per pool, then fill remaining length.
    """
    
    all_chars = "".join(pools)
    characters = [
        secrets.choice(pool)
        for pool in pools
        for _ in range(MIN_PER_TYPE)
    ]
    characters.extend(
        secrets.choice(all_chars)
        for _ in range(length - len(characters))
    )
    
    return characters


def generate_password(policy: PasswordPolicy | None = None) -> str:
    """Generate one cryptographically secure password from policy."""
    
    if policy is None:
        policy = PasswordPolicy()

    if not isinstance(policy, PasswordPolicy):
        raise TypeError("policy must be a PasswordPolicy instance.")

    symbols = build_symbol_pool(policy)
    if not symbols:
        raise ValueError(
            "Allowed symbol pool is empty. Cannot generate required symbols."
        )

    pools = (UPPERCASE, LOWERCASE, DIGITS, symbols)

    if policy.alternate_types:
        characters = _sample_alternating_characters(pools, policy.length)
        result = shuffle_by_type("".join(characters))
        if result is None:
            raise RuntimeError(
                "Internal error: generated types were not alternatable."
            )
        return result

    characters = _sample_characters(pools, policy.length)
    secrets.SystemRandom().shuffle(characters)
    
    return "".join(characters)
