# Refactor Plan: Rename `text` → `transcript` in Manual Meeting Creation

## Scope
Rename the request body field of `POST /api/v1/meetings/manual` from `text` to `transcript` across the schema, service, endpoint, tests, and docs.

## Goal
Make the API contract self-describing: the caller submits a `transcript` (meeting notes), which is stored directly in the `Meeting.transcript` column. This removes the former implicit mapping where `text` was "stored as the transcript".

## Out of Scope
- No change to the endpoint path, HTTP method, response shape, or storage behavior.
- No change to the optional fields (`title`, `date`, `duration_minutes`, `participants`).
- No change to the `sync`/`analyze` endpoints.

## Behavior Before / After
- **Before:** client sends `{"text": "...", ...}`; service stores `text` as `Meeting.transcript`; title derived from `text` when omitted.
- **After:** client sends `{"transcript": "...", ...}`; service stores `transcript` as `Meeting.transcript`; title derived from `transcript` when omitted.
- Functional outcome (a `Meeting` is created from the provided notes) is unchanged.

## Targets
| File | Change |
|------|--------|
| `src/pm_workflow/api/schemas/meeting.py` | `ManualMeetingCreate.text` → `transcript` |
| `src/pm_workflow/services/meeting.py` | read `payload.transcript`; `_derive_title` param rename |
| `src/pm_workflow/api/v1/meetings.py` | endpoint summary wording (optional) |
| `tests/unit/test_meeting_service.py` | use `transcript=` |
| `tests/integration/test_api.py` | send `"transcript":` |
| `docs/api-endpoints.md` | examples/notes use `transcript` |

## Risks
- External API contract change (field rename) — intentional per request. Any existing caller using `text` must switch to `transcript`.
