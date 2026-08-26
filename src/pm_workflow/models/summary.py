from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pm_workflow.core.entity import TimestampedModel

if TYPE_CHECKING:
    from pm_workflow.models.meeting import Meeting


class MeetingSummary(TimestampedModel):
    __tablename__ = "meeting_summaries"

    meeting_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("meetings.id"), unique=True, nullable=False, index=True)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="summary")
