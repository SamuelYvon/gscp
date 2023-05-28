import fcntl
import io
import os
import pty
import struct
import subprocess
import termios
from functools import partial
from typing import Tuple


def stdout_of_proc(completed_proc: subprocess.CompletedProcess[bytes]) -> str:
    text = str(completed_proc.stdout, encoding="UTF-8")
    return text


def stderr_of_proc(completed_proc: subprocess.CompletedProcess[bytes]) -> str:
    text = str(completed_proc.stderr, encoding="UTF-8")
    return text


def _setwinsize(*, fd: int, rows: int, cols: int) -> None:
    """
    Set the window size for the file descriptor;

    This is taken verbatim from commit
    https://github.com/pexpect/ptyprocess/commit/94f4d2c6c2445f538182ac8970571c5faae7d37f

    Licensed under

    ```
    ISC LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2013-2014, Pexpect development team
    Copyright (c) 2012, Noah Spurrier <noah@noah.org>

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    ```

    """

    # Some very old platforms have a bug that causes the value for
    # termios.TIOCSWINSZ to be truncated. There was a hack here to work
    # around this, but it caused problems with newer platforms so has been
    # removed. For details see https://github.com/pexpect/pexpect/issues/39
    TIOCSWINSZ = getattr(termios, "TIOCSWINSZ", -2146929561)
    # Note, assume ws_xpixel and ws_ypixel are zero.
    s = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(fd, TIOCSWINSZ, s)


def cmd_run_in_pty(*command: str) -> Tuple[int, bytes]:
    """

    :param command: the command (with possible arguments) to execute in pty
    :return: the status code, and the raw output of the child process
    """

    all_data = io.BytesIO()
    cols, rows = os.get_terminal_size()

    set_win_size = partial(_setwinsize, cols=cols, rows=rows)

    def read(fd: int) -> bytes:
        set_win_size(fd=fd)
        buff = os.read(fd, 1024)
        all_data.write(buff)
        return buff

    exit_code = pty.spawn(command, master_read=read)

    all_data.seek(0, io.SEEK_SET)

    return exit_code, all_data.read()
