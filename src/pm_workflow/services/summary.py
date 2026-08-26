from uuid import UUID

from sqlalchemy.orm import Session

from pm_workflow.integrations.llm.base import BaseLLMProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.models.meeting import Meeting
from pm_workflow.models.summary import MeetingSummary
from pm_workflow.repositories import summary_repo


class SummaryService:
    def __init__(self, llm: BaseLLMProvider, prompt_manager: PromptManager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    async def generate_meeting_summary(self, db: Session, meeting_id: UUID) -> MeetingSummary:
        meeting = db.get(Meeting, meeting_id)
        if not meeting:
            raise ValueError(f"Meeting not found: {meeting_id}")

        analysis = meeting.analysis
        context_parts = []
        if meeting.transcript:
            context_parts.append(f"Transcript:\n{meeting.transcript}")
        if analysis:
            analysis_parts = []
            if analysis.decisions:
                analysis_parts.append(f"Decisions:\n{chr(10).join(str(d) for d in analysis.decisions)}")
            if analysis.action_items:
                analysis_parts.append(f"Action Items:\n{chr(10).join(str(a) for a in analysis.action_items)}")
            if analysis.risks:
                analysis_parts.append(f"Risks:\n{chr(10).join(str(r) for r in analysis.risks)}")
            if analysis.dependencies:
                analysis_parts.append(f"Dependencies:\n{chr(10).join(str(d) for d in analysis.dependencies)}")
            if analysis.missing_information:
                analysis_parts.append(f"Missing Information:\n{chr(10).join(str(m) for m in analysis.missing_information)}")
            if analysis.client_requests:
                analysis_parts.append(f"Client Requests:\n{chr(10).join(str(c) for c in analysis.client_requests)}")
            if analysis.requirements:
                analysis_parts.append(f"Requirements:\n{chr(10).join(str(r) for r in analysis.requirements)}")
            if analysis.open_questions:
                analysis_parts.append(f"Open Questions:\n{chr(10).join(str(q) for q in analysis.open_questions)}")
            if analysis.project_status:
                analysis_parts.append(f"Project Status:\n{analysis.project_status}")
            if analysis.suggested_next_actions:
                analysis_parts.append(f"Suggested Next Actions:\n{chr(10).join(str(s) for s in analysis.suggested_next_actions)}")
            if analysis_parts:
                context_parts.append("\n\nAnalysis:\n" + "\n\n".join(analysis_parts))

        if not context_parts:
            raise ValueError("Cannot generate summary: meeting has no transcript and no analysis")

        context = "\n\n".join(context_parts)

        prompt = self.prompt_manager.load("summary").format(
            meeting_title=meeting.title,
            meeting_date=meeting.date.isoformat(),
            context=context,
        )
        raw = await self.llm.generate(prompt)
        summary_text = raw.get("text", "")

        try:
            summary_json = raw if isinstance(raw, dict) else {"text": summary_text}
        except (TypeError, ValueError):
            summary_json = {"text": summary_text}

        existing = summary_repo.get_by_meeting_id(db, meeting_id)
        if existing:
            existing.summary_text = summary_text
            existing.summary_json = summary_json
            return summary_repo.update(db, existing)

        return summary_repo.create(
            db,
            MeetingSummary(
                meeting_id=meeting_id,
                summary_text=summary_text,
                summary_json=summary_json,
            ),
        )
