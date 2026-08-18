import pytest
from fastapi.testclient import TestClient

from pm_workflow.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.skip(reason="Requires PostgreSQL running via docker-compose")
def test_list_meetings_empty():
    response = client.get("/api/v1/meetings/")
    assert response.status_code == 200
    assert response.json() == []
