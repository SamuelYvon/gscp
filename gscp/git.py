import subprocess

from .wrappers import stdout_of_proc


def git_current_branch() -> str:
    command = ["git", "branch", "--show-current"]
    out = stdout_of_proc(
        subprocess.run(command, capture_output=True, check=True, timeout=10)
    )
    return out.strip()
