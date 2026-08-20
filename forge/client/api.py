import urllib.error
import urllib.request
import json
from typing import Optional


class ForgeClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def execute(self, language: str, code: str, stdin: str = "",
                version: Optional[str] = None,
                timeout_ms: Optional[int] = None,
                memory_mb: Optional[int] = None) -> dict:
        payload = {
            "language": language,
            "code": code,
            "stdin": stdin,
        }
        if version:
            payload["version"] = version
        if timeout_ms:
            payload["timeout_ms"] = timeout_ms
        if memory_mb:
            payload["memory_mb"] = memory_mb

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.base_url + "/api/v1/executions",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_result(self, execution_id: str) -> dict:
        req = urllib.request.Request(
            self.base_url + f"/api/v1/executions/{execution_id}",
            method="GET",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def health(self) -> dict:
        req = urllib.request.Request(
            self.base_url + "/health",
            method="GET",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))