
from pm_workflow.core.exceptions import LLMError, ValidationError
from pm_workflow.integrations.llm.base import BaseLLMProvider
from pm_workflow.integrations.llm.prompt_manager import PromptManager
from pm_workflow.models.analysis import MeetingAnalysis
from pm_workflow.models.meeting import Meeting
from pm_workflow.api.schemas.analysis import AnalysisOutput


class AnalysisService:
    def __init__(self, llm: BaseLLMProvider, prompt_manager: PromptManager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    async def analyze_meeting(self, meeting: Meeting) -> MeetingAnalysis:
        prompt = self.prompt_manager.load("analysis").format(
            title=meeting.title,
            date=meeting.date.isoformat(),
            participants=", ".join(meeting.participants.keys()) if meeting.participants else "Unknown",
            transcript=meeting.transcript or "",
        )
        try:
            raw = await self.llm.generate(prompt, schema=AnalysisOutput.model_json_schema())
        except Exception as e:
            raise LLMError(f"LLM generation failed: {e}") from e

        try:
            parsed = AnalysisOutput.model_validate(raw)
        except Exception as e:
            raise ValidationError(f"Invalid LLM response: {e}") from e

        return MeetingAnalysis(
            meeting_id=meeting.id,
            decisions=parsed.decisions,
            action_items=parsed.action_items,
            risks=parsed.risks,
            dependencies=parsed.dependencies,
            missing_information=parsed.missing_information,
            client_requests=parsed.client_requests,
            requirements=parsed.requirements,
            open_questions=parsed.open_questions,
            project_status=parsed.project_status,
            suggested_next_actions=parsed.suggested_next_actions,
            raw_response=raw,
            model_used=self.llm.__class__.__name__,
        )
