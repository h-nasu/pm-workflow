from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MeetingBase(BaseModel):
    title: str
    date: datetime
    duration_minutes: int | None = None
    participants: dict[str, Any] = Field(default_factory=dict, json_schema_extra={"example": {"personA": True}})
    transcript: str | None = None
    transcript_url: str | None = None


class MeetingCreate(MeetingBase):
    fireflies_id: str


class ManualMeetingCreate(BaseModel):
    transcript: str = Field(..., min_length=1, description="Meeting transcript / notes, stored directly")
    title: str | None = Field(None, description="Meeting title; derived from transcript when omitted")
    date: datetime | None = Field(None, description="Meeting date (ISO 8601); defaults to now when omitted")
    duration_minutes: int | None = None
    participants: dict[str, Any] = Field(default_factory=dict, json_schema_extra={"example": {"personA": True}})


class MeetingExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw meeting text for LLM extraction")


class MeetingResponse(MeetingBase):
    id: UUID
    fireflies_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
