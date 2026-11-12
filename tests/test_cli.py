import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from src.spgpy import __version__
from src.spgpy.cli import build_parser, main
from src.spgpy.constants import (
    DEFAULT_EXCLUDED_PUNCTUATIONS,
    DEFAULT_LENGTH,
    MAXIMUM_GENERATION_COUNT,
)
from src.spgpy.generator import PasswordGenerator


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        """Run main() and return (exit_code, stdout, stderr)."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = None

        with patch.object(sys, "argv", ["spgpy", *args]):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                try:
                    main()
                except SystemExit as exc:
                    code = exc.code

        return code, stdout.getvalue(), stderr.getvalue()

    def test_parser_defaults(self):
        args = build_parser().parse_args([])

        self.assertEqual(args.length, DEFAULT_LENGTH)
        self.assertEqual(args.count, 1)
        self.assertFalse(args.use_all_punctuation)
        self.assertFalse(args.alternate_case)
        self.assertFalse(args.no_duplicates)

    def test_default_run_prints_one_valid_password(self):
        code, out, err = self.run_cli()
        lines = out.splitlines()

        self.assertIsNone(code)
        self.assertEqual(err, "")
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(lines[0]), DEFAULT_LENGTH)
        self.assertTrue(PasswordGenerator.is_valid_password(lines[0]))

    def test_length_and_count(self):
        _, out, _ = self.run_cli("--length", "24", "--count", "3")
        lines = out.splitlines()

        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(line) == 24 for line in lines))

    def test_short_flags(self):
        _, out, _ = self.run_cli("-l", "20", "-n", "2", "-t", "-d", "-a")
        lines = out.splitlines()

        self.assertEqual(len(lines), 2)

        for line in lines:
            self.assertTrue(
                PasswordGenerator.is_valid_password(
                    line, alternate_case=True, no_duplicates=True
                )
            )

    def test_alternate_case_flag(self):
        _, out, _ = self.run_cli("--alternate-case", "--count", "20")

        for line in out.splitlines():
            self.assertTrue(
                PasswordGenerator.is_valid_password(line, alternate_case=True)
            )

    def test_no_duplicates_flag(self):
        _, out, _ = self.run_cli("--no-duplicates", "--count", "20")

        for line in out.splitlines():
            self.assertEqual(len(set(line)), len(line))

    def test_default_excludes_unsafe_punctuation(self):
        _, out, _ = self.run_cli("--length", "128", "--count", "20")

        for line in out.splitlines():
            self.assertTrue(
                set(DEFAULT_EXCLUDED_PUNCTUATIONS).isdisjoint(line)
            )

    def test_use_all_punctuation_flag(self):
        code, out, _ = self.run_cli("--use-all-punctuation", "--count", "5")

        self.assertIsNone(code)
        self.assertEqual(len(out.splitlines()), 5)

    def test_version(self):
        code, out, _ = self.run_cli("--version")

        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), f"spgpy {__version__}")

    def test_count_out_of_range_is_a_usage_error(self):
        for count in ("0", "-1", str(MAXIMUM_GENERATION_COUNT + 1)):
            with self.subTest(count=count):
                code, out, err = self.run_cli("--count", count)

                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertIn("--count must be between", err)

    def test_length_out_of_range_reports_error(self):
        for length in ("5", "500"):
            with self.subTest(length=length):
                code, out, err = self.run_cli("--length", length)

                self.assertEqual(code, 1)
                self.assertEqual(out, "")
                self.assertTrue(err.startswith("Error: length must be"))

    def test_impossible_settings_report_error(self):
        code, out, err = self.run_cli("-l", "128", "--no-duplicates")

        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Error:", err)

    def test_non_integer_arguments_are_a_usage_error(self):
        for args in (("--length", "abc"), ("--count", "x")):
            with self.subTest(args=args):
                code, _, _ = self.run_cli(*args)

                self.assertEqual(code, 2)

    def test_removed_options_are_rejected(self):
        for flag in ("--validate", "--all-symbols", "--alternate-types"):
            with self.subTest(flag=flag):
                args = (flag, "x") if flag == "--validate" else (flag,)
                code, _, _ = self.run_cli(*args)

                self.assertEqual(code, 2)
