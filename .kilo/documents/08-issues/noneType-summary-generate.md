# Issue: `NoneType` error on daily summary generation endpoint

## Summary

`POST /api/v1/summaries/daily/generate` returns a 500 error with detail `'NoneType' object has no attribute 'load'` when called.

## Root Cause

In `src/pm_workflow/api/v1/summaries.py`, the `generate_daily_summary` route handler instantiated `SummaryService` with `None` for both `llm` and `prompt_manager` dependencies:

```python
summary_service = SummaryService(llm=None, prompt_manager=None)
```

When `SummaryService.generate_daily_summary()` executed, it called `self.prompt_manager.load("summary")`, which raised `AttributeError: 'NoneType' object has no attribute 'load'` because `self.prompt_manager` was `None`.

## Resolution

Updated `src/pm_workflow/api/v1/summaries.py` to properly instantiate `GeminiProvider` and `PromptManager` before passing them to `SummaryService`, matching the existing pattern used in `src/pm_workflow/api/v1/meetings.py`:

```python
llm = GeminiProvider()
prompt_manager = PromptManager()
summary_service = SummaryService(llm=llm, prompt_manager=prompt_manager)
```

## Preventive Measures

1. Added a regression test (`tests/unit/test_summaries_api.py`) that verifies `SummaryService` is instantiated with non-None `llm` and `prompt_manager` dependencies.
2. Consider adding dependency injection for `llm` and `prompt_manager` in the API layer to avoid manual instantiation in each route handler.

## Files Changed

- `src/pm_workflow/api/v1/summaries.py` — fixed dependency instantiation
- `tests/unit/test_summaries_api.py` — added regression test
