# Refactor Design: Improve Swagger `participants` Example

## Target Structure
In `api/schemas/meeting.py`:
```python
class MeetingBase(BaseModel):
    ...
    participants: dict[str, Any] = Field(default_factory=dict, example={"personA": True})
    ...

class ManualMeetingCreate(BaseModel):
    ...
    participants: dict[str, Any] = Field(default_factory=dict, example={"personA": True})
```

## Why `example` on the Field
FastAPI renders the field-level `example` into the OpenAPI schema, overriding the generic `additionalProp1` placeholder that Pydantic generates for `dict[str, Any]`. This is metadata-only: serialization/validation behavior is unaffected.

## No structural/architectural changes.
