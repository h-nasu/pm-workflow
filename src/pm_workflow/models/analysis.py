from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pm_workflow.core.entity import TimestampedModel
from pm_workflow.models.meeting import Meeting


class MeetingAnalysis(TimestampedModel):
    __tablename__ = "meeting_analyses"

    meeting_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False, index=True)
    decisions: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    action_items: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    risks: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    dependencies: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    missing_information: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    client_requests: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    requirements: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    open_questions: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    project_status: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    suggested_next_actions: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    raw_response: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="analysis")
