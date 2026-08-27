from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from pm_workflow.api.schemas.meeting import ManualMeetingCreate
from pm_workflow.core.exceptions import LLMError, ValidationError
from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories import meeting_repo


class ManualMeetingExtraction(BaseModel):
    title: str | None = None
    date: str | None = None
    duration_minutes: int | None = None
    participants: list[str] = Field(default_factory=list)
    transcript: str | None = None


def _parse_date(raw: str | None) -> datetime:
    if raw:
        normalized = raw.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
            if parsed.tzinfo is not None:
                parsed = parsed.astimezone(UTC).replace(tzinfo=None)
            return parsed
        except ValueError:
            pass
    return datetime.now(UTC).replace(tzinfo=None)


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


class LLMMeetingService:
    def __init__(self, llm: Any, prompt_manager: Any):
        self.llm = llm
        self.prompt_manager = prompt_manager

    async def create_from_text(self, db: Any, text: str) -> Meeting:
        prompt = self.prompt_manager.load("manual_meeting").format(text=text)
        try:
            raw = await self.llm.generate(prompt, schema=ManualMeetingExtraction.model_json_schema())
        except Exception as e:
            raise LLMError(f"LLM extraction failed: {e}") from e
        try:
            extracted = ManualMeetingExtraction.model_validate(raw)
        except Exception as e:
            raise ValidationError(f"Invalid extraction response: {e}") from e

        meeting = Meeting(
            fireflies_id=f"manual-{uuid4()}",
            title=extracted.title or "Untitled Meeting",
            date=_parse_date(extracted.date),
            duration_minutes=extracted.duration_minutes,
            participants={p: True for p in extracted.participants},
            transcript=extracted.transcript or text,
            transcript_url=None,
        )
        return meeting_repo.create(db, meeting)
