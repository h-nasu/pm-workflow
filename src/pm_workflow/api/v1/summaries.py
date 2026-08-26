from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pm_workflow.api.deps import get_db
from pm_workflow.api.schemas.summary import MeetingSummaryResponse
from pm_workflow.integrations.llm.gemini import GeminiProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.repositories import summary_repo
from pm_workflow.services.summary import SummaryService

router = APIRouter()


@router.get("/meeting/{meeting_id}", response_model=MeetingSummaryResponse)
def get_meeting_summary(meeting_id: UUID, db: Session = Depends(get_db)):
    summary = summary_repo.get_by_meeting_id(db, meeting_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return MeetingSummaryResponse.model_validate(summary)


@router.post("/meeting/{meeting_id}/generate", response_model=MeetingSummaryResponse)
async def generate_meeting_summary(meeting_id: UUID, db: Session = Depends(get_db)):
    llm = GeminiProvider()
    prompt_manager = PromptManager()
    summary_service = SummaryService(llm=llm, prompt_manager=prompt_manager)
    try:
        summary = await summary_service.generate_meeting_summary(db, meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return MeetingSummaryResponse.model_validate(summary)
