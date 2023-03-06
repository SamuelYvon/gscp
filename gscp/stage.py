import subprocess


def stage() -> None:
    subprocess.run(["git", "add", "-u"], capture_output=True, check=True, timeout=10)
