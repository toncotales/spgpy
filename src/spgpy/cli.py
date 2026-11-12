"""Command-line interface for spgpy."""

import argparse
import sys

from . import __version__

from .generator import PasswordGenerator
from .constants import (
    DEFAULT_LENGTH,
    MINIMUM_LENGTH,
    MAXIMUM_LENGTH,
    MAXIMUM_GENERATION_COUNT,
)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="spgpy",
        description="Generate cryptographically secure passwords.",
        epilog="spgpy stands for Secure Password Generator for Python."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=DEFAULT_LENGTH,
        help=(
            f"Password length ({MINIMUM_LENGTH}-{MAXIMUM_LENGTH}, "
            f"default: {DEFAULT_LENGTH})"
        )
    )
    parser.add_argument(
        "-a",
        "--use-all-punctuation",
        action="store_true",
        help="Include all punctuation characters without exclusion"
    )
    parser.add_argument(
        "-t",
        "--alternate-case",
        action="store_true",
        help="Never place two characters of the same type next to each other"
    )
    parser.add_argument(
        "-d",
        "--no-duplicates",
        action="store_true",
        help="No duplicate characters"
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help=(
            f"Number of passwords to generate "
            f"(1-{MAXIMUM_GENERATION_COUNT}, default: 1)"
        )
    )

    return parser


def main() -> None:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    if not 1 <= args.count <= MAXIMUM_GENERATION_COUNT:
        parser.error(
            f"--count must be between 1 and {MAXIMUM_GENERATION_COUNT}"
        )

    try:
        generator = PasswordGenerator(
            length=args.length,
            no_duplicates=args.no_duplicates,
            alternate_case=args.alternate_case,
            use_all_punctuation=args.use_all_punctuation
        )

        for _ in range(args.count):
            print(generator.generate())

    except (TypeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
