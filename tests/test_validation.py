import unittest

from src.spgpy.constants import MAXIMUM_GENERATION_COUNT
from src.spgpy.validation import (
    is_valid_password,
    validate_boolean,
    validate_count,
    validate_excluded_punctuation,
    validate_length,
)


class ValidateLengthTests(unittest.TestCase):
    def test_valid_lengths(self):
        for length in (12, 16, 128):
            with self.subTest(length=length):
                validate_length(length)

    def test_wrong_type(self):
        for value in ("16", 16.0, None, True):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    validate_length(value)

    def test_out_of_range(self):
        for value in (-1, 0, 11, 129):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_length(value)


class ValidateBooleanTests(unittest.TestCase):
    def test_accepts_booleans(self):
        validate_boolean("flag", True)
        validate_boolean("flag", False)

    def test_rejects_other_types(self):
        for value in (0, 1, "True", None):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, "flag"):
                    validate_boolean("flag", value)


class ValidateExcludedPunctuationTests(unittest.TestCase):
    def test_accepts_any_iterable_of_punctuation(self):
        for value in ("!@", ["!", "@"], ("!", "@"), {"!", "@"}):
            with self.subTest(value=value):
                self.assertEqual(
                    validate_excluded_punctuation(value),
                    frozenset("!@"),
                )

    def test_empty_is_allowed(self):
        self.assertEqual(validate_excluded_punctuation(""), frozenset())

    def test_not_iterable(self):
        with self.assertRaises(TypeError):
            validate_excluded_punctuation(5)

    def test_items_must_be_single_characters(self):
        for value in (["!!"], [1], [""]):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_excluded_punctuation(value)

    def test_items_must_be_punctuation(self):
        for value in ("a", "1", " ", "é"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_excluded_punctuation(value)


class ValidateCountTests(unittest.TestCase):
    def test_valid_counts(self):
        for count in (1, 10, MAXIMUM_GENERATION_COUNT):
            with self.subTest(count=count):
                validate_count(count)

    def test_wrong_type(self):
        for value in ("1", 1.0, None, True):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    validate_count(value)

    def test_out_of_range(self):
        for value in (0, -1, MAXIMUM_GENERATION_COUNT + 1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_count(value)


class IsValidPasswordTests(unittest.TestCase):
    def test_strong_password(self):
        self.assertTrue(is_valid_password("Aa12!Bb34@Cc"))

    def test_non_string_password(self):
        for value in (None, 123, b"Aa12!Bb34@Cc"):
            with self.subTest(value=value):
                self.assertFalse(is_valid_password(value))

    def test_non_boolean_options(self):
        self.assertFalse(is_valid_password("Aa12!Bb34@Cc", alternate_case=1))
        self.assertFalse(is_valid_password("Aa12!Bb34@Cc", no_duplicates="x"))

    def test_length_limits(self):
        self.assertFalse(is_valid_password("Aa1!Bb2@Cc3"))
        self.assertTrue(is_valid_password("Aa1!" * 32))
        self.assertFalse(is_valid_password("Aa1!" * 33))

    def test_missing_type(self):
        for password in (
            "aa11!!bb22@@",  # no uppercase
            "AA11!!BB22@@",  # no lowercase
            "AAaa!!BBbb@@",  # no digit
            "AAaa11BBbb22",  # no punctuation
        ):
            with self.subTest(password=password):
                self.assertFalse(is_valid_password(password))

    def test_needs_two_of_each_type(self):
        self.assertFalse(is_valid_password("Aaaaaaaaaaa1!!!"))

    def test_special_characters_are_rejected(self):
        self.assertFalse(is_valid_password("Aa12!Bb34@Cc é"))

    def test_alternate_case_rule(self):
        self.assertFalse(
            is_valid_password("AAaa11!!BBbb", alternate_case=True)
        )
        self.assertTrue(is_valid_password("Aa1!Bb2@Cc3#", alternate_case=True))

    def test_no_duplicates_rule(self):
        self.assertTrue(is_valid_password("Aa1!Bb2@Cc3#", no_duplicates=True))
        self.assertFalse(is_valid_password("Aa1!Aa1!Bb2@", no_duplicates=True))
        self.assertTrue(is_valid_password("Aa1!Aa1!Bb2@"))
