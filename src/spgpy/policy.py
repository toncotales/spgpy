"""Password generation policy for spgpy."""

from dataclasses import dataclass

from .constants import (
    DEFAULT_EXCLUDED_SYMBOLS,
    DEFAULT_LENGTH,
    MAX_LENGTH,
    MIN_LENGTH,
    PUNCTUATION,
)

@dataclass(frozen=True)
class PasswordPolicy:
    """Rules describing how a password should be generated.

    Attributes:
        length: Total password length.
        all_symbols: Use every punctuation symbol, ignoring excluded_symbols.
        alternate_types: No two adjacent characters can be of the same type.
        excluded_symbols: Punctuation characters left out of the symbol pool.
    """

    length: int = DEFAULT_LENGTH
    all_symbols: bool = False
    alternate_types: bool = False
    excluded_symbols: frozenset[str] = DEFAULT_EXCLUDED_SYMBOLS

    def __post_init__(self) -> None:
        
        if isinstance(self.length, bool) or not isinstance(self.length, int):
            raise TypeError("length must be an integer.")

        if not MIN_LENGTH <= self.length <= MAX_LENGTH:
            raise ValueError(
                f"length must be between {MIN_LENGTH} "
                f"and {MAX_LENGTH} characters."
            )

        if not isinstance(self.all_symbols, bool):
            raise TypeError("all_symbols must be a boolean.")

        if not isinstance(self.alternate_types, bool):
            raise TypeError("alternate_types must be a boolean.")

        try:
            excluded = frozenset(self.excluded_symbols)
        except TypeError as exc:
            raise TypeError(
                "excluded_symbols must be an iterable of characters."
            ) from exc

        if any(not isinstance(char, str) for char in excluded):
            raise TypeError("excluded_symbols must contain only strings.")

        if any(len(char) != 1 for char in excluded):
            raise ValueError(
                "Each excluded symbol must be exactly one character."
            )

        if any(char not in PUNCTUATION for char in excluded):
            raise ValueError("excluded_symbols may contain punctuation only.")

        object.__setattr__(self, "excluded_symbols", excluded)
