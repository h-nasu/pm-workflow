from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from pm_workflow.models.analysis import MeetingAnalysis
from pm_workflow.models.meeting import Meeting
from pm_workflow.models.summary import MeetingSummary
from pm_workflow.repositories import summary_repo
from pm_workflow.repositories.meeting import MeetingRepository
from pm_workflow.services.summary import SummaryService


@pytest.mark.asyncio
async def test_generate_meeting_summary_transcript_and_analysis(db):
    meeting = Meeting(
        fireflies_id="ff-1",
        title="Test Meeting",
        date=datetime(2024, 1, 15, tzinfo=UTC),
        participants={},
        transcript="This is a transcript.",
    )
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(db, meeting)
    analysis = MeetingAnalysis(
        meeting_id=meeting.id,
        decisions=[{"text": "Decided to use PostgreSQL"}],
        action_items=[{"text": "Deploy by Friday"}],
        risks=[],
        dependencies=[],
        missing_information=[],
        client_requests=[],
        requirements=[],
        open_questions=[],
        project_status={},
        suggested_next_actions=[],
        raw_response={},
        model_used="gemini",
    )
    db.add(analysis)
    db.commit()

    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={"text": "Summary text", "key_decisions": ["Use PostgreSQL"]})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    result = await service.generate_meeting_summary(db, meeting.id)

    assert result.summary_text == "Summary text"
    assert result.meeting_id == meeting.id
    mock_prompt_manager.load.assert_called_once_with("summary")


@pytest.mark.asyncio
async def test_generate_meeting_summary_transcript_only(db):
    meeting = Meeting(
        fireflies_id="ff-2",
        title="Transcript Only Meeting",
        date=datetime(2024, 1, 16, tzinfo=UTC),
        participants={},
        transcript="Just a transcript.",
    )
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(db, meeting)

    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={"text": "Transcript summary"})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    result = await service.generate_meeting_summary(db, meeting.id)

    assert result.summary_text == "Transcript summary"
    assert result.meeting_id == meeting.id


@pytest.mark.asyncio
async def test_generate_meeting_summary_analysis_only(db):
    meeting = Meeting(
        fireflies_id="ff-3",
        title="Analysis Only Meeting",
        date=datetime(2024, 1, 17, tzinfo=UTC),
        participants={},
        transcript=None,
    )
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(db, meeting)
    analysis = MeetingAnalysis(
        meeting_id=meeting.id,
        decisions=[{"text": "Use Redis"}],
        action_items=[],
        risks=[],
        dependencies=[],
        missing_information=[],
        client_requests=[],
        requirements=[],
        open_questions=[],
        project_status={},
        suggested_next_actions=[],
        raw_response={},
        model_used="gemini",
    )
    db.add(analysis)
    db.commit()

    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={"text": "Analysis summary"})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    result = await service.generate_meeting_summary(db, meeting.id)

    assert result.summary_text == "Analysis summary"
    assert result.meeting_id == meeting.id


@pytest.mark.asyncio
async def test_generate_meeting_summary_neither_transcript_nor_analysis(db):
    meeting = Meeting(
        fireflies_id="ff-4",
        title="Empty Meeting",
        date=datetime(2024, 1, 18, tzinfo=UTC),
        participants={},
        transcript=None,
    )
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(db, meeting)

    mock_llm = MagicMock()
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    with pytest.raises(ValueError, match="Cannot generate summary"):
        await service.generate_meeting_summary(db, meeting.id)


@pytest.mark.asyncio
async def test_generate_meeting_summary_idempotent_update(db):
    meeting = Meeting(
        fireflies_id="ff-5",
        title="Update Summary Meeting",
        date=datetime(2024, 1, 19, tzinfo=UTC),
        participants={},
        transcript="Original transcript.",
    )
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(db, meeting)
    summary = MeetingSummary(meeting_id=meeting.id, summary_text="Old summary", summary_json={})
    summary_repo.create(db, summary)

    mock_llm = MagicMock()
    mock_llm.generate = AsyncMock(return_value={"text": "New summary"})
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    result = await service.generate_meeting_summary(db, meeting.id)

    assert result.summary_text == "New summary"
    assert result.id == summary.id
    updated = summary_repo.get_by_meeting_id(db, meeting.id)
    assert updated is not None
    assert updated.summary_text == "New summary"


@pytest.mark.asyncio
async def test_generate_meeting_summary_meeting_not_found(db):
    mock_llm = MagicMock()
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.load.return_value = "Title: {meeting_title}\nDate: {meeting_date}\n{context}"

    service = SummaryService(llm=mock_llm, prompt_manager=mock_prompt_manager)
    with pytest.raises(ValueError, match="Meeting not found"):
        await service.generate_meeting_summary(db, UUID("00000000-0000-0000-0000-000000000000"))
