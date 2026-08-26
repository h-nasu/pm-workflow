from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MeetingSummaryResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    summary_text: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
