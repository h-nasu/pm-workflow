from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from pm_workflow.main import app

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
