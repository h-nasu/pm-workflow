from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from pm_workflow.api.deps import get_db
from pm_workflow.core.entity import Base
from pm_workflow.main import app
from pm_workflow.models import *

_sqlite_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_sqlite_engine)
Base.metadata.create_all(bind=_sqlite_engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_meetings():
    response = client.get("/api/v1/meetings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_analyses():
    response = client.get("/api/v1/analysis/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_analysis_not_found():
    response = client.get(f"/api/v1/analysis/{UUID('00000000-0000-0000-0000-000000000000')}")
    assert response.status_code == 404


def test_get_meeting_summary_not_found():
    response = client.get(f"/api/v1/summaries/meeting/{UUID('00000000-0000-0000-0000-000000000000')}")
    assert response.status_code == 404


def test_generate_meeting_summary_requires_existing_meeting():
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    response = client.post(f"/api/v1/summaries/meeting/{fake_id}/generate")
    assert response.status_code == 500


def test_create_manual_meeting():
    response = client.post(
        "/api/v1/meetings/manual",
        json={
            "transcript": "Kickoff with Alice and Bob",
            "title": "Project Kickoff",
            "duration_minutes": 45,
            "participants": {"Alice": True, "Bob": True},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Project Kickoff"
    assert data["fireflies_id"].startswith("manual-")
    assert data["participants"] == {"Alice": True, "Bob": True}
    assert data["transcript"] == "Kickoff with Alice and Bob"


def test_create_manual_meeting_derives_title_from_transcript():
    response = client.post("/api/v1/meetings/manual", json={"transcript": "Daily standup notes"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Daily standup notes"
    assert data["transcript"] == "Daily standup notes"


def test_create_manual_meeting_requires_transcript():
    response = client.post("/api/v1/meetings/manual", json={"transcript": ""})
    assert response.status_code == 422
