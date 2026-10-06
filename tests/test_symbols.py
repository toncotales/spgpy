import unittest

from spgpy.constants import PUNCTUATION
from spgpy.policy import PasswordPolicy
from spgpy.symbols import build_symbol_pool


class SymbolPoolTests(unittest.TestCase):
    def test_default_pool_excludes_excluded_symbols(self):
        policy = PasswordPolicy()
        pool = build_symbol_pool(policy)

        self.assertTrue(pool)
        for symbol in policy.excluded_symbols:
            self.assertNotIn(symbol, pool)

    def test_all_symbols_returns_punctuation(self):
        policy = PasswordPolicy(all_symbols=True)
        self.assertEqual(build_symbol_pool(policy), PUNCTUATION)

    def test_cache_returns_same_value(self):
        policy = PasswordPolicy()
        first = build_symbol_pool(policy)
        second = build_symbol_pool(policy)

        self.assertIs(first, second)


if __name__ == "__main__":
    unittest.main()
