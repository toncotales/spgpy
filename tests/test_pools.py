import string
import unittest

from src.spgpy.constants import DEFAULT_EXCLUDED_PUNCTUATIONS
from src.spgpy.pools import build_character_pools, build_punctuation_pool


class PunctuationPoolTests(unittest.TestCase):
    def test_use_all_punctuation_ignores_exclusions(self):
        pool = build_punctuation_pool(True, set(string.punctuation))

        self.assertEqual(pool, string.punctuation)

    def test_excluded_characters_are_removed(self):
        pool = build_punctuation_pool(False, {"!", "@"})

        self.assertNotIn("!", pool)
        self.assertNotIn("@", pool)
        self.assertEqual(len(pool), len(string.punctuation) - 2)

    def test_default_exclusions(self):
        pool = build_punctuation_pool(False, DEFAULT_EXCLUDED_PUNCTUATIONS)

        self.assertEqual(set(pool), set("!@#$%&*-_?"))

    def test_excluding_everything_gives_empty_pool(self):
        self.assertEqual(
            build_punctuation_pool(False, set(string.punctuation)), ""
        )


class CharacterPoolsTests(unittest.TestCase):
    def test_pools_and_order(self):
        pools = build_character_pools("!?")

        self.assertEqual(
            pools,
            (
                string.ascii_uppercase,
                string.ascii_lowercase,
                string.digits,
                "!?",
            ),
        )
