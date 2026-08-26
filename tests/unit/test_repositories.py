from datetime import UTC, datetime

from pm_workflow.models.analysis import MeetingAnalysis
from pm_workflow.models.meeting import Meeting
from pm_workflow.models.summary import MeetingSummary
from pm_workflow.repositories.analysis import AnalysisRepository
from pm_workflow.repositories.meeting import MeetingRepository
from pm_workflow.repositories.summary import SummaryRepository


def test_meeting_repository_create(db):
    repo = MeetingRepository()
    meeting = Meeting(
        fireflies_id="ff-123",
        title="Test Meeting",
        date=datetime.now(UTC),
        participants={"alice": True},
    )
    created = repo.create(db, meeting)
    assert created.id is not None
    assert created.fireflies_id == "ff-123"


def test_meeting_repository_get_by_fireflies_id(db):
    repo = MeetingRepository()
    meeting = Meeting(fireflies_id="ff-456", title="Another", date=datetime.now(UTC))
    repo.create(db, meeting)
    found = repo.get_by_fireflies_id(db, "ff-456")
    assert found is not None
    assert found.title == "Another"


def test_meeting_repository_list_by_date_range(db):
    repo = MeetingRepository()
    for i in range(5):
        m = Meeting(fireflies_id=f"ff-{i}", title=f"M{i}", date=datetime(2024, 1, i + 1, tzinfo=UTC))
        repo.create(db, m)
    results = repo.list_by_date_range(db, datetime(2024, 1, 2, tzinfo=UTC), datetime(2024, 1, 3, tzinfo=UTC))
    assert len(results) == 2


def test_analysis_repository(db):
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(
        db, Meeting(fireflies_id="ff-1", title="M1", date=datetime.now(UTC))
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


def test_analysis_repository_list_by_date_range(db):
    meeting_repo = MeetingRepository()
    for i in range(5):
        m = meeting_repo.create(
            db,
            Meeting(
                fireflies_id=f"ff-{i}",
                title=f"M{i}",
                date=datetime(2024, 1, i + 1, tzinfo=UTC),
            ),
        )
        analysis_repo = AnalysisRepository()
        analysis_repo.create(
            db,
            MeetingAnalysis(
                meeting_id=m.id,
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
            ),
        )
    repo = AnalysisRepository()
    results = repo.list_by_date_range(
        db, datetime(2024, 1, 2, tzinfo=UTC), datetime(2024, 1, 3, tzinfo=UTC)
    )
    assert len(results) == 2


def test_summary_repository(db):
    meeting_repo = MeetingRepository()
    meeting = meeting_repo.create(
        db,
        Meeting(
            fireflies_id="ff-summary",
            title="Summary Meeting",
            date=datetime.now(UTC),
            participants={},
        ),
    )
    repo = SummaryRepository()
    summary = MeetingSummary(meeting_id=meeting.id, summary_text="Test", summary_json={})
    created = repo.create(db, summary)
    assert created.id is not None
    found = repo.get_by_meeting_id(db, meeting.id)
    assert found is not None
    assert found.summary_text == "Test"


from uuid import UUID


def test_summary_repository_get_by_meeting_id_missing(db):
    repo = SummaryRepository()
    found = repo.get_by_meeting_id(db, UUID("00000000-0000-0000-0000-000000000000"))
    assert found is None
