import subprocess

from rich.prompt import Prompt

from .git import git_current_branch
from .wrappers import stderr_of_proc

_NO_UPSTREAM = "no upstream branch"


def _push_upstream(branch: str, remote: str = "origin") -> None:
    """
    Push by setting the upstream branch

    :param branch:
    :param remote:
    :return:
    """

    command = ["git", "push", "--set-upstream", remote, branch]
    subprocess.run(command, capture_output=True, check=True, timeout=10)


def push(force: bool = False) -> None:
    command = ["git", "push"]

    if force:
        command.append("--force")

    result = subprocess.run(command, capture_output=True, check=False, timeout=10)
    stderr = stderr_of_proc(result)

    if result.returncode:
        no_upstream = _NO_UPSTREAM in stderr

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
                remote = input("Please enter the remote name: ")
                _push_upstream(branch_name, remote=remote)
