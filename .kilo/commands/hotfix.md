---
description: Respond to critical production issues
agent: debugger
---
This workflow guides the process of responding to critical issues in production.

## Steps

1. **Before-Task Hook**: Follow all before-task hook steps (analyze the severity and impact)
2. **Identify**: Reproduce the issue in a production-like environment
3. **Debug**: Use the `debug-error.md` skill to diagnose the root cause quickly
4. **Fix**: Implement the minimal fix that resolves the production issue, following `rules/coding.md` and `rules/architecture.md`
5. **Test**: Write a regression test following `rules/testing.md` and verify the fix
6. **Review**: Conduct an expedited code review focusing on correctness and safety
7. **Branch**: Create a hotfix branch from the production/main branch
8. **Merge**: Merge the hotfix into production/main and the current development branch
9. **Tag**: Create a version tag for the hotfix release
10. **Document**: Update `08-issues/` with root cause, resolution, and preventive measures
11. **After-Task Hook**: Follow all after-task hook steps (verify deployment, evaluate confidence)

## Exit Criteria

- Production issue is resolved
- Regression test is added
- Hotfix is merged into all relevant branches
- Git tag is created
- Post-mortem document is created if severity warrants it
