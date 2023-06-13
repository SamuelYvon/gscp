import subprocess

from rich.prompt import Confirm, Prompt

from .git import git_current_branch
from .wrappers import stderr_of_proc

_NO_UPSTREAM = "no upstream branch"
_REMOTE_WORK = "remote contains work"


def _push_upstream(branch: str, remote: str = "origin") -> None:
    """
    Push by setting the upstream branch

    :param branch:
    :param remote:
    :return:
    """

    command = ["git", "push", "--set-upstream", remote, branch]
    subprocess.run(command, capture_output=True, check=True, timeout=10)


def _get_remote_name() -> str:
    remote = ""

    confirmed = False
    while not confirmed:
        remote = Prompt.ask("Please enter the remote name").strip()

        if not len(remote):
            print("Empty remote not allowed.")
            continue

        confirmed = Confirm.ask(f"Is '{remote}' the right remote?")

    assert len(remote), "Programming error"

    return remote


def pull() -> subprocess.CompletedProcess:
    command = ["git", "pull"]
    result = subprocess.run(command, capture_output=True, check=False, timeout=10)
    return result


def push(force: bool = False) -> None:
    command = ["git", "push"]

    if force:
        command.append("--force")

    result = subprocess.run(command, capture_output=True, check=False, timeout=10)
    stderr = stderr_of_proc(result)

    if result.returncode:
        no_upstream = _NO_UPSTREAM in stderr
        remote_work = _REMOTE_WORK in stderr

        if no_upstream:
            branch_name = git_current_branch()

            confirmation = Prompt.ask(
                f"It seems there is no upstream branch. "
                f"Do you want to push to origin/{branch_name} or another remote?",
                choices=["y", "n", "o"],
                default="y",
            )

            if confirmation == "y":
                _push_upstream(branch_name)
            elif confirmation == "o":
                _push_upstream(branch_name, remote=_get_remote_name())
        elif remote_work:
            confirmation = Prompt.ask(
                "It seems the remote branch contains work unmerged with the"
                " current branch. Do you want to pull?",
                choices=["y", "n"],
                default="y",
            )

            if confirmation == "y":
                # We pull (fast-forward or not, we need to push)
                _ = pull()
                push()
