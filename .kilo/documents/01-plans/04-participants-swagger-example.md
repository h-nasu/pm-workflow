# Refactor Plan: Improve Swagger `participants` Example

## Scope
Improve the OpenAPI/Swagger example for the `participants` field so it reads naturally as `{ "personA": true }` instead of the auto-generated `additionalProp1: {}`.

## Goal
Make the API contract self-explanatory in Swagger UI. The `participants` field is a `dict[str, Any]` in which each key is a participant name mapped to `true` (e.g. `{ "personA": true }`), matching how `sync.py` builds it (`{p: True for p in participants}`). The generic `additionalProp1` placeholder is confusing.

## Out of Scope
- No change to request/response runtime behavior or data types.
- No change to storage or service logic.

## Targets
| File | Change |
|------|--------|
| `src/pm_workflow/api/schemas/meeting.py` | Add a clear `example` to `MeetingBase.participants` and `ManualMeetingCreate.participants` |

## Behavior Before / After
- **Before:** Swagger example for `participants` is `{ "additionalProp1": {} }`.
- **After:** Swagger example for `participants` is `{ "personA": true }`.
- The actual accepted/returned data shape is unchanged.
