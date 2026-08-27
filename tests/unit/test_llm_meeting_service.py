from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from pm_workflow.core.exceptions import ValidationError
from pm_workflow.repositories.meeting import MeetingRepository
from pm_workflow.services.meeting import LLMMeetingService, _parse_date


@pytest.mark.asyncio
async def test_create_from_text_creates_meeting(db):
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(
        return_value={
            "title": "Sprint Planning",
            "date": "2024-03-10T14:30:00",
            "duration_minutes": 60,
            "participants": ["Alice", "Bob"],
            "transcript": "Discussed roadmap.",
        }
    )
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Meeting text: {text}"

    service = LLMMeetingService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    meeting = await service.create_from_text(db, "Some raw text")

    assert meeting.title == "Sprint Planning"
    assert meeting.fireflies_id.startswith("manual-")
    assert meeting.participants == {"Alice": True, "Bob": True}
    assert meeting.transcript == "Discussed roadmap."
    assert isinstance(meeting.date, datetime)

    repo = MeetingRepository()
    fetched = repo.get_by_fireflies_id(db, meeting.fireflies_id)
    assert fetched is not None
    assert fetched.id == meeting.id


@pytest.mark.asyncio
async def test_create_from_text_defaults_when_fields_missing(db):
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Meeting text: {text}"

    service = LLMMeetingService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    meeting = await service.create_from_text(db, "raw text payload")

    assert meeting.title == "Untitled Meeting"
    assert meeting.transcript == "raw text payload"
    assert meeting.participants == {}
    assert meeting.fireflies_id.startswith("manual-")


@pytest.mark.asyncio
async def test_create_from_text_raises_validation_error_on_bad_response(db):
    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={"duration_minutes": "not-an-int"})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Meeting text: {text}"

    service = LLMMeetingService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    with pytest.raises(ValidationError):
        await service.create_from_text(db, "text")


def test_parse_date_valid_iso():
    parsed = _parse_date("2024-03-10T14:30:00")
    assert parsed.year == 2024
    assert parsed.month == 3


def test_parse_date_handles_z_suffix_as_naive_utc():
    parsed = _parse_date("2024-03-10T14:30:00Z")
    assert parsed.year == 2024
    assert parsed.tzinfo is None


def test_parse_date_falls_back_to_now():
    assert isinstance(_parse_date(None), datetime)
    assert isinstance(_parse_date("not-a-date"), datetime)
