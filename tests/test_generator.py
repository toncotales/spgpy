import string
import unittest

from src.spgpy.constants import (
    DEFAULT_EXCLUDED_PUNCTUATIONS,
    DEFAULT_LENGTH,
    MAXIMUM_GENERATION_COUNT,
)
from src.spgpy.generator import PasswordGenerator


class DefaultsTests(unittest.TestCase):
    def test_default_settings(self):
        generator = PasswordGenerator()

        self.assertEqual(generator.length, DEFAULT_LENGTH)
        self.assertFalse(generator.no_duplicates)
        self.assertFalse(generator.alternate_case)
        self.assertFalse(generator.use_all_punctuation)
        self.assertEqual(
            set(generator.excluded_punctuation),
            set(DEFAULT_EXCLUDED_PUNCTUATIONS),
        )

    def test_default_password(self):
        password = PasswordGenerator().generate()

        self.assertEqual(len(password), DEFAULT_LENGTH)
        self.assertTrue(PasswordGenerator.is_valid_password(password))


class SettingsTests(unittest.TestCase):
    def test_invalid_length(self):
        with self.assertRaises(TypeError):
            PasswordGenerator(length="16")

        with self.assertRaises(ValueError):
            PasswordGenerator(length=5)

        with self.assertRaises(ValueError):
            PasswordGenerator(length=500)

    def test_invalid_boolean_options(self):
        for name in ("no_duplicates", "alternate_case", "use_all_punctuation"):
            with self.subTest(name=name):
                with self.assertRaises(TypeError):
                    PasswordGenerator(**{name: 1})

    def test_properties_can_be_changed(self):
        generator = PasswordGenerator()

        generator.length = 30
        generator.no_duplicates = True
        generator.alternate_case = True
        generator.use_all_punctuation = True

        self.assertEqual(generator.length, 30)
        self.assertTrue(generator.no_duplicates)
        self.assertTrue(generator.alternate_case)
        self.assertTrue(generator.use_all_punctuation)
        self.assertEqual(len(generator.generate()), 30)

    def test_properties_are_validated(self):
        generator = PasswordGenerator()

        with self.assertRaises(ValueError):
            generator.length = 1

        with self.assertRaises(TypeError):
            generator.alternate_case = "yes"

        self.assertEqual(generator.length, DEFAULT_LENGTH)
        self.assertFalse(generator.alternate_case)

    def test_set_excluded_punctuation(self):
        generator = PasswordGenerator()
        generator.set_excluded_punctuation("!@")

        self.assertEqual(set(generator.excluded_punctuation), {"!", "@"})

    def test_set_excluded_punctuation_is_validated(self):
        generator = PasswordGenerator()

        with self.assertRaises(ValueError):
            generator.set_excluded_punctuation("a")

        with self.assertRaises(TypeError):
            generator.set_excluded_punctuation(5)


class GenerateTests(unittest.TestCase):
    def test_every_option_combination(self):
        for no_duplicates in (False, True):
            for alternate_case in (False, True):
                for use_all in (False, True):
                    for length in (12, 13, 16, 40, 72):
                        with self.subTest(
                            no_duplicates=no_duplicates,
                            alternate_case=alternate_case,
                            use_all_punctuation=use_all,
                            length=length,
                        ):
                            generator = PasswordGenerator(
                                length=length,
                                no_duplicates=no_duplicates,
                                alternate_case=alternate_case,
                                use_all_punctuation=use_all,
                            )

                            for _ in range(25):
                                password = generator.generate()

                                self.assertEqual(len(password), length)
                                self.assertTrue(
                                    PasswordGenerator.is_valid_password(
                                        password,
                                        alternate_case=alternate_case,
                                        no_duplicates=no_duplicates,
                                    )
                                )

    def test_default_passwords_avoid_excluded_punctuation(self):
        generator = PasswordGenerator(length=64)
        excluded = set(DEFAULT_EXCLUDED_PUNCTUATIONS)

        for _ in range(100):
            self.assertTrue(excluded.isdisjoint(generator.generate()))

    def test_custom_excluded_punctuation_is_respected(self):
        generator = PasswordGenerator(length=64)
        generator.set_excluded_punctuation(
            set(string.punctuation) - set("!?")
        )

        for _ in range(100):
            password = generator.generate()
            punctuation = {c for c in password if c in string.punctuation}

            self.assertTrue(punctuation <= {"!", "?"})

    def test_use_all_punctuation_ignores_exclusions(self):
        generator = PasswordGenerator(use_all_punctuation=True)
        generator.set_excluded_punctuation(string.punctuation)

        self.assertTrue(
            PasswordGenerator.is_valid_password(generator.generate())
        )

    def test_all_punctuation_excluded_raises(self):
        generator = PasswordGenerator()
        generator.set_excluded_punctuation(string.punctuation)

        with self.assertRaises(ValueError):
            generator.generate()

    def test_no_duplicates_with_too_long_length_raises(self):
        generator = PasswordGenerator(length=128, no_duplicates=True)

        with self.assertRaises(ValueError):
            generator.generate()

    def test_passwords_differ(self):
        generator = PasswordGenerator(length=32)

        self.assertEqual(len({generator.generate() for _ in range(50)}), 50)


class GenerateManyTests(unittest.TestCase):
    def test_returns_requested_number_of_passwords(self):
        passwords = PasswordGenerator().generate_many(5)

        self.assertEqual(len(passwords), 5)
        self.assertTrue(all(isinstance(p, str) for p in passwords))

    def test_default_count_is_one(self):
        self.assertEqual(len(PasswordGenerator().generate_many()), 1)

    def test_maximum_count(self):
        passwords = PasswordGenerator().generate_many(MAXIMUM_GENERATION_COUNT)

        self.assertEqual(len(passwords), MAXIMUM_GENERATION_COUNT)

    def test_invalid_count(self):
        generator = PasswordGenerator()

        for value in (0, -1, MAXIMUM_GENERATION_COUNT + 1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    generator.generate_many(value)

        with self.assertRaises(TypeError):
            generator.generate_many("3")


class StaticValidationTests(unittest.TestCase):
    def test_is_valid_password_is_callable_on_the_class(self):
        self.assertTrue(PasswordGenerator.is_valid_password("Aa12!Bb34@Cc"))
        self.assertFalse(PasswordGenerator.is_valid_password("short"))

    def test_is_valid_password_options(self):
        password = "AAaa11!!BBbb"

        self.assertTrue(PasswordGenerator.is_valid_password(password))
        self.assertFalse(
            PasswordGenerator.is_valid_password(password, alternate_case=True)
        )
        self.assertFalse(
            PasswordGenerator.is_valid_password(password, no_duplicates=True)
        )
