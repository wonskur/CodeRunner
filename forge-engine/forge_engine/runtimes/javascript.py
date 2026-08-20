import os

from ..models.execution import ExecutionRequest
from .base import Runtime


class JavaScriptRuntime(Runtime):
    language = "javascript"
    versions = ["node20"]
    source_filename = "main.js"

    def prepare(self, workspace: str, req: ExecutionRequest) -> None:
        with open(os.path.join(workspace, "main.js"), "w", encoding="utf-8") as f:
            f.write(req.code)
        with open(os.path.join(workspace, "stdin.txt"), "w", encoding="utf-8") as f:
            f.write(req.stdin)

    def build_command(self, workspace: str, req: ExecutionRequest) -> list[str]:
        return ["node", "main.js"]