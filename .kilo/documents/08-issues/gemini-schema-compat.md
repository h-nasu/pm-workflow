# Issue: GeminiProvider LLM generation failed with `'dict' object has no attribute 'model_dump'` and related errors

## Date
2026-08-18

## Severity
High

## Symptom
`POST /api/v1/meetings/{id}/analyze` returned one of:
```json
{
  "detail": "LLM generation failed: 'dict' object has no attribute 'model_dump'"
}
```
or
```json
{
  "detail": "LLM generation failed: object GenerateContentResponse can't be used in 'await' expression"
}
```

## Root Cause
The `google-genai` SDK v2.18.1 introduced breaking changes:
1. `Schema.from_json_schema()` now expects a Pydantic `JSONSchema` model object, but the code passed a plain Python `dict`.
2. `Models.generate_content()` is a **synchronous** method, but the code incorrectly used `await` on it.
3. `gemini-2.0-flash` model was deprecated/removed; the API returned 404.

## Resolution
1. **`src/pm_workflow/integrations/llm/gemini.py`** — Replaced `response_schema=types.Schema.from_json_schema(json_schema=schema)` with `response_json_schema=schema`. The newer SDK accepts raw JSON schema dicts via `GenerateContentConfig.response_json_schema`, which is the recommended approach per the SDK's own deprecation notice.
2. **`src/pm_workflow/integrations/llm/gemini.py`** — Removed incorrect `await` from `self.client.models.generate_content(...)`. The SDK method is synchronous and returns `GenerateContentResponse` directly.
3. **`src/pm_workflow/integrations/llm/gemini.py`** — Updated model name from `gemini-2.0-flash` (deprecated/removed) to `gemini-3.6-flash`.
4. **`tests/unit/test_gemini.py`** — Added regression tests for both schema and no-schema generation paths.

## Preventive Measures
- Pin `google-genai` version in `pyproject.toml` to avoid silent breakage from SDK updates.
- Add unit tests that exercise the `GeminiProvider.generate()` path with a schema dict to catch API incompatibilities early.
- Consult SDK migration guides when upgrading major versions of AI provider libraries.
