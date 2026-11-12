"""The PasswordGenerator class, the main public API of spgpy."""

from collections.abc import Iterable

from . import entropy
from .arrangement import arrange_alternating
from .constants import DEFAULT_EXCLUDED_PUNCTUATIONS, DEFAULT_LENGTH
from .pools import build_character_pools, build_punctuation_pool
from .sampling import sample_characters_by_type
from .validation import (
    is_valid_password,
    validate_boolean,
    validate_count,
    validate_excluded_punctuation,
    validate_length,
)


class PasswordGenerator:
    """Generate cryptographically secure passwords.

    Args:
        length: Number of characters in each password.
        no_duplicates: If True, no character appears twice in a password.
        alternate_case: If True, no two adjacent characters share a type.
        use_all_punctuation: If True, ignore the excluded punctuation.
    """

    def __init__(
        self,
        length: int = DEFAULT_LENGTH,
        no_duplicates: bool = False,
        alternate_case: bool = False,
        use_all_punctuation: bool = False,
    ) -> None:
        self.length = length
        self.no_duplicates = no_duplicates
        self.alternate_case = alternate_case
        self.use_all_punctuation = use_all_punctuation

        self.set_excluded_punctuation(DEFAULT_EXCLUDED_PUNCTUATIONS)

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        validate_length(value)
        self._length = value

    @property
    def no_duplicates(self) -> bool:
        return self._no_duplicates

    @no_duplicates.setter
    def no_duplicates(self, value: bool) -> None:
        validate_boolean("no_duplicates", value)
        self._no_duplicates = value

    @property
    def alternate_case(self) -> bool:
        return self._alternate_case

    @alternate_case.setter
    def alternate_case(self, value: bool) -> None:
        validate_boolean("alternate_case", value)
        self._alternate_case = value

    @property
    def use_all_punctuation(self) -> bool:
        return self._use_all_punctuation

    @use_all_punctuation.setter
    def use_all_punctuation(self, value: bool) -> None:
        validate_boolean("use_all_punctuation", value)
        self._use_all_punctuation = value

    @property
    def excluded_punctuation(self) -> str:
        return "".join(self._excluded_punctuation)

    def set_excluded_punctuation(
        self, punctuation_characters: Iterable[str]
    ) -> None:
        """Set the collection of punctuation characters to be excluded."""
        items = validate_excluded_punctuation(punctuation_characters)
        self._excluded_punctuation = items

    def generate(self) -> str:
        """Generate one password using the current settings.

        Returns:
            str: The generated password.

        Raises:
            ValueError: If settings make password generation impossible.
                This can happen if:
                - All punctuation characters have been excluded.
                - `no_duplicates` is True and the requested `length` exceeds
                  the total number of unique characters available.
            RuntimeError: If the characters cannot be arranged so that no
                two neighbours share a type (should never happen).
        """
        punctuation_pool = build_punctuation_pool(
            self.use_all_punctuation, self.excluded_punctuation
        )

        if not punctuation_pool:
            raise ValueError("Allowed punctuation pool is empty.")

        pools = build_character_pools(punctuation_pool)

        characters = sample_characters_by_type(
            pools=pools,
            length=self.length,
            no_duplicates=self.no_duplicates,
            alternate_case=self.alternate_case,
        )

        if self.alternate_case:
            result = arrange_alternating(characters)

            if result is None:
                raise RuntimeError("Unable to alternate character types.")

            return result

        entropy.shuffle(characters)

        return "".join(characters)

    def generate_many(self, count: int = 1) -> list[str]:
        """Generate a list of secure passwords."""
        validate_count(count)
        return [self.generate() for _ in range(count)]

    @staticmethod
    def is_valid_password(
        password: str,
        alternate_case: bool = False,
        no_duplicates: bool = False,
    ) -> bool:
        """Validate a password string."""
        return is_valid_password(password, alternate_case, no_duplicates)
