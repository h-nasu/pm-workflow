# Issue: `/meetings/extract` docs operation hangs / "loading forever"

## Symptom
Opening the Swagger UI operation `POST /api/v1/meetings/extract` (or clicking "Try it out" → "Execute") appears to load forever with no response.

## Reproduction
1. Run the API (`uvicorn pm_workflow.main:app`).
2. Open `http://localhost:8000/docs` and navigate to the `extract` operation.
3. With "Try it out", send `{"text":"..."}`.
4. In environments without a reachable Gemini endpoint or without `GEMINI_API_KEY`, the request never returns (or takes many seconds) → UI shows a perpetual loading state.

Verified locally: with a valid key the call returns in ~0.5–4s; with a missing key / blocked network the call previously retried via `tenacity` and/or blocked on the socket until TCP timeout (effectively "forever" from the UI's perspective).

## Root Cause
`POST /api/v1/meetings/extract` (and `sync`, `analyze`) performs a synchronous external LLM call, but:
1. `GeminiProvider` constructed the `genai.Client` **without any request timeout** → a blocked/unreachable network hangs indefinitely (no upper bound).
2. There was **no guard for a missing `GEMINI_API_KEY`** → without a key the provider still attempts the network call, which (via `tenacity` retries) delays failure and can appear to hang.

The hang is at request-execution time, which is exactly what Swagger UI's "Try it out" triggers — hence the docs operation "loads forever."

## Resolution
- `src/pm_workflow/integrations/llm/gemini.py`: `genai.Client(..., http_options=types.HttpOptions(timeout=60000))` so external calls fail fast instead of hanging forever.
- `src/pm_workflow/api/v1/meetings.py`: added `_require_llm_configured()`, called at the start of `extract_meeting`, `sync_meetings`, and `analyze_meeting`. Returns `503` immediately when `GEMINI_API_KEY` is not configured, so no network call is attempted.
- `analyze_meeting` now checks the key before the DB lookup (consistent ordering).

## Correction (unit bug)
The first fix used `types.HttpOptions(timeout=30)`. `HttpOptions.timeout` is documented in **milliseconds**, so `30` meant 30 ms — the LLM call aborted almost instantly with "The read operation timed out" (the symptom reported right after the fix). Corrected to `timeout=60000` (60 seconds), which accommodates normal LLM latency (calls return in ~5–7s) while still bounding a blocked network. This is covered by `test_gemini_provider_configures_request_timeout_in_ms` (asserts timeout >= 30000 ms).

## Preventive Measures
- Regression tests added in `tests/integration/test_api.py`:
  - `test_extract_meeting_without_api_key_returns_503`
  - `test_sync_without_api_key_returns_503`
  - `test_analyze_without_api_key_returns_503`
- These assert that the endpoints fail fast (503) when the LLM provider is unconfigured, preventing the silent hang regression.
- External integrations must always set an explicit timeout (done in `GeminiProvider`) and validate required configuration up front.
