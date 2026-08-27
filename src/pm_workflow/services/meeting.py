from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pm_workflow.api.schemas.meeting import ManualMeetingCreate
from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories import meeting_repo


def _derive_title(transcript: str) -> str:
    for line in transcript.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:200]
    return "Untitled Meeting"


def _normalize_date(value: datetime | None) -> datetime:
    if value is None:
        return datetime.now(UTC).replace(tzinfo=None)
    if value.tzinfo is not None:
        return value.astimezone(UTC).replace(tzinfo=None)
    return value


class ManualMeetingService:
    def create_from_payload(self, db: Any, payload: ManualMeetingCreate) -> Meeting:
        meeting = Meeting(
            fireflies_id=f"manual-{uuid4()}",
            title=payload.title or _derive_title(payload.transcript),
            date=_normalize_date(payload.date),
            duration_minutes=payload.duration_minutes,
            participants=payload.participants or {},
            transcript=payload.transcript,
            transcript_url=None,
        )
        return meeting_repo.create(db, meeting)
