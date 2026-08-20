from dataclasses import dataclass
from typing import Optional

REQUEST_ERRORS = {"INVALID_REQUEST", "REJECTED", "UNSUPPORTED_LANGUAGE"}
CODE_ERRORS = {
    "ACCEPTED",
    "COMPILATION_ERROR",
    "RUNTIME_ERROR",
    "TIME_LIMIT",
    "MEMORY_LIMIT",
    "OUTPUT_LIMIT",
}
SYSTEM_ERRORS = {"SYSTEM_ERROR", "SANDBOX_ERROR", "RUNTIME_UNAVAILABLE", "QUEUE_ERROR"}

ALL_STATUSES = REQUEST_ERRORS | CODE_ERRORS | SYSTEM_ERRORS


@dataclass
class ExecutionRequest:
    execution_id: str
    language: str
    version: Optional[str]
    code: str
    stdin: str = ""
    timeout_ms: int = 2000
    memory_mb: int = 256
    max_output_bytes: int = 1_000_000