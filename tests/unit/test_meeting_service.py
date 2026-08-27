from datetime import UTC, datetime

from pm_workflow.api.schemas.meeting import ManualMeetingCreate
from pm_workflow.repositories.meeting import MeetingRepository
from pm_workflow.services.meeting import ManualMeetingService, _derive_title


def test_create_from_payload_uses_provided_fields(db):
    payload = ManualMeetingCreate(
        transcript="Some raw notes",
        title="Sprint Planning",
        date=datetime(2024, 3, 10, 14, 30, tzinfo=UTC),
        duration_minutes=60,
        participants={"Alice": True, "Bob": True},
    )
    service = ManualMeetingService()
    meeting = service.create_from_payload(db, payload)

    assert meeting.title == "Sprint Planning"
    expected_date = datetime(2024, 3, 10, 14, 30, tzinfo=UTC).replace(tzinfo=None)
    assert meeting.date == expected_date
    assert meeting.duration_minutes == 60
    assert meeting.participants == {"Alice": True, "Bob": True}
    assert meeting.transcript == "Some raw notes"
    assert meeting.fireflies_id.startswith("manual-")

    repo = MeetingRepository()
    fetched = repo.get_by_fireflies_id(db, meeting.fireflies_id)
    assert fetched is not None
    assert fetched.id == meeting.id


def test_create_from_payload_defaults_when_optional_fields_omitted(db):
    payload = ManualMeetingCreate(transcript="Kickoff with Alice and Bob")
    service = ManualMeetingService()
    meeting = service.create_from_payload(db, payload)

    assert meeting.title == "Kickoff with Alice and Bob"
    assert meeting.participants == {}
    assert meeting.transcript == "Kickoff with Alice and Bob"
    assert isinstance(meeting.date, datetime)
    assert meeting.fireflies_id.startswith("manual-")


def test_derive_title_uses_first_non_empty_line():
    assert _derive_title("  \nLine one\nLine two") == "Line one"


def test_derive_title_truncates_long_lines():
    long_line = "x" * 500
    assert len(_derive_title(long_line)) == 200


def test_derive_title_falls_back_to_untitled():
    assert _derive_title("   \n   \n") == "Untitled Meeting"
