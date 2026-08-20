from fastapi import APIRouter, HTTPException, Response

from ..dependencies.services import execution_service
from ..schemas.execution import ExecutionCreated, ExecutionRequest, ExecutionResult

router = APIRouter(prefix="/api/v1/executions", tags=["executions"])


@router.post(
    "",
    status_code=202,
    response_model=ExecutionCreated,
)
async def create_execution(req: ExecutionRequest, response: Response):
    validation_error = execution_service.validate(req)
    if validation_error:
        raise HTTPException(
            status_code=422,
            detail={
                "status": "invalid_request",
                "error": validation_error,
            },
        )

    rejection = execution_service.policy_check(req)
    if rejection:
        raise HTTPException(
            status_code=403,
            detail={
                "execution_id": None,
                "status": rejection["status"],
                "reason": rejection["reason"],
            },
        )

    execution = execution_service.create(req)
    response.status_code = 202
    return execution


@router.get("/{execution_id}", response_model=ExecutionResult)
async def get_execution(execution_id: str):
    execution = execution_service.get(execution_id)
    if execution is None:
        raise HTTPException(status_code=404, detail="execution not found")
    return execution