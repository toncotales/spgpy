import string
import unittest
from collections import Counter

from src.spgpy.classifier import classify_character
from src.spgpy.constants import MINIMUM_PER_TYPE
from src.spgpy.sampling import sample_characters_by_type

POOLS = (
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits,
    "!@#$%&*-_?",
)


def sample(**overrides):
    options = {
        "pools": POOLS,
        "length": 16,
        "no_duplicates": False,
        "alternate_case": False,
    }
    options.update(overrides)

    return sample_characters_by_type(**options)


class SamplingTests(unittest.TestCase):
    def test_every_option_combination(self):
        for no_duplicates in (False, True):
            for alternate_case in (False, True):
                for length in (12, 13, 16, 40, 72):
                    with self.subTest(
                        no_duplicates=no_duplicates,
                        alternate_case=alternate_case,
                        length=length,
                    ):
                        for _ in range(50):
                            chars = sample(
                                length=length,
                                no_duplicates=no_duplicates,
                                alternate_case=alternate_case,
                            )
                            counts = Counter(
                                classify_character(char) for char in chars
                            )

                            self.assertEqual(len(chars), length)
                            self.assertEqual(len(counts), 4)
                            self.assertTrue(
                                all(n >= MINIMUM_PER_TYPE
                                    for n in counts.values())
                            )

                            if no_duplicates:
                                self.assertEqual(len(set(chars)), length)

                            if alternate_case:
                                self.assertLessEqual(
                                    max(counts.values()), (length + 1) // 2
                                )

    def test_pool_order_does_not_matter(self):
        # Every pool must keep 2 to max characters, whatever order the pools
        # are passed in.
        reordered = (POOLS[3], POOLS[2], POOLS[0], POOLS[1])

        for _ in range(100):
            chars = sample(pools=reordered, alternate_case=True)
            counts = Counter(classify_character(char) for char in chars)

            self.assertTrue(all(2 <= n <= 8 for n in counts.values()))

    def test_wrong_number_of_pools(self):
        with self.assertRaises(ValueError):
            sample(pools=POOLS[:3])

    def test_empty_pool(self):
        with self.assertRaises(ValueError):
            sample(pools=(POOLS[0], POOLS[1], POOLS[2], ""))

    def test_no_duplicates_pool_too_small(self):
        with self.assertRaises(ValueError):
            sample(pools=(POOLS[0], POOLS[1], POOLS[2], "!"),
                   no_duplicates=True)

    def test_no_duplicates_length_exceeds_available(self):
        with self.assertRaises(ValueError):
            sample(length=73, no_duplicates=True)

    def test_repeated_pool_characters_count_once_when_unique(self):
        pools = (POOLS[0], POOLS[1], POOLS[2], "!!??")
        chars = sample(pools=pools, length=16, no_duplicates=True)

        self.assertEqual(len(set(chars)), 16)
