---
description: Prepare and execute a release
agent: architect
---
This workflow guides the process of preparing and executing a release.

## Steps

1. **Before-Task Hook**: Follow all before-task hook steps (define release scope and version)
2. **Plan**: Create a release plan in `01-plans/` with version number, changes, and timeline
3. **Specify**: Define acceptance criteria and release notes in `02-specifications/`
4. **Task Breakdown**: Create tasks for release preparation in `04-tasks/`
5. **Finalize**: Merge all completed feature branches, resolve conflicts
6. **Test**: Run full test suite including integration and e2e tests
7. **Review**: Conduct a release review using the `review-code.md` skill
8. **Tag**: Create a git tag for the release version
9. **Document**: Update `docs/` with release notes and any migration guides
10. **Deploy**: Execute the deployment procedure defined in project documentation
11. **After-Task Hook**: Follow all after-task hook steps (verify deployment, update documents, evaluate confidence)

## Standards

- Follow the git guidelines in `rules/git.md`
- Follow the coding standards in `rules/coding.md`

## Exit Criteria

- All tests pass
- Release notes are published
- Git tag is created
- Deployment is verified
- Confidence level is above 0.9
