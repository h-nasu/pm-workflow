from uuid import UUID

from sqlalchemy.orm import Session

from pm_workflow.models.summary import MeetingSummary
from pm_workflow.repositories.base import BaseRepository


class SummaryRepository(BaseRepository[MeetingSummary]):
    def __init__(self):
        super().__init__(MeetingSummary)

    def get_by_meeting_id(self, db: Session, meeting_id: UUID) -> MeetingSummary | None:
        return db.query(MeetingSummary).filter(MeetingSummary.meeting_id == meeting_id).first()
