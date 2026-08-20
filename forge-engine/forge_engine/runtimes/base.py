from abc import ABC, abstractmethod
from typing import Optional

from ..models.execution import ExecutionRequest
from ..models.result import ExecutionResult
from ..sandbox.base import Sandbox, SandboxResult


class Runtime(ABC):
    language: str = ""
    versions: list[str] = []
    source_filename: str = "main"

    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @abstractmethod
    def prepare(self, workspace: str, req: ExecutionRequest) -> None:
        ...

    @abstractmethod
    def build_command(self, workspace: str, req: ExecutionRequest) -> list[str]:
        ...

    def compile(self, workspace: str, req: ExecutionRequest) -> Optional[ExecutionResult]:
        return None

    def map_result(self, req: ExecutionRequest, raw: SandboxResult) -> ExecutionResult:
        if raw.error_code:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="SYSTEM_ERROR",
                error_code=raw.error_code,
                error_message=raw.error_message,
                time_ms=raw.time_ms,
            )
        if raw.timed_out:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="TIME_LIMIT",
                stdout=raw.stdout,
                stderr=raw.stderr,
                time_ms=raw.time_ms,
            )
        if raw.memory_exceeded:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="MEMORY_LIMIT",
                stdout=raw.stdout,
                stderr=raw.stderr,
                time_ms=raw.time_ms,
            )
        if raw.output_exceeded:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="OUTPUT_LIMIT",
                stdout=raw.stdout,
                stderr=raw.stderr,
                time_ms=raw.time_ms,
            )
        if raw.signal is not None:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="RUNTIME_ERROR",
                stdout=raw.stdout,
                stderr=raw.stderr,
                signal=raw.signal,
                time_ms=raw.time_ms,
            )
        if raw.exit_code != 0:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="RUNTIME_ERROR",
                stdout=raw.stdout,
                stderr=raw.stderr,
                exit_code=raw.exit_code,
                time_ms=raw.time_ms,
            )
        return ExecutionResult(
            execution_id=req.execution_id,
            status="ACCEPTED",
            stdout=raw.stdout,
            stderr=raw.stderr,
            exit_code=0,
            time_ms=raw.time_ms,
        )