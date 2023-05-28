import subprocess

from rich.console import Console


def stage(_console: Console) -> None:
    cmd = ["git", "add", "-u"]
    subprocess.run(cmd, capture_output=True, check=True, timeout=10)
