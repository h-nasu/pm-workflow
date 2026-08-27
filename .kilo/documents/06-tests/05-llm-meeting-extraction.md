# Test Plan & Results: LLM-based Meeting Extraction Endpoint

## Unit Tests (`tests/unit/test_llm_meeting_service.py`)
- `test_create_from_text_creates_meeting` — LLM returns all fields; meeting persisted with `manual-` id, mapped participants (`{name: True}`), correct transcript; round-trip verified.
- `test_create_from_text_defaults_when_fields_missing` — Empty extraction → `Untitled Meeting` title, raw `text` as transcript, empty participants, `manual-` id.
- `test_create_from_text_raises_validation_error_on_bad_response` — Invalid LLM JSON → `ValidationError`.
- `test_parse_date_valid_iso` / `test_parse_date_handles_z_suffix_as_naive_utc` / `test_parse_date_falls_back_to_now` — ISO parsing, `Z` handling (naive UTC), fallback.

## Integration Tests (`tests/integration/test_api.py`)
Runs against in-memory SQLite via `get_db` override.
- `test_extract_meeting` — `POST /api/v1/meetings/extract` with mocked LLM/PromptManager returns `200` and correct shape (`title`, `manual-` id, participants mapping).
- `test_extract_meeting_requires_text` — Empty `text` returns `422`.

## Results
```
41 passed
```
Lint: new code clean (pre-existing repo-wide B008/BLE001 unaffected). Type check: new modules clean.
