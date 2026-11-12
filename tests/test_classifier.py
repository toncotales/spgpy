import unittest

from src.spgpy.classifier import classify_character
from src.spgpy.constants import SPECIAL_CHARACTER


class ClassifierTests(unittest.TestCase):
    def test_character_types(self):
        cases = {
            "A": "UPPERCASE",
            "z": "LOWERCASE",
            "7": "DIGITS",
            "!": "PUNCTUATION",
        }

        for char, expected in cases.items():
            with self.subTest(char=char):
                self.assertEqual(classify_character(char), expected)

    def test_non_ascii_is_special_character(self):
        for char in ("é", "中", " ", "\n"):
            with self.subTest(char=char):
                self.assertEqual(classify_character(char), SPECIAL_CHARACTER)

    def test_non_string_raises_type_error(self):
        for value in (1, None, b"a", ["a"]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    classify_character(value)

    def test_wrong_length_raises_value_error(self):
        for value in ("", "ab"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    classify_character(value)
