import subprocess

from gscp.wrappers import stdout_of_proc


def git_current_branch() -> str:
    command = ["git", "branch", "--show-current"]
    out = stdout_of_proc(
        subprocess.run(command, capture_output=True, check=True, timeout=10)
    )
    return out.strip()


def git_is_in_repo() -> bool:
    command = ["git", "rev-parse", "--is-inside-work-tree"]
    out = subprocess.run(command, capture_output=True, check=False, timeout=10)
    ok = len(out.stdout) > 0
    return ok
