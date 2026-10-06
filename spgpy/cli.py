"""Command-line interface for spgpy."""

import argparse
import sys

from . import __version__

from .constants import DEFAULT_LENGTH, MAX_COUNT, MAX_LENGTH, MIN_LENGTH
from .policy import PasswordPolicy
from .generator import generate_password
from .validator import is_password_strong


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    
    parser = argparse.ArgumentParser(
        prog="spgpy",
        description="Generate cryptographically secure passwords.",
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
            f"Password length ({MIN_LENGTH}-{MAX_LENGTH}, "
            f"default: {DEFAULT_LENGTH})"
        )
    )
    parser.add_argument(
        "-a",
        "--all-symbols",
        action="store_true",
        help="Include all punctuation symbols without exclusion"
    )
    parser.add_argument(
        "-t",
        "--alternate-types",
        action="store_true",
        help="Never place two characters of the same type next to each other"
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help=f"Number of passwords to generate (1-{MAX_COUNT}, default: 1)"
    )
    parser.add_argument(
        "-v",
        "--validate",
        type=str,
        help="Check if a specific password meets strength requirements"
    )

    return parser


def main() -> None:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    if args.validate is not None:
        if is_password_strong(
            args.validate,
            alternate_types=args.alternate_types
        ):
            print("[PASSED] Strength check successful.")
            return
        
        print("[FAILED] Strength check failed.")
        raise SystemExit(1)

    if not 1 <= args.count <= MAX_COUNT:
        parser.error(f"--count must be between 1 and {MAX_COUNT}")

    try:
        policy = PasswordPolicy(
            length=args.length,
            all_symbols=args.all_symbols,
            alternate_types=args.alternate_types
        )

        for _ in range(args.count):
            print(generate_password(policy))

    except (TypeError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
