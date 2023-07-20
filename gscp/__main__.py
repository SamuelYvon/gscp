"""
gscp: `Git Stage Commit Push`
Samuel Yvon <samuelyvon9@gmail.com>
"""

import argparse
from typing import cast

from rich.console import Console

from gscp.commit import commit, pre_commit
from gscp.git import git_is_in_repo
from gscp.push_pull import push
from gscp.stage import stage
from gscp.version import ApplicationVersion


def _create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-cp",
        "--commit-push",
        action="store_true",
        help="Skip the stage part; take what is already staged.",
    )

    parser.add_argument(
        "--version", action="version", version=f"gscp {ApplicationVersion.parse()}"
    )

    parser.add_argument(
        "message",
        type=str,
        default="",
        nargs="?",
        help="Commit message to use. If no message specified, "
        "it falls back to git's default behaviour with verbose mode",
    )

    parser.add_argument(
        "-pre",
        action="store_true",
        help="Performs a pre-commit check before making the actual commit."
        " Uses the git pre-commit hook.",
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
    console = Console()

    parser = _create_argparser()
    args = parser.parse_args()

    pre = cast(bool, args.pre)
    commit_push_only = cast(bool, args.commit_push)
    message = args.message if args.message else ""
    no_verify = cast(bool, args.no_verify)
    amend = cast(bool, args.amend)
    force = cast(bool, args.force)

    if not git_is_in_repo():
        console.print("You are not in a git repository", style="bold red")
        exit(1)

    if pre:
        pre_commit_result = pre_commit()

        if isinstance(pre_commit_result, str):
            print(pre_commit_result)
            console.print(
                "Pre-commit script failed. Fix errors then try again.", style="bold red"
            )
            exit(1)

    if not commit_push_only:
        stage(console)

    if commit(message, amend=amend, no_verify=no_verify, console=console):
        push(force=force or amend)


if __name__ == "__main__":
    main()
