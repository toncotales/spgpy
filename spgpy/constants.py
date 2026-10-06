"""Constants used by spgpy."""

import string


DEFAULT_LENGTH = 16
MIN_LENGTH  = 12
MAX_LENGTH = 128
MAX_COUNT = 1000

DIGITS = string.digits
PUNCTUATION = string.punctuation
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase

REQUIRED_TYPES = ("uppercase", "lowercase", "digit", "symbol")
MIN_PER_TYPE = 2

# Symbols that commonly break shells, URLs, SQL, or config files.
UNSAFE_SYMBOLS = frozenset([
    "'", '"',    # quotes
    "\\", "/",   # slashes
    "`",         # backtick
    "<", ">",    # angle brackets
])

# Symbols that are safe but uncommon.
UNCOMMON_SYMBOLS = frozenset([
    "[", "]", "{", "}", "(", ")",   # brackets and braces
    ".", ",",                       # period and comma
    ":", ";",                       # colon and semicolon
    "+", "=",                       # plus and equals
    "~", "^", "|",                  # tilde, caret, and pipe
])

DEFAULT_EXCLUDED_SYMBOLS = UNSAFE_SYMBOLS | UNCOMMON_SYMBOLS
