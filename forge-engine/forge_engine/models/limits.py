from dataclasses import dataclass


@dataclass
class Limits:
    timeout_ms: int = 2000
    memory_mb: int = 256
    max_output_bytes: int = 1_000_000
    max_processes: int = 32