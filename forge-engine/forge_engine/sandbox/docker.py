import subprocess
import time

from .base import Sandbox, SandboxResult


class SubprocessSandbox(Sandbox):
    def run(
        self,
        command: list[str],
        cwd: str,
        stdin: str,
        timeout_ms: int,
        memory_mb: int,
        max_output_bytes: int,
    ) -> SandboxResult:
        start = time.monotonic()
        timed_out = False
        output_exceeded = False
        signal_received = None
        exit_code = None
        stdout = ""
        stderr = ""

        try:
            proc = subprocess.Popen(
                command,
                cwd=cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            return SandboxResult(
                stdout="",
                stderr="",
                exit_code=None,
                signal=None,
                time_ms=0,
                memory_bytes=None,
                error_code="RUNTIME_UNAVAILABLE",
                error_message=f"command not found: {command[0]}",
            )
        except Exception as exc:
            return SandboxResult(
                stdout="",
                stderr="",
                exit_code=None,
                signal=None,
                time_ms=0,
                memory_bytes=None,
                error_code="SANDBOX_ERROR",
                error_message=str(exc),
            )

        try:
            stdout, stderr = proc.communicate(input=stdin, timeout=timeout_ms / 1000.0)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            stdout, stderr = proc.communicate()
        finally:
            elapsed_ms = int((time.monotonic() - start) * 1000)

        if proc.returncode is not None:
            if proc.returncode < 0:
                signal_received = -proc.returncode
                exit_code = None
            else:
                exit_code = proc.returncode

        if len(stdout.encode("utf-8")) > max_output_bytes:
            output_exceeded = True
            stdout = stdout[: max_output_bytes // 4]
        if len(stderr.encode("utf-8")) > max_output_bytes:
            stderr = stderr[: max_output_bytes // 4]

        return SandboxResult(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            signal=signal_received,
            time_ms=elapsed_ms,
            memory_bytes=None,
            timed_out=timed_out,
            memory_exceeded=False,
            output_exceeded=output_exceeded,
        )