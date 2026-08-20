from ..models.execution import ExecutionRequest
from ..models.result import ExecutionResult
from ..runner.runner import Runner


class ExecutionHandler:
    def __init__(self, runner: Runner):
        self.runner = runner

    def handle(self, req: ExecutionRequest) -> ExecutionResult:
        return self.runner.execute(req)