# AGENTS.md

This file defines the **binding agent contract** for this repository.
It takes precedence over all other guidance files.

---

## 1. Hierarchy of Authority

| Priority | Source | Role |
|----------|--------|------|
| 1 | `AGENTS.md` | Binding agent rules |
| 2 | `.kilo/instructions/*.md` | Project workflows and guidance |
| 3 | `.kilo/rules/*.md` | Standards and policies |
| 4 | User messages | Immediate task requests |

When sources conflict, the higher-priority source wins.

---

## 2. Core Principles

- **Read and apply** all instruction and rule files before acting.
- **Quote the specific rule** being followed when executing a task.
- **Do not skip** instructions because they seem advisory; treat them as requirements unless the user explicitly overrides them.
- **Verify** work with tests, linting, and type checks before marking tasks complete.
- **Document** all changes in the appropriate client-facing or internal documentation.

---

## 3. Mandatory Workflow

For every user request, follow this sequence:

1. **LOAD** — Read `AGENTS.md`, `.kilo/instructions/`, and `.kilo/rules/`.
2. **APPLY** — Execute the task while explicitly referencing applicable rules.
3. **VERIFY** — Run tests, lint, and type checks.
4. **DOCUMENT** — Update documentation to reflect changes made.

If verification fails, **do not mark the task complete**. Stop, report the failure, and request user direction.

---

## 4. Conflict Resolution

- If `AGENTS.md` conflicts with `.kilo/rules/`, follow `AGENTS.md`.
- If `.kilo/instructions/` conflicts with `.kilo/rules/`, follow `.kilo/instructions/`.
- If the user explicitly overrides a rule, the user’s instruction takes precedence, but the agent must **state the override** before proceeding.
