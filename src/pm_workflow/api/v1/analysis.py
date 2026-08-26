from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from pm_workflow.api.deps import get_db
from pm_workflow.api.schemas.analysis import AnalysisResponse
from pm_workflow.repositories import analysis_repo

router = APIRouter()


@router.get("/", response_model=list[AnalysisResponse])
def list_analyses(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    if start_date and end_date:
        analyses = analysis_repo.list_by_date_range(db, start_date=start_date, end_date=end_date)
    else:
        analyses = analysis_repo.get_all(db, limit=limit, offset=offset)
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/{meeting_id}", response_model=AnalysisResponse)
def get_analysis(meeting_id: UUID, db: Session = Depends(get_db)):
    analysis = analysis_repo.get_by_meeting_id(db, meeting_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse.model_validate(analysis)
