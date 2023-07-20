import os
import subprocess
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm

from .wrappers import cmd_run_in_pty, stderr_of_proc, stdout_of_proc

_COMMIT_BASE_COMMAND = ["git", "commit", "-v"]


def _commit_with_message(
    message: str, *, console: Console, amend: bool = False, no_verify: bool = False
) -> bool:
    cmd = [*_COMMIT_BASE_COMMAND, "-m", message]

    if amend:
        ok = Confirm.ask(
            "You are about to commit using git amend with a new message. "
            "Is this what you want?",
            default=True,
        )
        if not ok:
            return False

        cmd.append("--amend")

    if no_verify:
        cmd.append("-n")

    return 0 == cmd_run_in_pty(*cmd)[0]


def _commit_without_message(
    *, console: Console, amend: bool = False, no_verify: bool = False
) -> bool:
    cmd = [*_COMMIT_BASE_COMMAND]

    if amend:
        cmd.append("--amend")

    if no_verify:
        cmd.append("-n")

    return 0 == cmd_run_in_pty(*cmd)[0]


def commit(
    message: str, *, console: Console, amend: bool = False, no_verify: bool = False
) -> bool:
    if message:
        return _commit_with_message(
            message, console=console, amend=amend, no_verify=no_verify
        )
    else:
        return _commit_without_message(
            console=console, amend=amend, no_verify=no_verify
        )


def pre_commit() -> str | bool:
    """
    Runs the pre-commit hook script if it exists.

    A pre-condition is that we know we are within a git directory.
    """

    directory = Path(os.getcwd())
    dot_git = ".git"

    while not (directory / dot_git).exists():
        directory = directory.parent  # go up!

    pre_commit_script = directory / dot_git / "hooks" / "pre-commit"

    if not pre_commit_script.is_file():
        return True

    # Run the script twice in case it auto fixes stuff
    out = subprocess.run(
        [pre_commit_script], capture_output=False, check=False, timeout=10
    )

    if 0 == out.returncode:
        return True

    out = subprocess.run(
        [pre_commit_script], capture_output=True, check=False, timeout=10
    )

    if 0 == out.returncode:
        return True
    else:
        stdout = stdout_of_proc(out)
        stderr = stderr_of_proc(out)

        return f"{stdout}\n{stderr}".strip()
