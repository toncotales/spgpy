"""Character sampling for spgpy: decide which characters a password holds."""

from collections.abc import Sequence

from . import entropy
from .constants import CHARACTER_POOLS, MINIMUM_PER_TYPE


def sample_characters_by_type(
    *,
    pools: Sequence[str],
    length: int,
    no_duplicates: bool,
    alternate_case: bool,
) -> list[str]:
    """Pick the characters for one password, grouped by pool.

    Every pool contributes at least ``MINIMUM_PER_TYPE`` characters. The
    returned list is not shuffled; the caller decides the final order.

    Args:
        pools: One string of allowed characters per character type.
        length: Total number of characters to pick.
        no_duplicates: If True, no character is picked twice.
        alternate_case: If True, keep every type at or below half the
            length (rounded up) so the characters can later be arranged
            with no two neighbours of the same type.

    Returns:
        list[str]: The picked characters.

    Raises:
        ValueError: If the pools cannot satisfy the requested settings.
    """
    if len(pools) != len(CHARACTER_POOLS):
        raise ValueError("Incorrect number of character pools")

    if any(not pool for pool in pools):
        raise ValueError("Character pools must not be empty.")

    if no_duplicates:
        return _sample_unique(pools, length, alternate_case)

    return _sample_with_repeats(pools, length, alternate_case)


def _sample_unique(
    pools: Sequence[str],
    length: int,
    alternate_case: bool,
) -> list[str]:
    """Pick characters so that none is used more than once."""
    # Remove repeated characters inside each pool, keeping their order.
    unique_pools = [list(dict.fromkeys(pool)) for pool in pools]

    if any(len(pool) < MINIMUM_PER_TYPE for pool in unique_pools):
        raise ValueError(
            "Each character pool must contain enough unique "
            "characters to satisfy the minimum requirement."
        )

    total_available = len({char for pool in unique_pools for char in pool})

    if length > total_available:
        raise ValueError(
            "Password length exceeds the number of available "
            "unique characters."
        )

    # Guarantee the minimum number of characters from every pool.
    selected: list[str] = []

    for pool in unique_pools:
        selected.extend(entropy.sample(pool, MINIMUM_PER_TYPE))

    selected_set = set(selected)
    remaining = length - len(selected)

    # Every character not picked yet, remembered with the pool it came from.
    candidates: list[tuple[int, str]] = [
        (index, char)
        for index, pool in enumerate(unique_pools)
        for char in pool
        if char not in selected_set
    ]

    if not alternate_case:
        picked = entropy.sample(candidates, remaining)
        selected.extend(char for _, char in picked)
        return selected

    # Keep the number of characters per type balanced.
    counts = [MINIMUM_PER_TYPE] * len(unique_pools)
    max_count = (length + 1) // 2

    while remaining:
        eligible = [
            position
            for position, (index, _) in enumerate(candidates)
            if counts[index] < max_count
        ]

        if not eligible:
            raise ValueError(
                "Unable to generate a unique password "
                "with alternating character types."
            )

        index, char = candidates.pop(entropy.choice(eligible))

        selected.append(char)
        counts[index] += 1
        remaining -= 1

    return selected


def _sample_with_repeats(
    pools: Sequence[str],
    length: int,
    alternate_case: bool,
) -> list[str]:
    """Pick characters while allowing the same character more than once."""
    # counts[i] is how many characters will be drawn from pools[i]. Using the
    # pool's position (not its name) keeps counts and pools aligned.
    counts = [MINIMUM_PER_TYPE] * len(pools)
    remaining = length - sum(counts)

    if alternate_case:
        max_per_type = (length + 1) // 2

        while remaining:
            open_pools = [
                index
                for index, count in enumerate(counts)
                if count < max_per_type
            ]

            if not open_pools:
                raise ValueError(
                    "Password length cannot satisfy alternating-type "
                    "requirements."
                )

            # Pools with more room left are more likely to be picked.
            weighted = [
                index
                for index in open_pools
                for _ in range(max_per_type - counts[index])
            ]

            counts[entropy.choice(weighted)] += 1
            remaining -= 1

        return [
            entropy.choice(pool)
            for pool, count in zip(pools, counts)
            for _ in range(count)
        ]

    all_characters = "".join(pools)

    characters = [
        entropy.choice(pool)
        for pool in pools
        for _ in range(MINIMUM_PER_TYPE)
    ]

    characters.extend(entropy.choice(all_characters) for _ in range(remaining))

    return characters
