from fastapi import APIRouter, HTTPException

from ..dependencies.engine import problem_service
from forge_engine.services.problem_service import Problem, TestCase

router = APIRouter(prefix="/api/v1/problems", tags=["problems"])


@router.post("", status_code=201)
async def create_problem(payload: dict):
    problem_id = payload.get("problem_id")
    title = payload.get("title")
    description = payload.get("description")
    if not problem_id or not title or not description:
        raise HTTPException(status_code=422, detail="problem_id, title, description are required")

    test_cases = [
        TestCase(
            input=tc.get("input", ""),
            expected_output=tc.get("expected_output", ""),
            is_sample=tc.get("is_sample", False),
        )
        for tc in payload.get("test_cases", [])
    ]

    problem = Problem(
        problem_id=problem_id,
        title=title,
        description=description,
        time_limit_ms=payload.get("time_limit_ms", 2000),
        memory_limit_mb=payload.get("memory_limit_mb", 256),
        test_cases=test_cases,
    )
    problem_service.create(problem)
    return problem


@router.get("/{problem_id}")
async def get_problem(problem_id: str):
    problem = problem_service.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="problem not found")
    return problem


@router.get("")
async def list_problems():
    return problem_service.list_all()