from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pm_workflow.api.deps import get_db
from pm_workflow.api.schemas.summary import DailySummaryResponse
from pm_workflow.integrations.llm.gemini import GeminiProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.repositories import meeting_repo, summary_repo
from pm_workflow.services.summary import SummaryService

router = APIRouter()


@router.get("/daily", response_model=DailySummaryResponse)
def get_daily_summary(target_date: date, db: Session = Depends(get_db)):
    summary = summary_repo.get_by_date(db, target_date)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return DailySummaryResponse.model_validate(summary)


@router.post("/daily/generate", response_model=DailySummaryResponse)
async def generate_daily_summary(target_date: date, db: Session = Depends(get_db)):
    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())
    meetings = meeting_repo.list_by_date_range(db, start_date=start, end_date=end)
    llm = GeminiProvider()
    prompt_manager = PromptManager()
    summary_service = SummaryService(llm=llm, prompt_manager=prompt_manager)
    try:
        summary = await summary_service.generate_daily_summary(db, target_date, meetings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return DailySummaryResponse.model_validate(summary)
