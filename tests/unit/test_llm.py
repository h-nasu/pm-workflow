from unittest.mock import AsyncMock, MagicMock

import pytest

from pm_workflow.services.analysis import AnalysisService


@pytest.fixture
def mock_llm():
    return AsyncMock()


@pytest.fixture
def mock_prompt_manager():
    pm = MagicMock()
    pm.load.return_value = "Analyze: {title}\n{date}\n{participants}\n{transcript}"
    return pm


@pytest.mark.asyncio
async def test_analysis_service(mock_llm, mock_prompt_manager):
    from pm_workflow.models.meeting import Meeting
    from datetime import datetime, timezone

    mock_llm.generate.return_value = {
        "decisions": [{"text": "Launch on Feb 15"}],
        "action_items": [],
        "risks": [],
        "dependencies": [],
        "missing_information": [],
        "client_requests": [],
        "requirements": [],
        "open_questions": [],
        "project_status": {},
        "suggested_next_actions": [],
    }

    service = AnalysisService(mock_llm, mock_prompt_manager)
    meeting = Meeting(
        fireflies_id="ff-1",
        title="Test",
        date=datetime.now(timezone.utc),
        participants={},
        transcript="We decided to launch on Feb 15.",
    )

    analysis = await service.analyze_meeting(meeting)

    assert analysis.meeting_id == meeting.id
    assert analysis.decisions == [{"text": "Launch on Feb 15"}]
    assert analysis.model_used == "AsyncMock"
