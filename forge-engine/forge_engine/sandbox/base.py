from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: Optional[int]
    signal: Optional[str]
    time_ms: int
    memory_bytes: Optional[int]
    timed_out: bool = False
    memory_exceeded: bool = False
    output_exceeded: bool = False
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class Sandbox(ABC):
    @abstractmethod
    def run(
        self,
        command: list[str],
        cwd: str,
        stdin: str,
        timeout_ms: int,
        memory_mb: int,
        max_output_bytes: int,
    ) -> SandboxResult:
        ...