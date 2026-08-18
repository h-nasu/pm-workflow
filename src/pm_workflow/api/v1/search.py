from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from pm_workflow.api.deps import get_db
from pm_workflow.api.schemas.meeting import MeetingResponse
from pm_workflow.models.meeting import Meeting

router = APIRouter()


@router.get("/", response_model=list[MeetingResponse])
def search(q: str, db: Session = Depends(get_db)):
    query = db.query(Meeting).filter(
        or_(
            Meeting.title.ilike(f"%{q}%"),
            Meeting.transcript.ilike(f"%{q}%"),
        )
    ).limit(50)
    return query.all()
