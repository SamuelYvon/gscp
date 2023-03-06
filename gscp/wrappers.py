import io
import os
import pty
import subprocess
from typing import Tuple


def stdout_of_proc(completed_proc: subprocess.CompletedProcess[bytes]) -> str:
    text = str(completed_proc.stdout, encoding="UTF-8")
    return text


def stderr_of_proc(completed_proc: subprocess.CompletedProcess[bytes]) -> str:
    text = str(completed_proc.stderr, encoding="UTF-8")
    return text


def cmd_run_in_pty(*command: str) -> Tuple[int, bytes]:
    """

    :param command: the command (with possible arguments) to execute in pty
    :return: the status code, and the raw output of the child process
    """

    all_data = io.BytesIO()

    def read(fd: int) -> bytes:
        buff = os.read(fd, 1024)
        all_data.write(buff)
        return buff

    exit_code = pty.spawn(command, master_read=read)

    all_data.seek(0, io.SEEK_SET)

    return exit_code, all_data.read()
