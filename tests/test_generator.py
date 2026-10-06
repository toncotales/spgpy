import unittest
from collections import Counter

from spgpy.constants import MIN_PER_TYPE
from spgpy.generator import generate_password
from spgpy.policy import PasswordPolicy
from spgpy.classify import get_char_type
from spgpy.validator import is_password_strong


class GeneratorTests(unittest.TestCase):
    def test_default_password(self):
        password = generate_password()
        self.assertEqual(len(password), 16)
        self.assertTrue(is_password_strong(password))

    def test_custom_length(self):
        policy = PasswordPolicy(length=32)
        password = generate_password(policy)
        self.assertEqual(len(password), 32)
        self.assertTrue(is_password_strong(password))

    def test_required_types(self):
        password = generate_password()
        counts = Counter(
            get_char_type(char) for char in password
        )
        char_types = ("uppercase", "lowercase", "digit", "symbol")

        for char_type in char_types:
            self.assertGreaterEqual(counts[char_type], MIN_PER_TYPE)

    def test_alternating_types(self):
        policy = PasswordPolicy(length=24, alternate_types=True)
        password = generate_password(policy)
        types = [get_char_type(char) for char in password]

        self.assertTrue(all(a != b for a, b in zip(types, types[1:])))
        self.assertTrue(is_password_strong(password, alternate_types=True))

    def test_alternating_types_at_minimum_length(self):
        policy = PasswordPolicy(length=12, alternate_types=True)

        for _ in range(100):
            with self.subTest(iteration=_):
                password = generate_password(policy)
                types = [get_char_type(char) for char in password]
                self.assertEqual(len(password), 12)
                self.assertTrue(all(a != b for a, b in zip(types, types[1:])))
                self.assertTrue(is_password_strong(password, alternate_types=True))

    def test_alternating_types_never_fails_for_supported_lengths(self):
        for length in range(12, 129):
            policy = PasswordPolicy(length=length, alternate_types=True)
            password = generate_password(policy)

            with self.subTest(length=length):
                types = [get_char_type(char) for char in password]
                self.assertEqual(len(password), length)
                self.assertTrue(all(a != b for a, b in zip(types, types[1:])))
                self.assertTrue(is_password_strong(password, alternate_types=True))

    def test_all_symbols(self):
        policy = PasswordPolicy(all_symbols=True)
        password = generate_password(policy)

        self.assertEqual(len(password), 16)
        self.assertTrue(is_password_strong(password))

    def test_invalid_policy_argument(self):
        with self.assertRaises(TypeError):
            generate_password(123)


if __name__ == "__main__":
    unittest.main()
