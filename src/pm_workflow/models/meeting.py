from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pm_workflow.core.entity import TimestampedModel


class Meeting(TimestampedModel):
    __tablename__ = "meetings"

    fireflies_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(nullable=True)
    participants: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    transcript: Mapped[str] = mapped_column(Text, nullable=True)
    transcript_url: Mapped[str] = mapped_column(String(1000), nullable=True)

    analysis: Mapped["MeetingAnalysis"] = relationship("MeetingAnalysis", back_populates="meeting", uselist=False)  # noqa: F821
    summary: Mapped["MeetingSummary"] = relationship("MeetingSummary", back_populates="meeting", uselist=False)  # noqa: F821
