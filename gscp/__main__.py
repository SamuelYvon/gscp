"""
gscp: `Git Stage Commit Push`
Samuel Yvon <samuelyvon9@gmail.com>
"""

import argparse
from typing import cast

from .commit import commit
from .push import push
from .stage import stage


def _create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "message",
        type=str,
        default="",
        nargs="?",
        help="Commit message to use. If no message specified, "
        "it falls back to git's default behaviour with verbose mode",
    )

    parser.add_argument(
        "-a",
        "--amend",
        action="store_true",
        help="If we using git amend mode (warning, this triggers a force push)",
    )

    parser.add_argument(
        "-n",
        "--no-verify",
        action="store_true",
        help="If we skip the pre-commit hooks for git-add",
    )

    parser.add_argument(
        "-f", "--force", action="store_true", help="If we use `git push --force`"
    )

    return parser


def main() -> None:
    parser = _create_argparser()
    args = parser.parse_args()

    message = args.message if args.message else ""
    no_verify = cast(bool, args.no_verify)
    amend = cast(bool, args.amend)
    force = cast(bool, args.force)

    stage()
    if commit(message, amend=amend, no_verify=no_verify):
        push(force=force or amend)


if __name__ == "__main__":
    main()
