from typing import Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AnalysisOutput(BaseModel):
    decisions: list[dict[str, Any]] = []
    action_items: list[dict[str, Any]] = []
    risks: list[dict[str, Any]] = []
    dependencies: list[dict[str, Any]] = []
    missing_information: list[dict[str, Any]] = []
    client_requests: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    open_questions: list[dict[str, Any]] = []
    project_status: dict[str, Any] = {}
    suggested_next_actions: list[dict[str, Any]] = []


class AnalysisResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    decisions: list[dict[str, Any]]
    action_items: list[dict[str, Any]]
    risks: list[dict[str, Any]]
    dependencies: list[dict[str, Any]]
    missing_information: list[dict[str, Any]]
    client_requests: list[dict[str, Any]]
    requirements: list[dict[str, Any]]
    open_questions: list[dict[str, Any]]
    project_status: dict[str, Any]
    suggested_next_actions: list[dict[str, Any]]
    model_used: str
    created_at: datetime

    model_config = {"from_attributes": True, "protected_namespaces": ()}
