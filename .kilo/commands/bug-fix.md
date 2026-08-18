---
description: Diagnose and fix bugs
agent: debugger
---
This workflow guides the process of diagnosing and fixing bugs.

## Steps

1. **Before-Task Hook**: Follow all before-task hook steps (analyze the bug report, define reproduction steps)
2. **Reproduce**: Identify and document the exact reproduction steps
3. **Debug**: Use the `debug-error.md` skill to diagnose the root cause
4. **Fix**: Implement the minimal fix that addresses the root cause, following `rules/coding.md` and `rules/architecture.md`
5. **Test**: Add or update tests to cover the bug scenario and verify the fix
6. **Review**: Conduct code review focusing on the fix and regression prevention
7. **Document**: Update `08-issues/` with root cause, resolution, and preventive measures
8. **After-Task Hook**: Follow all after-task hook steps (verify tests, update documents, evaluate confidence)

## Exit Criteria

- Bug is reproducible and then resolved
- Fix includes a regression test
- Code review is approved
- No regressions detected in existing tests
