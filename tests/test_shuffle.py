import unittest
from collections import Counter

from spgpy.classify import get_char_type
from spgpy.shuffle import shuffle_by_type


class ShuffleTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(shuffle_by_type(""), "")

    def test_preserves_characters(self):
        value = "AAaa11!!"
        result = shuffle_by_type(value)

        self.assertIsNotNone(result)
        self.assertEqual(Counter(result), Counter(value))

    def test_alternates_types(self):
        value = "AAaa11!!"
        result = shuffle_by_type(value)
        types = [get_char_type(char) for char in result]

        self.assertIsNotNone(result)
        self.assertTrue(all(a != b for a, b in zip(types, types[1:])))

    def test_returns_none_when_impossible(self):
        self.assertIsNone(shuffle_by_type("AAAAAaa1"))

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            shuffle_by_type(123)


if __name__ == "__main__":
    unittest.main()
