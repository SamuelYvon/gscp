import subprocess


def stage() -> None:
    cmd = ["git", "add", "-u"]
    subprocess.run(cmd, capture_output=True, check=True, timeout=10)
