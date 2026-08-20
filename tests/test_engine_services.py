import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "forge-engine"))

from forge_engine.models.execution import ExecutionRequest
from forge_engine.services.execution_service import ExecutionService
from forge_engine.services.problem_service import Problem, ProblemService, TestCase
from forge_engine.services.submission_service import SubmissionService


def test_execution_create_validate_claim():
    service = ExecutionService()
    req = ExecutionRequest(
        execution_id="test1",
        language="python",
        version="3.12",
        code="print('hi')",
    )
    error = service.validate(req)
    assert error is None
    created = service.create(req)
    assert created.execution_id.startswith("exec_")
    assert service.get(created.execution_id) is not None
    claimed = service.claim()
    assert claimed is not None
    assert service.claim() is None


def test_execution_validate_errors():
    service = ExecutionService()
    req = ExecutionRequest(
        execution_id="test2",
        language="python",
        version="3.12",
        code="",
    )
    error = service.validate(req)
    assert error is not None
    assert error["code"] == "INVALID_REQUEST"


def test_execution_policy_check():
    service = ExecutionService()
    req = ExecutionRequest(
        execution_id="test3",
        language="ruby",
        version="3.0",
        code="puts 1",
    )
    rejection = service.policy_check(req)
    assert rejection is not None
    assert rejection["status"] == "REJECTED"
    assert rejection["reason"] == "LANGUAGE_NOT_SUPPORTED"


def test_problem_service():
    service = ProblemService()
    problem = Problem(
        problem_id="p1",
        title="Sum",
        description="Sum two numbers",
        test_cases=[TestCase(input="1 2", expected_output="3")],
    )
    service.create(problem)
    assert service.get("p1") == problem
    assert len(service.list_all()) == 1
    assert service.delete("p1") is True
    assert service.get("p1") is None


def test_submission_service():
    service = SubmissionService()
    sub = service.create("p1", "python", "print(1)")
    assert sub.submission_id.startswith("sub_")
    assert service.get(sub.submission_id) is sub
    assert len(service.list_by_problem("p1")) == 1