from datetime import date

from sqlalchemy import Date, Integer, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from pm_workflow.core.entity import TimestampedModel


class DailySummary(TimestampedModel):
    __tablename__ = "daily_summaries"

    date: Mapped[date] = mapped_column(Date, unique=True, nullable=False, index=True)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    meeting_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
