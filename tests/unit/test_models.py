from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pm_workflow.core.entity import Base
from pm_workflow.models.meeting import Meeting


def test_meeting_model_columns():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    meeting = Meeting(
        fireflies_id="test-1",
        title="Test",
        date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        participants={"user": "test"},
        transcript="hello world",
    )
    db.add(meeting)
    db.commit()

    loaded = db.get(Meeting, meeting.id)
    assert loaded.fireflies_id == "test-1"
    assert loaded.title == "Test"
    assert loaded.participants == {"user": "test"}
    assert loaded.transcript == "hello world"
