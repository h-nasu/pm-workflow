from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from pm_workflow.main import app

client = TestClient(app)


def test_get_meeting_summary_not_found():
    mock_db = MagicMock()
    with patch("pm_workflow.api.v1.summaries.get_db", return_value=mock_db), \
         patch("pm_workflow.api.v1.summaries.summary_repo.get_by_meeting_id", return_value=None):
        response = client.get(f"/api/v1/summaries/meeting/{UUID('00000000-0000-0000-0000-000000000000')}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Summary not found"}


@pytest.mark.asyncio
async def test_generate_meeting_summary_instantiates_service_with_dependencies():
    mock_db = MagicMock()
    mock_meeting = MagicMock()
    mock_meeting.id = UUID("12345678-1234-1234-1234-123456789012")
    mock_meeting.title = "Test Meeting"
    mock_meeting.date = date(2026, 8, 18)
    mock_meeting.transcript = "Transcript text"
    mock_meeting.analysis = None

    with patch("pm_workflow.api.v1.summaries.get_db", return_value=mock_db), \
         patch("pm_workflow.api.v1.summaries.GeminiProvider") as mock_gemini_cls, \
         patch("pm_workflow.api.v1.summaries.PromptManager") as mock_prompt_mgr_cls, \
         patch("pm_workflow.api.v1.summaries.SummaryService") as mock_service_cls, \
         patch("pm_workflow.api.v1.summaries.summary_repo.get_by_meeting_id", return_value=None):

        mock_llm = MagicMock()
        mock_prompt_manager = MagicMock()
        mock_gemini_cls.return_value = mock_llm
        mock_prompt_mgr_cls.return_value = mock_prompt_manager

        mock_summary = MagicMock()
        mock_summary.id = UUID("87654321-4321-4321-4321-210987654321")
        mock_summary.meeting_id = mock_meeting.id
        mock_summary.summary_text = "Generated summary"
        mock_service_instance = MagicMock()
        mock_service_instance.generate_meeting_summary = AsyncMock(return_value=mock_summary)
        mock_service_cls.return_value = mock_service_instance

        from pm_workflow.api.v1.summaries import generate_meeting_summary
        await generate_meeting_summary(meeting_id=mock_meeting.id, db=mock_db)

        mock_gemini_cls.assert_called_once()
        mock_prompt_mgr_cls.assert_called_once()
        mock_service_cls.assert_called_once_with(llm=mock_llm, prompt_manager=mock_prompt_manager)
