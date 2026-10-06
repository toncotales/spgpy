import unittest

from spgpy.validator import is_password_strong


class ValidatorTests(unittest.TestCase):
    def test_strong_password(self):
        self.assertTrue(is_password_strong("Aa12!Bb34@Cc"))

    def test_too_short(self):
        self.assertFalse(is_password_strong("Aa1!Aa1!Aa"))

    def test_missing_type(self):
        self.assertFalse(is_password_strong("AaAaAaAa!!!!"))

    def test_special_character(self):
        self.assertFalse(is_password_strong("Aa12! Aa12!"))

    def test_alternating_types(self):
        valid = "A1a!B2b@C3c#"
        invalid = "AA1!aa2!BB"

        self.assertTrue(is_password_strong(valid, alternate_types=True))
        self.assertFalse(is_password_strong(invalid, alternate_types=True))

    def test_non_string_password(self):
        self.assertFalse(is_password_strong(123))


if __name__ == "__main__":
    unittest.main()
