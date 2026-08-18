from datetime import date
from sqlalchemy.orm import Session
from pm_workflow.models.summary import DailySummary
from pm_workflow.repositories.base import BaseRepository


class SummaryRepository(BaseRepository[DailySummary]):
    def __init__(self):
        super().__init__(DailySummary)

    def get_by_date(self, db: Session, date: date) -> DailySummary | None:
        return db.query(DailySummary).filter(DailySummary.date == date).first()
