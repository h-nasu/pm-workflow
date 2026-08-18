from unittest.mock import MagicMock, patch

import pytest

from pm_workflow.integrations.llm.gemini import GeminiProvider


@pytest.fixture
def mock_genai_client():
    with patch("pm_workflow.integrations.llm.gemini.genai.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"decisions": []}'
        mock_client.models.generate_content.return_value = mock_response
        yield mock_client


@pytest.mark.asyncio
async def test_gemini_provider_generate_with_schema(mock_genai_client):
    with patch("pm_workflow.integrations.llm.gemini.get_settings") as mock_settings:
        mock_settings.return_value.GEMINI_API_KEY = "test-key"
        provider = GeminiProvider()
        schema = {"type": "object", "properties": {"decisions": {"type": "array"}}}
        result = await provider.generate("test prompt", schema=schema)
        assert result == {"decisions": []}
        call_kwargs = mock_genai_client.models.generate_content.call_args.kwargs
        assert call_kwargs["config"].response_json_schema == schema
        assert call_kwargs["config"].response_mime_type == "application/json"


@pytest.mark.asyncio
async def test_gemini_provider_generate_without_schema(mock_genai_client):
    with patch("pm_workflow.integrations.llm.gemini.get_settings") as mock_settings:
        mock_settings.return_value.GEMINI_API_KEY = "test-key"
        provider = GeminiProvider()
        result = await provider.generate("test prompt")
        assert result == {"text": '{"decisions": []}'}
        call_kwargs = mock_genai_client.models.generate_content.call_args.kwargs
        assert call_kwargs["config"].response_json_schema is None
        assert call_kwargs["config"].response_mime_type == "text/plain"
