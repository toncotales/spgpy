"""Symbol pool generation for spgpy."""

from functools import lru_cache

from .constants import PUNCTUATION
from .policy import PasswordPolicy


@lru_cache(maxsize=32)
def build_symbol_pool(policy: PasswordPolicy) -> str:
    """Return the punctuation characters allowed by the policy."""
    
    if policy.all_symbols:
        return PUNCTUATION
    
    return "".join(s for s in PUNCTUATION if s not in policy.excluded_symbols)
