from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    version: Optional[str] = None
    code: str
    stdin: str = ""
    timeout_ms: Optional[int] = Field(default=None, ge=1)
    memory_mb: Optional[int] = Field(default=None, ge=1)


class ExecutionCreated(BaseModel):
    execution_id: str
    status: str


class ExecutionResult(BaseModel):
    execution_id: str
    status: str
    stdout: str = ""
    stderr: str = ""
    exit_code: Optional[int] = None
    signal: Optional[str] = None
    time_ms: Optional[int] = None
    memory_bytes: Optional[int] = None
    error: Optional[dict] = None

    language: str = ""
    version: Optional[str] = None
    code: str = ""
    stdin: str = ""
    timeout_ms: int = 2000
    memory_mb: int = 256
    reason: Optional[str] = None