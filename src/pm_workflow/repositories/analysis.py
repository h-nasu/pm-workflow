from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from pm_workflow.models.analysis import MeetingAnalysis
from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[MeetingAnalysis]):
    def __init__(self):
        super().__init__(MeetingAnalysis)

    def get_by_meeting_id(self, db: Session, meeting_id: UUID) -> MeetingAnalysis | None:
        return db.query(MeetingAnalysis).filter(MeetingAnalysis.meeting_id == meeting_id).first()

    def list_by_date_range(self, db: Session, start_date: datetime, end_date: datetime) -> list[MeetingAnalysis]:
        return (
            db.query(MeetingAnalysis)
            .join(Meeting, MeetingAnalysis.meeting_id == Meeting.id)
            .filter(Meeting.date >= start_date, Meeting.date <= end_date)
            .all()
        )
