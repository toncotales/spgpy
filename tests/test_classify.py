import unittest

from spgpy.classify import get_char_type


class ClassifyTests(unittest.TestCase):
    def test_get_char_type(self):
        cases = {
            "A": "uppercase",
            "z": "lowercase",
            "7": "digit",
            "!": "symbol",
            " ": "special_character",
        }

        for char, expected in cases.items():
            with self.subTest(char=char):
                self.assertEqual(get_char_type(char), expected)

    def test_non_ascii_is_special_character(self):
        self.assertEqual(get_char_type("é"), "special_character")

    def test_validation(self):
        with self.assertRaises(TypeError):
            get_char_type(1)
        with self.assertRaises(ValueError):
            get_char_type("")
        with self.assertRaises(ValueError):
            get_char_type("ab")


if __name__ == "__main__":
    unittest.main()
