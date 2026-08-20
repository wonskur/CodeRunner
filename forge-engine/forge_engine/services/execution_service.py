import threading
import uuid
from collections import deque
from typing import Optional

from ..models.execution import ExecutionRequest

SUPPORTED_LANGUAGES = {
    "python": ["3.12", "3.11"],
    "javascript": ["node20"],
    "cpp": ["c++17"],
}

POLICY = {
    "max_code_bytes": 1_000_000,
    "max_stdin_bytes": 1_000_000,
    "max_timeout_ms": 30_000,
    "max_memory_mb": 512,
    "default_timeout_ms": 2_000,
    "default_memory_mb": 256,
    "max_output_bytes": 1_000_000,
}


class ExecutionService:
    def __init__(self) -> None:
        self._queue: "deque[str]" = deque()
        self._store: "dict[str, ExecutionRequest]" = {}
        self._lock = threading.Lock()

    def validate(self, req: ExecutionRequest) -> Optional[dict]:
        if not req.language or not req.language.strip():
            return {"code": "INVALID_REQUEST", "message": "language is required"}
        if not req.code:
            return {"code": "INVALID_REQUEST", "message": "code is required"}
        if len(req.code.encode("utf-8")) > POLICY["max_code_bytes"]:
            return {"code": "INVALID_REQUEST", "message": "code is too large"}
        if len(req.stdin.encode("utf-8")) > POLICY["max_stdin_bytes"]:
            return {"code": "INVALID_REQUEST", "message": "stdin is too large"}
        if req.timeout_ms and req.timeout_ms > POLICY["max_timeout_ms"]:
            return {"code": "INVALID_REQUEST", "message": "timeout_ms is too large"}
        if req.memory_mb and req.memory_mb > POLICY["max_memory_mb"]:
            return {"code": "INVALID_REQUEST", "message": "memory_mb is too large"}
        return None

    def policy_check(self, req: ExecutionRequest) -> Optional[dict]:
        if req.language not in SUPPORTED_LANGUAGES:
            return {"status": "REJECTED", "reason": "LANGUAGE_NOT_SUPPORTED"}
        if req.version and req.version not in SUPPORTED_LANGUAGES[req.language]:
            return {"status": "REJECTED", "reason": "VERSION_NOT_SUPPORTED"}
        return None

    def create(self, req: ExecutionRequest) -> ExecutionRequest:
        execution_id = "exec_" + uuid.uuid4().hex[:8]
        stored = ExecutionRequest(
            execution_id=execution_id,
            language=req.language,
            version=req.version,
            code=req.code,
            stdin=req.stdin,
            timeout_ms=req.timeout_ms or POLICY["default_timeout_ms"],
            memory_mb=req.memory_mb or POLICY["default_memory_mb"],
            max_output_bytes=req.max_output_bytes or POLICY["max_output_bytes"],
        )
        with self._lock:
            self._store[execution_id] = stored
            self._queue.append(execution_id)
        return stored

    def get(self, execution_id: str) -> Optional[ExecutionRequest]:
        with self._lock:
            return self._store.get(execution_id)

    def claim(self) -> Optional[ExecutionRequest]:
        with self._lock:
            if not self._queue:
                return None
            execution_id = self._queue.popleft()
            return self._store.get(execution_id)


execution_service = ExecutionService()