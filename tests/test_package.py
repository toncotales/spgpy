import unittest

import src.spgpy as spgpy
from src.spgpy.generator import PasswordGenerator


class PackageTests(unittest.TestCase):
    def test_version_is_semver(self):
        self.assertRegex(spgpy.__version__, r"^\d+\.\d+\.\d+$")

    def test_public_api(self):
        self.assertEqual(
            sorted(spgpy.__all__), ["PasswordGenerator", "__version__"]
        )
        self.assertIs(spgpy.PasswordGenerator, PasswordGenerator)

    def test_old_api_is_gone(self):
        old_names = (
            "PasswordPolicy",
            "generate_password",
            "is_password_strong",
        )

        for name in old_names:
            with self.subTest(name=name):
                self.assertFalse(hasattr(spgpy, name))
