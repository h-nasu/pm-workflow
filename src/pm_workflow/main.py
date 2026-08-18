from fastapi import FastAPI

from pm_workflow.api.v1 import api_router
from pm_workflow.config import get_settings

settings = get_settings()

app = FastAPI(
    title="PM Workflow API",
    description="AI-first Project Management System",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")
