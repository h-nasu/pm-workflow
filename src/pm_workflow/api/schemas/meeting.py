from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MeetingBase(BaseModel):
    title: str
    date: datetime
    duration_minutes: int | None = None
    participants: dict[str, Any] = Field(default_factory=dict)
    transcript: str | None = None
    transcript_url: str | None = None


class MeetingCreate(MeetingBase):
    fireflies_id: str


class MeetingResponse(MeetingBase):
    id: UUID
    fireflies_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
