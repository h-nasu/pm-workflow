from datetime import datetime

from sqlalchemy.orm import Session

from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories.base import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    def __init__(self):
        super().__init__(Meeting)

    def get_by_fireflies_id(self, db: Session, fireflies_id: str) -> Meeting | None:
        return db.query(Meeting).filter(Meeting.fireflies_id == fireflies_id).first()

    def list_by_date_range(
        self, db: Session, start_date: datetime, end_date: datetime, limit: int = 100, offset: int = 0
    ) -> list[Meeting]:
        return (
            db.query(Meeting)
            .filter(Meeting.date >= start_date, Meeting.date <= end_date)
            .limit(limit)
            .offset(offset)
            .all()
        )
