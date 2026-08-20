from contextlib import asynccontextmanager

from fastapi import FastAPI

from .dependencies.engine import build_worker
from .routes import executions, health, problems


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker = build_worker()
    worker.start()
    yield
    worker.stop()


app = FastAPI(
    title="Forge API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(executions.router)
app.include_router(problems.router)
