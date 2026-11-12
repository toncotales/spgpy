import unittest
from collections import Counter

from src.spgpy.arrangement import arrange_alternating
from src.spgpy.classifier import classify_character


def has_adjacent_same_type(text):
    types = [classify_character(char) for char in text]
    return any(a == b for a, b in zip(types, types[1:]))


class ArrangeAlternatingTests(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(arrange_alternating([]), "")

    def test_preserves_characters(self):
        chars = list("Aa1!Bb2@Cc3#")
        result = arrange_alternating(chars)

        self.assertEqual(Counter(result), Counter(chars))

    def test_no_adjacent_characters_share_a_type(self):
        chars = list("AB12cdEF34gh!@#$")

        for _ in range(200):
            result = arrange_alternating(chars)

            self.assertIsNotNone(result)
            self.assertFalse(has_adjacent_same_type(result))

    def test_returns_none_when_impossible(self):
        self.assertIsNone(arrange_alternating(list("ABCDe")))

    def test_single_character(self):
        self.assertEqual(arrange_alternating(["A"]), "A")

    def test_input_must_be_a_list(self):
        for value in ("abc", ("a", "b"), None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    arrange_alternating(value)

    def test_items_must_be_strings(self):
        with self.assertRaises(TypeError):
            arrange_alternating(["a", 1])

    def test_items_must_be_single_characters(self):
        with self.assertRaises(ValueError):
            arrange_alternating(["a", "bc"])
