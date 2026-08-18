from datetime import date

from sqlalchemy.orm import Session

from pm_workflow.integrations.llm.base import BaseLLMProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.models.meeting import Meeting
from pm_workflow.models.summary import DailySummary
from pm_workflow.repositories import summary_repo


class SummaryService:
    def __init__(self, llm: BaseLLMProvider, prompt_manager: PromptManager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    async def generate_daily_summary(self, db: Session, target_date: date, meetings: list[Meeting]) -> DailySummary:
        if not meetings:
            context = "No meetings found for this date."
        else:
            lines = []
            for m in meetings:
                lines.append(f"- {m.title} ({m.date.isoformat()})")
            context = "\n".join(lines)

        prompt = self.prompt_manager.load("summary").format(
            date=target_date.isoformat(),
            meetings_context=context,
        )
        raw = await self.llm.generate(prompt)
        summary_text = raw.get("text", "")

        try:
            summary_json = raw if isinstance(raw, dict) else {"text": summary_text}
        except Exception:
            summary_json = {"text": summary_text}

        existing = summary_repo.get_by_date(db, target_date)
        if existing:
            existing.summary_text = summary_text
            existing.summary_json = summary_json
            existing.meeting_count = len(meetings)
            return summary_repo.update(db, existing)

        return summary_repo.create(
            db,
            DailySummary(
                date=target_date,
                summary_text=summary_text,
                summary_json=summary_json,
                meeting_count=len(meetings),
            ),
        )
