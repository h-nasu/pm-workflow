from datetime import datetime

from sqlalchemy.orm import Session

from pm_workflow.integrations.fireflies import FirefliesClient
from pm_workflow.models.meeting import Meeting
from pm_workflow.repositories import analysis_repo, meeting_repo
from pm_workflow.services.analysis import AnalysisService


class SyncService:
    def __init__(self, analysis_service: AnalysisService):
        self.fireflies = FirefliesClient()
        self.analysis_service = analysis_service

    async def sync_range(self, db: Session, start_date: datetime, end_date: datetime) -> list[Meeting]:
        transcripts = await self.fireflies.fetch_transcripts(start_date, end_date)
        synced = []
        for t in transcripts:
            existing = meeting_repo.get_by_fireflies_id(db, t["id"])
            if existing:
                continue
            participants = {p: True for p in t.get("participants", [])}
            sentences = t.get("sentences", [])
            transcript = " ".join(s["text"] for s in sentences) if sentences else None
            raw_date = t.get("date")
            if isinstance(raw_date, str):
                meeting_date = datetime.fromisoformat(raw_date)
            elif isinstance(raw_date, (int, float)):
                # Fireflies may return millisecond timestamps
                ts = raw_date if raw_date < 1e12 else raw_date / 1000.0
                meeting_date = datetime.fromtimestamp(ts)
            else:
                meeting_date = start_date
            meeting = Meeting(
                fireflies_id=t["id"],
                title=t["title"],
                date=meeting_date,
                duration_minutes=t.get("duration"),
                participants=participants,
                transcript=transcript,
                transcript_url=t.get("transcript_url"),
            )
            meeting = meeting_repo.create(db, meeting)
            analysis = await self.analysis_service.analyze_meeting(meeting)
            analysis_repo.create(db, analysis)
            synced.append(meeting)
        return synced
