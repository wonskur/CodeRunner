from typing import Optional

from ..runtimes.base import Runtime
from ..runtimes.cpp import CppRuntime
from ..runtimes.javascript import JavaScriptRuntime
from ..runtimes.python import PythonRuntime
from ..sandbox.base import Sandbox


class RuntimeRegistry:
    def __init__(self, sandbox: Sandbox):
        self._sandbox = sandbox
        self._runtimes: dict[tuple[str, str], Runtime] = {}
        for cls in (PythonRuntime, JavaScriptRuntime, CppRuntime):
            runtime = cls(sandbox)
            for version in runtime.versions:
                self._runtimes[(runtime.language, version)] = runtime

    def find(self, language: str, version: Optional[str]) -> Optional[Runtime]:
        if version:
            return self._runtimes.get((language, version))
        for (lang, _ver), runtime in self._runtimes.items():
            if lang == language:
                return runtime
        return None