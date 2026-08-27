# Refactor Specification: Improve Swagger `participants` Example

## Expected behavior (must be preserved)
- `participants` remains `dict[str, Any]`.
- Request and response accept/return `{ name: true, ... }`.
- No runtime/logic change.

## Change
- Set an OpenAPI `example` of `{"personA": true}` on the `participants` field in `MeetingBase` (used by `MeetingResponse`) and in `ManualMeetingCreate` (request body).

## Before (Swagger example)
```json
"participants": { "additionalProp1": {} }
```
## After (Swagger example)
```json
"participants": { "personA": true }
```

## Verification
- `app.openapi()` schema for `MeetingResponse` and `ManualMeetingCreate` shows the new example.
- All existing tests pass without modification.
