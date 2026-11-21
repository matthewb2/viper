import codecs
import locale
import os
import platform
import subprocess
import sys
from io import BytesIO

import pexpect
import psutil


def _get_preferred_output_encoding() -> str:
    """Return the most likely encoding for subprocess console output."""
    if platform.system() == "Windows":
        try:
            import ctypes

            cp = ctypes.windll.kernel32.GetConsoleOutputCP()
            if cp:
                return f"cp{cp}"
        except Exception:
            pass
        try:
            cp = ctypes.windll.kernel32.GetOEMCP()
            if cp:
                return f"cp{cp}"
        except Exception:
            pass
    return locale.getpreferredencoding(False) or getattr(sys.stdout, "encoding", None) or "utf-8"


def decode_cmd_output(raw_bytes: bytes, preferred_encoding: str | None = None) -> str:
    if not raw_bytes:
        return ""
    encodings = []
    for enc in (
        "utf-8",
        preferred_encoding,
        locale.getpreferredencoding(False),
        getattr(sys.stdout, "encoding", None),
    ):
        if enc and enc not in encodings:
            encodings.append(enc)
    if platform.system() == "Windows" and "cp949" not in encodings:
        encodings.append("cp949")
    for enc in encodings:
        try:
            return raw_bytes.decode(enc)
        except Exception:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def run_cmd(command, verbose=False, error_print=None, cwd=None):
    try:
        if sys.stdin.isatty() and hasattr(pexpect, "spawn") and platform.system() != "Windows":
            return run_cmd_pexpect(command, verbose, cwd)

        return run_cmd_subprocess(command, verbose, cwd)
    except OSError as e:
        error_message = f"Error occurred while running command '{command}': {str(e)}"
        if error_print is None:
            print(error_message)
        else:
            error_print(error_message)
        return 1, error_message


def get_windows_parent_process_name():
    try:
        current_process = psutil.Process()
        while True:
            parent = current_process.parent()
            if parent is None:
                break
            parent_name = parent.name().lower()
            if parent_name in ["powershell.exe", "cmd.exe"]:
                return parent_name
            current_process = parent
        return None
    except Exception:
        return None


def _write_safe_stdout(text: str, stdout_enc: str):
    if not text:
        return
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        safe_text = text.encode(stdout_enc, errors="backslashreplace").decode(
            stdout_enc, errors="replace"
        )
        sys.stdout.write(safe_text)
    sys.stdout.flush()


def run_cmd_subprocess(command, verbose=False, cwd=None, encoding=sys.stdout.encoding):
    if verbose:
        print("Using run_cmd_subprocess:", command)

    try:
        shell = os.environ.get("SHELL", "/bin/sh")
        parent_process = None

        # Determine the appropriate shell
        if platform.system() == "Windows":
            parent_process = get_windows_parent_process_name()
            if parent_process == "powershell.exe":
                command = f"powershell -Command {command}"

        if verbose:
            print("Running command:", command)
            print("SHELL:", shell)
            if platform.system() == "Windows":
                print("Parent process:", parent_process)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
            shell=True,
            bufsize=0,
            cwd=cwd,
        )

        raw_chunks = []
        preferred_encoding = _get_preferred_output_encoding()
        inc_decoder = codecs.getincrementaldecoder(preferred_encoding)(errors="replace")
        stdout_enc = (
            getattr(sys.stdout, "encoding", None) or encoding or preferred_encoding or "utf-8"
        )

        while True:
            chunk = process.stdout.read(256)
            if not chunk:
                break
            raw_chunks.append(chunk)
            stream_text = inc_decoder.decode(chunk, final=False)
            _write_safe_stdout(stream_text, stdout_enc)

        tail_text = inc_decoder.decode(b"", final=True)
        _write_safe_stdout(tail_text, stdout_enc)

        process.wait()
        decoded_output = decode_cmd_output(b"".join(raw_chunks), preferred_encoding)
        return process.returncode, decoded_output
    except Exception as e:
        return 1, str(e)


def run_cmd_pexpect(command, verbose=False, cwd=None):
    """
    Run a shell command interactively using pexpect, capturing all output.

    :param command: The command to run as a string.
    :param verbose: If True, print output in real-time.
    :return: A tuple containing (exit_status, output)
    """
    if verbose:
        print("Using run_cmd_pexpect:", command)

    output = BytesIO()

    def output_callback(b):
        output.write(b)
        return b

    try:
        # Use the SHELL environment variable, falling back to /bin/sh if not set
        shell = os.environ.get("SHELL", "/bin/sh")
        if verbose:
            print("With shell:", shell)

        if os.path.exists(shell):
            # Use the shell from SHELL environment variable
            if verbose:
                print("Running pexpect.spawn with shell:", shell)
            child = pexpect.spawn(shell, args=["-i", "-c", command], encoding="utf-8", cwd=cwd)
        else:
            # Fall back to spawning the command directly
            if verbose:
                print("Running pexpect.spawn without shell.")
            child = pexpect.spawn(command, encoding="utf-8", cwd=cwd)

        # Transfer control to the user, capturing output
        child.interact(output_filter=output_callback)

        # Wait for the command to finish and get the exit status
        child.close()
        return child.exitstatus, output.getvalue().decode("utf-8", errors="replace")

    except (pexpect.ExceptionPexpect, TypeError, ValueError) as e:
        error_msg = f"Error running command {command}: {e}"
        return 1, error_msg