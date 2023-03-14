import subprocess


def stage(no_verify: bool = False) -> None:
    cmd = ["git", "add", "-u"]
    if no_verify:
        cmd.append("-n")
    subprocess.run(cmd, capture_output=True, check=True, timeout=10)
