# Refactor Design: Rename `text` → `transcript`

## Target Structure
- `ManualMeetingCreate` becomes:
  ```python
  class ManualMeetingCreate(BaseModel):
      transcript: str = Field(..., min_length=1, description="Meeting transcript / notes stored directly")
      title: str | None = Field(None, description="Meeting title; derived from transcript when omitted")
      date: datetime | None = Field(None, description="Meeting date (ISO 8601); defaults to now when omitted")
      duration_minutes: int | None = None
      participants: dict[str, Any] = Field(default_factory=dict)
  ```
- `ManualMeetingService`:
  - `_derive_title(transcript: str) -> str` (param renamed from `text`).
  - `create_from_payload` uses `payload.transcript` for both title derivation and `Meeting.transcript`.
- Endpoint summary updated to "Create a meeting from provided transcript" (cosmetic).

## Mapping
`payload.transcript` → `Meeting.transcript` (direct 1:1). Title derivation source changes only in name.

## No structural/architectural changes; single field rename plus call-site updates.
