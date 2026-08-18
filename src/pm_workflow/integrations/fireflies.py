from datetime import datetime
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from pm_workflow.config import get_settings
from pm_workflow.core.exceptions import ExternalAPIError


class FirefliesClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.fireflies.ai/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.settings.FIREFLIES_API_KEY}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def fetch_transcripts(self, start_date: datetime, end_date: datetime) -> list[dict[str, Any]]:
        query = """
        query ($fromDate: DateTime, $toDate: DateTime) {
            transcripts(fromDate: $fromDate, toDate: $toDate) {
                id
                title
                date
                duration
                participants
                transcript_url
                sentences {
                    text
                }
            }
        }
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {
                        "fromDate": start_date.isoformat(),
                        "toDate": end_date.isoformat(),
                    },
                },
                headers=self.headers,
                timeout=30.0,
            )
            if response.status_code != 200:
                raise ExternalAPIError(
                    f"Fireflies API HTTP {response.status_code}: {response.text}"
                )
            data = response.json()
            if "errors" in data:
                raise ExternalAPIError(f"Fireflies API error: {data['errors']}")
            transcripts = data.get("data", {}).get("transcripts", [])
            normalized = []
            for t in transcripts:
                normalized.append({
                    "id": t["id"],
                    "title": t["title"],
                    "date": t["date"],
                    "duration": t.get("duration"),
                    "participants": t.get("participants", []),
                    "transcript_url": t.get("transcript_url"),
                    "sentences": t.get("sentences", []),
                })
            return normalized
