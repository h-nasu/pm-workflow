import json
from typing import Any

from google import genai
from google.genai import types

from pm_workflow.config import get_settings
from pm_workflow.integrations.llm.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.settings = get_settings()
        self.client = genai.Client(
            api_key=self.settings.GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=60000),
        )
        self.model = "gemini-3.6-flash"

    async def generate(self, prompt: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
        config = types.GenerateContentConfig(
            response_mime_type="application/json" if schema else "text/plain",
            response_json_schema=schema,
        )
        response = self.client.models.generate_content(model=self.model, contents=prompt, config=config)
        text = response.text or "{}"
        if schema:
            return json.loads(text)
        return {"text": text}
