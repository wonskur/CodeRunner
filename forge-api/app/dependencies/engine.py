import os
import sys
from pathlib import Path

_ENGINE_PATH = Path(__file__).resolve().parents[3] / "forge-engine"
if str(_ENGINE_PATH) not in sys.path:
    sys.path.insert(0, str(_ENGINE_PATH))

from forge_engine.runner.registry import RuntimeRegistry
from forge_engine.runner.runner import Runner
from forge_engine.sandbox.docker import SubprocessSandbox
from forge_engine.services.problem_service import ProblemService
from forge_engine.worker.worker import Worker

from .services import execution_service

problem_service = ProblemService()


def build_worker() -> Worker:
    sandbox = SubprocessSandbox()
    registry = RuntimeRegistry(sandbox)
    runner = Runner(sandbox, registry)
    worker = Worker(
        runner=runner,
        claim=execution_service.claim,
        update=execution_service.update,
    )
    return worker