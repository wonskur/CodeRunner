import threading
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Submission:
    submission_id: str
    problem_id: str
    language: str
    code: str
    status: str = "PENDING"
    execution_id: Optional[str] = None


class SubmissionService:
    def __init__(self) -> None:
        self._submissions: dict[str, Submission] = {}
        self._lock = threading.Lock()

    def create(self, problem_id: str, language: str, code: str) -> Submission:
        submission = Submission(
            submission_id="sub_" + uuid.uuid4().hex[:8],
            problem_id=problem_id,
            language=language,
            code=code,
        )
        with self._lock:
            self._submissions[submission.submission_id] = submission
        return submission

    def get(self, submission_id: str) -> Optional[Submission]:
        with self._lock:
            return self._submissions.get(submission_id)

    def list_by_problem(self, problem_id: str) -> list[Submission]:
        with self._lock:
            return [
                s for s in self._submissions.values() if s.problem_id == problem_id
            ]


submission_service = SubmissionService()