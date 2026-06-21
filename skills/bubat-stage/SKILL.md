---
name: bubat-stage
description: Run a BUBAT stage by id using the shared stage index and runbook. Use when user types "stage <stage-id>" or asks to run a stage.
---

# BUBAT Stage Runner

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Given a stage id or shortcut (`04`, `component`, `04-component`, etc.):

1. Normalize requested stage using Shortcut + Alias tables below.
2. Read `${WORKSPACE_ROOT}/shared/stage-runbook.md`.
3. Read `${WORKSPACE_ROOT}/shared/stage-index.md` for current stage inputs, references, load boundaries, and outputs.
4. Read `${WORKSPACE_ROOT}/shared/output-catalog.md` for artifact names and consumers.
5. Read `${WORKSPACE_ROOT}/shared/stage-gates.md` and apply relevant gates.
6. Check `${WORKSPACE_ROOT}/raw/MANIFEST.md`; load raw rows matching exact stage id.
7. Read current stage `${WORKSPACE_ROOT}/stages/<stage-id>/CONTEXT.md` for stage-specific rules only.
8. Load required upstream inputs and references from stage index.
9. If workspace targets existing project codebase (`project_path` set or code exists nearby), invoke `@commands/cl/research_codebase.md` with stage-focused query before synthesis to improve precision.
10. Execute stage-specific process.
11. Present checkpoint before saving.
12. Run audit, placeholder, traceability, and diagram gates as applicable.
13. Write outputs listed in output catalog.
14. After confirmed writes, invoke `skills/bubat-sync-index` for changed output paths.
15. Report output files and downstream stages likely affected.

## Shortcuts

- `stage discovery` → `01-discovery`
- `stage flow` → `01b-flow`
- `stage bounded-context` → `01c-bounded-context`
- `stage data-model` → `01d-data-model`
- `stage context` → `02-context`
- `stage container` → `03-container`
- `stage component` → `04-component`
- `stage document` → `05-document`
- `stage spec` → `06-spec`
- `stage validation` → `07-spec-validation`
- `stage test-scaffold` → `08-test-scaffold`
- `stage 01` → `01-discovery`
- `stage 01b` → `01b-flow`
- `stage 01c` → `01c-bounded-context`
- `stage 01d` → `01d-data-model`
- `stage 02` → `02-context`
- `stage 03` → `03-container`
- `stage 04` → `04-component`
- `stage 05` → `05-document`
- `stage 06` → `06-spec`
- `stage 07` → `07-spec-validation`
- `stage 08` → `08-test-scaffold`

## Alias Rules

Accept:
- numeric ids: `01`, `01b`, `01c`, `01d`, `02` ... `08`
- full ids: `04-component`
- names: `component`, `container`, `spec`, `validation`

If alias is ambiguous, ask user to choose. If unknown, list valid stage ids from `${WORKSPACE_ROOT}/shared/stage-index.md`.

## Rule

Do not use `CLAUDE.md` load matrix. `${WORKSPACE_ROOT}/shared/stage-index.md` is authoritative.
