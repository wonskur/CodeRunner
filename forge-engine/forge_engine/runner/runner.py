import shutil
import tempfile

from ..models.execution import ExecutionRequest
from ..models.result import ExecutionResult
from ..sandbox.base import Sandbox


class Runner:
    def __init__(self, sandbox: Sandbox, registry):
        self.sandbox = sandbox
        self.registry = registry

    def execute(self, req: ExecutionRequest) -> ExecutionResult:
        runtime = self.registry.find(req.language, req.version)
        if runtime is None:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="REJECTED",
                error_code="UNSUPPORTED_LANGUAGE",
                error_message=f"language '{req.language}' is not supported",
            )

        workspace = tempfile.mkdtemp(prefix=f"forge_{req.execution_id}_")
        try:
            runtime.prepare(workspace, req)

            compile_result = runtime.compile(workspace, req)
            if compile_result is not None:
                return compile_result

            raw = self.sandbox.run(
                command=runtime.build_command(workspace, req),
                cwd=workspace,
                stdin=req.stdin,
                timeout_ms=req.timeout_ms,
                memory_mb=req.memory_mb,
                max_output_bytes=req.max_output_bytes,
            )

            return runtime.map_result(req, raw)
        except Exception as exc:
            return ExecutionResult(
                execution_id=req.execution_id,
                status="SYSTEM_ERROR",
                error_code="SANDBOX_ERROR",
                error_message=str(exc),
            )
        finally:
            shutil.rmtree(workspace, ignore_errors=True)