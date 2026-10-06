import unittest
from dataclasses import FrozenInstanceError

from spgpy.constants import DEFAULT_EXCLUDED_SYMBOLS
from spgpy.policy import PasswordPolicy


class PasswordPolicyTests(unittest.TestCase):
    def test_defaults_are_valid(self):
        policy = PasswordPolicy()
        self.assertEqual(policy.length, 16)
        self.assertEqual(policy.excluded_symbols, DEFAULT_EXCLUDED_SYMBOLS)

    def test_policy_is_immutable(self):
        policy = PasswordPolicy()
        with self.assertRaises(FrozenInstanceError):
            policy.length = 20

    def test_length_type(self):
        with self.assertRaises(TypeError):
            PasswordPolicy(length="16")
        with self.assertRaises(TypeError):
            PasswordPolicy(length=True)

    def test_length_range(self):
        with self.assertRaises(ValueError):
            PasswordPolicy(length=11)
        with self.assertRaises(ValueError):
            PasswordPolicy(length=129)

    def test_boolean_types(self):
        with self.assertRaises(TypeError):
            PasswordPolicy(all_symbols=1)
        with self.assertRaises(TypeError):
            PasswordPolicy(alternate_types=0)

    def test_excluded_symbols_accept_iterables(self):
        policy = PasswordPolicy(excluded_symbols=("!", "@", "!"))
        self.assertEqual(policy.excluded_symbols, frozenset({"!", "@"}))

    def test_excluded_symbols_type(self):
        with self.assertRaises(TypeError):
            PasswordPolicy(excluded_symbols=123)
        with self.assertRaises(TypeError):
            PasswordPolicy(excluded_symbols={"!", 1})

    def test_excluded_symbols_values(self):
        with self.assertRaises(ValueError):
            PasswordPolicy(excluded_symbols={"ab"})
        with self.assertRaises(ValueError):
            PasswordPolicy(excluded_symbols={"a"})


if __name__ == "__main__":
    unittest.main()
