---
description: Implement new features from planning through deployment
agent: code
---
This workflow guides the implementation of new features from planning through deployment.

## Steps

1. **Before-Task Hook**: Follow all before-task hook steps (analyze request, define requirements, create documents)
2. **Plan**: Create a plan in `01-plans/`
3. **Specify**: Define requirements in `02-specifications/`
4. **Design**: Create design in `03-designs/`
5. **Break Down Tasks**: Create tasks in `04-tasks/`
6. **Implement**: Implement changes incrementally following `rules/coding.md` and `rules/architecture.md`
7. **Test**: Write and run tests; ensure all pass
8. **Review**: Conduct code review using the `review-code.md` skill
9. **Document**: Update client-facing documentation under `docs/`
10. **After-Task Hook**: Follow all after-task hook steps (verify tests, update documents, evaluate confidence)

## Exit Criteria

- All tasks are complete
- All tests pass
- Code review is approved
- Documentation is updated
- Confidence level is above 0.8
