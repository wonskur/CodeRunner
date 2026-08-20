from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestCase:
    __test__ = False
    input: str
    expected_output: str
    is_sample: bool = False


@dataclass
class Problem:
    problem_id: str
    title: str
    description: str
    time_limit_ms: int = 2000
    memory_limit_mb: int = 256
    test_cases: list[TestCase] = field(default_factory=list)


class ProblemService:
    def __init__(self) -> None:
        self._problems: dict[str, Problem] = {}

    def create(self, problem: Problem) -> Problem:
        self._problems[problem.problem_id] = problem
        return problem

    def get(self, problem_id: str) -> Optional[Problem]:
        return self._problems.get(problem_id)

    def list_all(self) -> list[Problem]:
        return list(self._problems.values())

    def delete(self, problem_id: str) -> bool:
        return self._problems.pop(problem_id, None) is not None


problem_service = ProblemService()