# Task Breakdown: Improve Swagger `participants` Example

| # | Task | Files | Verification |
|---|------|-------|--------------|
| 1 | Add `example={"personA": True}` to `MeetingBase.participants` | `api/schemas/meeting.py` | openapi schema |
| 2 | Add `example={"personA": True}` to `ManualMeetingCreate.participants` | `api/schemas/meeting.py` | openapi schema |
| 3 | Verify OpenAPI example via `app.openapi()` | n/a (script) | schema shows example |
| 4 | Run full test suite + lint + typecheck | repo root | `pytest`, `ruff`, `mypy` |
