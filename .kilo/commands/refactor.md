---
description: Restructure code without changing behavior
agent: planner
---
This workflow guides the process of restructuring existing code without changing its external behavior.

## Steps

1. **Before-Task Hook**: Follow all before-task hook steps (define scope, identify refactoring targets)
2. **Plan**: Create a plan in `01-plans/` with the refactoring goals and scope
3. **Specify**: Document the expected behavior before and after refactoring in `02-specifications/`
4. **Design**: Define the target structure in `03-designs/`
5. **Task Breakdown**: Create small, verifiable tasks in `04-tasks/`
6. **Implement**: Execute refactoring incrementally, task by task, following `rules/coding.md` and `rules/architecture.md`
7. **Test**: Run all existing tests after each task to verify no behavior changes
8. **Review**: Conduct code review using the `review-code.md` skill
9. **Document**: Update any affected documentation under `docs/`
10. **After-Task Hook**: Follow all after-task hook steps (verify tests, update documents, evaluate confidence)

## Exit Criteria

- All existing tests pass without modification
- External behavior is unchanged
- Code quality metrics improved
- Code review is approved
