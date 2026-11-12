import string
from types import MappingProxyType
from collections.abc import Mapping


MINIMUM_PER_TYPE: int = 2
MINIMUM_LENGTH: int = 12
DEFAULT_LENGTH: int = 16
MAXIMUM_LENGTH: int = 128
MAXIMUM_GENERATION_COUNT: int = 1000

SPECIAL_CHARACTER: str = "SPECIAL_CHARACTER"

CHARACTER_POOLS: Mapping[str, str] = MappingProxyType(
    {
        "UPPERCASE": string.ascii_uppercase,
        "LOWERCASE": string.ascii_lowercase,
        "PUNCTUATION": string.punctuation,
        "DIGITS": string.digits,
    }
)

PUNCTUATION_CLASSIFIED: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "common": frozenset("!@#$%&*-_?"),
        "uncommon": frozenset("[]{}().,:;+=~^|"),
        "unsafe": frozenset("'\"\\/`<>"),
    }
)

DEFAULT_EXCLUDED_PUNCTUATIONS: frozenset[str] = (
    PUNCTUATION_CLASSIFIED["unsafe"] | PUNCTUATION_CLASSIFIED["uncommon"]
)
