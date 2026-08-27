# Change Log: Improve Swagger `participants` Example

## Change: Clearer OpenAPI example for `participants`
- **When**: After the `text` → `transcript` rename of the manual meeting endpoint.
- **Why**: The auto-generated Swagger example for the `participants` dict (`dict[str, Any]`) showed a confusing `additionalProp1: {}` placeholder. The real shape is `{ "name": true }` (matching `sync.py`'s `{p: True for p in participants}`). A clear example improves API understanding.
- **What changed**:
  - `MeetingBase.participants` and `ManualMeetingCreate.participants` in `api/schemas/meeting.py` now carry `json_schema_extra={"example": {"personA": True}}`.
  - Used `json_schema_extra` (not the deprecated `example=` Field kwarg) — this also removed `PydanticDeprecatedSince20` warnings, improving code quality.
- **Behavior preserved**: Only the OpenAPI documentation example changed. Runtime request/response types and behavior are unchanged; all 33 tests pass without modification. `mypy` and `ruff` are clean.
