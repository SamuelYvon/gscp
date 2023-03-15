from rich.prompt import Confirm

from .wrappers import cmd_run_in_pty

_COMMIT_BASE_COMMAND = ["git", "commit", "-v"]


def _commit_with_message(
    message: str, amend: bool = False, no_verify: bool = False
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


def _commit_without_message(amend: bool = False, no_verify: bool = False) -> bool:
    cmd = [*_COMMIT_BASE_COMMAND]

    if amend:
        cmd.append("--amend")

    if no_verify:
        cmd.append("-n")

    return 0 == cmd_run_in_pty(*cmd)[0]


def commit(message: str, amend: bool = False, no_verify: bool = False) -> bool:
    if message:
        return _commit_with_message(message, amend=amend, no_verify=no_verify)
    else:
        return _commit_without_message(amend=amend, no_verify=no_verify)
