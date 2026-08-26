from fastapi import APIRouter

from pm_workflow.api.v1.analysis import router as analysis_router
from pm_workflow.api.v1.meetings import router as meetings_router
from pm_workflow.api.v1.search import router as search_router
from pm_workflow.api.v1.summaries import router as summaries_router

api_router = APIRouter()

api_router.include_router(
    meetings_router,
    prefix="/meetings",
    tags=["meetings"],
)

api_router.include_router(
    search_router,
    prefix="/search",
    tags=["search"],
)

api_router.include_router(
    summaries_router,
    prefix="/summaries",
    tags=["summaries"],
)

api_router.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["analysis"],
)