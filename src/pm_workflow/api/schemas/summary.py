from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class DailySummaryResponse(BaseModel):
    id: UUID
    date: date
    summary_text: str
    meeting_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
