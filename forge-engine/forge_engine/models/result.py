from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionResult:
    execution_id: str
    status: str
    stdout: str = ""
    stderr: str = ""
    exit_code: Optional[int] = None
    signal: Optional[str] = None
    time_ms: Optional[int] = None
    memory_bytes: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "signal": self.signal,
            "time_ms": self.time_ms,
            "memory_bytes": self.memory_bytes,
            "error": (
                {"code": self.error_code, "message": self.error_message}
                if self.error_code
                else None
            ),
        }