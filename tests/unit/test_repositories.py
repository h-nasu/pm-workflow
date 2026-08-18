from datetime import datetime, timezone


from pm_workflow.models.analysis import MeetingAnalysis
from pm_workflow.models.meeting import Meeting
from pm_workflow.models.summary import DailySummary
from pm_workflow.repositories.analysis import AnalysisRepository
from pm_workflow.repositories.meeting import MeetingRepository
from pm_workflow.repositories.summary import SummaryRepository


def test_meeting_repository_create(db):
    repo = MeetingRepository()
    meeting = Meeting(
        fireflies_id="ff-123",
        title="Test Meeting",
        date=datetime.now(timezone.utc),
        participants={"alice": True},
    )
    created = repo.create(db, meeting)
    assert created.id is not None
    assert created.fireflies_id == "ff-123"


def test_meeting_repository_get_by_fireflies_id(db):
    repo = MeetingRepository()
    meeting = Meeting(fireflies_id="ff-456", title="Another", date=datetime.now(timezone.utc))
    repo.create(db, meeting)
    found = repo.get_by_fireflies_id(db, "ff-456")
    assert found is not None
    assert found.title == "Another"


def test_meeting_repository_list_by_date_range(db):
    repo = MeetingRepository()
    for i in range(5):
        m = Meeting(fireflies_id=f"ff-{i}", title=f"M{i}", date=datetime(2024, 1, i + 1, tzinfo=timezone.utc))
        repo.create(db, m)
    results = repo.list_by_date_range(db, datetime(2024, 1, 2, tzinfo=timezone.utc), datetime(2024, 1, 3, tzinfo=timezone.utc))
    assert len(results) == 2


def test_analysis_repository(db):
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(
        db, Meeting(fireflies_id="ff-1", title="M1", date=datetime.now(timezone.utc))
    )
    repo = AnalysisRepository()
    analysis = MeetingAnalysis(
        meeting_id=meeting.id,
        decisions=[],
        action_items=[],
        risks=[],
        dependencies=[],
        missing_information=[],
        client_requests=[],
        requirements=[],
        open_questions=[],
        project_status={},
        suggested_next_actions=[],
        raw_response={},
        model_used="gemini",
    )
    created = repo.create(db, analysis)
    assert created.id is not None
    found = repo.get_by_meeting_id(db, meeting.id)
    assert found is not None
    assert found.model_used == "gemini"


def test_summary_repository(db):
    repo = SummaryRepository()
    summary = DailySummary(date=datetime(2024, 1, 15).date(), summary_text="Test", summary_json={}, meeting_count=1)
    created = repo.create(db, summary)
    assert created.id is not None
    found = repo.get_by_date(db, datetime(2024, 1, 15).date())
    assert found is not None
    assert found.summary_text == "Test"
