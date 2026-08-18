from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pm_workflow.api.v1.summaries import generate_daily_summary


@pytest.mark.asyncio
async def test_generate_daily_summary_instantiates_service_with_dependencies():
    mock_db = MagicMock()
    mock_meeting = MagicMock()
    mock_meeting.title = "Test Meeting"
    mock_meeting.date = date(2026, 8, 18)

    with patch("pm_workflow.api.v1.summaries.GeminiProvider") as mock_gemini_cls, \
         patch("pm_workflow.api.v1.summaries.PromptManager") as mock_prompt_mgr_cls, \
         patch("pm_workflow.api.v1.summaries.SummaryService") as mock_service_cls, \
         patch("pm_workflow.api.v1.summaries.meeting_repo.list_by_date_range", return_value=[mock_meeting]), \
         patch("pm_workflow.api.v1.summaries.DailySummaryResponse.model_validate", return_value=MagicMock()):

        mock_llm = MagicMock()
        mock_prompt_manager = MagicMock()
        mock_gemini_cls.return_value = mock_llm
        mock_prompt_mgr_cls.return_value = mock_prompt_manager

        mock_summary = MagicMock()
        mock_service_instance = MagicMock()
        mock_service_instance.generate_daily_summary = AsyncMock(return_value=mock_summary)
        mock_service_cls.return_value = mock_service_instance

        await generate_daily_summary(target_date=date(2026, 8, 18), db=mock_db)

        mock_gemini_cls.assert_called_once()
        mock_prompt_mgr_cls.assert_called_once()
        mock_service_cls.assert_called_once_with(llm=mock_llm, prompt_manager=mock_prompt_manager)
