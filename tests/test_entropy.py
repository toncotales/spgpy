import unittest
from collections import Counter

from src.spgpy import entropy


class EntropyTests(unittest.TestCase):
    def test_choice_returns_member(self):
        items = "abcdef"

        for _ in range(50):
            self.assertIn(entropy.choice(items), items)

    def test_sample_returns_unique_items(self):
        items = list(range(20))
        result = entropy.sample(items, 10)

        self.assertEqual(len(result), 10)
        self.assertEqual(len(set(result)), 10)
        self.assertTrue(set(result) <= set(items))

    def test_sample_too_many_raises(self):
        with self.assertRaises(ValueError):
            entropy.sample([1, 2, 3], 4)

    def test_shuffle_keeps_items_and_returns_none(self):
        items = list("abcdefghij")
        original = items.copy()

        self.assertIsNone(entropy.shuffle(items))
        self.assertEqual(Counter(items), Counter(original))

    def test_weighted_index_skips_zero_weights(self):
        for _ in range(50):
            self.assertEqual(entropy.weighted_index([0, 5, 0]), 1)

    def test_weighted_index_invalid_weights(self):
        for weights in ([], [0, 0], [-1, 3]):
            with self.subTest(weights=weights):
                with self.assertRaises(ValueError):
                    entropy.weighted_index(weights)
