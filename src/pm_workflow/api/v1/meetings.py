from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from tenacity import RetryError

from pm_workflow.api.deps import get_db
from pm_workflow.api.schemas.analysis import AnalysisResponse
from pm_workflow.api.schemas.meeting import MeetingResponse
from pm_workflow.core.exceptions import ExternalAPIError
from pm_workflow.integrations.llm.gemini import GeminiProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories import analysis_repo, meeting_repo
from pm_workflow.services.analysis import AnalysisService
from pm_workflow.services.sync import SyncService

router = APIRouter()


@router.get("/", response_model=list[MeetingResponse])
def list_meetings(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    return meeting_repo.get_all(db, limit=limit, offset=offset)


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("/sync", summary="Sync meetings from Fireflies")
async def sync_meetings(
    start_date: datetime = Query(..., description="Start of the date range to sync (ISO 8601, e.g. 2024-01-01T00:00:00)"),
    end_date: datetime = Query(..., description="End of the date range to sync (ISO 8601, e.g. 2024-12-31T23:59:59)"),
    db: Session = Depends(get_db),
):
    llm = GeminiProvider()
    prompt_manager = PromptManager()
    analysis_service = AnalysisService(llm=llm, prompt_manager=prompt_manager)
    sync_service = SyncService(analysis_service=analysis_service)
    try:
        synced = await sync_service.sync_range(db, start_date, end_date)
    except RetryError as e:
        cause = e.__cause__
        if isinstance(cause, ExternalAPIError):
            raise HTTPException(status_code=502, detail=str(cause)) from e
        raise HTTPException(status_code=502, detail=f"Fireflies API request failed after retries: {cause}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return {"synced": len(synced)}


@router.post("/{meeting_id}/analyze", response_model=AnalysisResponse)
async def analyze_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    llm = GeminiProvider()
    prompt_manager = PromptManager()
    analysis_service = AnalysisService(llm=llm, prompt_manager=prompt_manager)
    try:
        analysis = await analysis_service.analyze_meeting(meeting)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    analysis_repo.create(db, analysis)
    db.commit()
    db.refresh(analysis)
    return AnalysisResponse.model_validate(analysis)
