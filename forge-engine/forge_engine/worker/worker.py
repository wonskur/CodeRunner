import threading
import time

from ..models.execution import ExecutionRequest
from ..models.result import ExecutionResult
from ..runner.runner import Runner


class Worker:
    def __init__(self, runner: Runner, claim, update, poll_interval_ms: int = 100):
        self.runner = runner
        self.claim = claim
        self.update = update
        self.poll_interval_ms = poll_interval_ms
        self._stop = threading.Event()
        self._thread = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        while not self._stop.is_set():
            job = self.claim()
            if job is None:
                time.sleep(self.poll_interval_ms / 1000.0)
                continue

            self.update(job.execution_id, status="RUNNING")

            req = ExecutionRequest(
                execution_id=job.execution_id,
                language=job.language,
                version=job.version,
                code=job.code,
                stdin=job.stdin,
                timeout_ms=job.timeout_ms,
                memory_mb=job.memory_mb,
            )

            result = self.runner.execute(req)

            self.update(
                job.execution_id,
                status=result.status,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.exit_code,
                signal=result.signal,
                time_ms=result.time_ms,
                memory_bytes=result.memory_bytes,
                error=(
                    {"code": result.error_code, "message": result.error_message}
                    if result.error_code
                    else None
                ),
            )