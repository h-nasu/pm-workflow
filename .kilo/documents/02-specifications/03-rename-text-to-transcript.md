# Refactor Specification: Rename `text` → `transcript`

## Expected behavior (must be preserved)
- `POST /api/v1/meetings/manual` creates a `Meeting` from the submitted notes.
- The submitted notes are stored verbatim in `Meeting.transcript`.
- If `title` is omitted, it is derived from the first non-empty line of the notes (≤200 chars) or `"Untitled Meeting"`.
- If `date` is omitted, current UTC time is used. `participants` defaults to `{}`.
- Missing/empty notes → `422`.

## Change
- Request field `text` is renamed to `transcript`. It remains required (non-empty string).
- All other request/response fields unchanged.

## Request before
```json
{ "text": "Kickoff with Alice and Bob", "title": "Project Kickoff" }
```
## Request after
```json
{ "transcript": "Kickoff with Alice and Bob", "title": "Project Kickoff" }
```

## Verification
- Existing tests for the endpoint are updated to the new field name and must pass.
- No other endpoint or behavior is affected.
