import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from spgpy.cli import main


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        stdout = io.StringIO()
        stderr = io.StringIO()
        argv = ["spgpy", *args]

        with patch.object(sys, "argv", argv):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as exc:
                    main()

        return exc.exception.code, stdout.getvalue(), stderr.getvalue()

    def test_generate_count(self):
        output = io.StringIO()
        argv = ["spgpy", "-n", "3"]

        with patch.object(sys, "argv", argv):
            with redirect_stdout(output):
                main()

        self.assertEqual(len(output.getvalue().splitlines()), 3)

    def test_count_above_maximum(self):
        code, _, stderr = self.run_cli("-n", "1001")
        self.assertEqual(code, 2)
        self.assertIn("--count must be between", stderr)

    def test_count_below_minimum(self):
        code, _, stderr = self.run_cli("-n", "0")
        self.assertEqual(code, 2)
        self.assertIn("--count must be between", stderr)

    def test_empty_validation_value_is_checked(self):
        output = io.StringIO()
        argv = ["spgpy", "--validate", ""]

        with patch.object(sys, "argv", argv):
            with redirect_stdout(output):
                with self.assertRaises(SystemExit) as exc:
                    main()

        self.assertEqual(exc.exception.code, 1)
        self.assertIn("[FAILED]", output.getvalue())

    def test_validation(self):
        output = io.StringIO()
        password = "Aa12!Bb34@Cc"
        argv = ["spgpy", "--validate", password]

        with patch.object(sys, "argv", argv):
            with redirect_stdout(output):
                main()

        self.assertIn("[PASSED]", output.getvalue())
        
    def test_validation_failure_returns_nonzero(self):
        output = io.StringIO()
        argv = ["spgpy", "--validate", "weak"]

        with patch.object(sys, "argv", argv):
            with redirect_stdout(output):
                with self.assertRaises(SystemExit) as exc:
                    main()

        self.assertEqual(exc.exception.code, 1)
        self.assertIn("[FAILED]", output.getvalue())


if __name__ == "__main__":
    unittest.main()
