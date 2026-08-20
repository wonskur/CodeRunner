import os

from ..models.execution import ExecutionRequest
from ..models.result import ExecutionResult
from .base import Runtime


class CppRuntime(Runtime):
    language = "cpp"
    versions = ["c++17"]
    source_filename = "main.cpp"

    def prepare(self, workspace: str, req: ExecutionRequest) -> None:
        with open(os.path.join(workspace, "main.cpp"), "w", encoding="utf-8") as f:
            f.write(req.code)
        with open(os.path.join(workspace, "stdin.txt"), "w", encoding="utf-8") as f:
            f.write(req.stdin)

    def build_command(self, workspace: str, req: ExecutionRequest) -> list[str]:
        return ["./main"]

    def compile(self, workspace: str, req: ExecutionRequest) -> ExecutionResult | None:
        raw = self.sandbox.run(
            command=["g++", "-std=c++17", "-O2", "-o", "main", "main.cpp"],
            cwd=workspace,
            stdin="",
            timeout_ms=10_000,
            memory_mb=req.memory_mb,
            max_output_bytes=req.max_output_bytes,
        )
        if raw.error_code:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="SYSTEM_ERROR",
                error_code=raw.error_code,
                error_message=raw.error_message,
                time_ms=raw.time_ms,
            )
        if raw.exit_code != 0:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="COMPILATION_ERROR",
                stdout=raw.stdout,
                stderr=raw.stderr,
                exit_code=raw.exit_code,
                time_ms=raw.time_ms,
            )
        return None