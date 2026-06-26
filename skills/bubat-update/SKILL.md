---
name: bubat-update
description: Re-run one or more BUBAT stages after system changes. Use when user types "update <stage(s)>" in a BUBAT workspace, e.g. "update 03" or "update 03 04 05".
---

# BUBAT Update

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Given the stage numbers specified:

1. Parse which stage numbers were specified (e.g. `update 03 04 05`).
2. Detect update mode:
   - default = `patch`
   - explicit `--rewrite` = full artifact regeneration
   - explicit `--patch` = section-level update even if user omitted mode previously
3. Warn: downstream stages will be re-run — confirm before proceeding.
4. Re-run each specified stage in order, starting from the lowest number.
5. Each re-run stage reads its inputs fresh (including any upstream outputs that were re-run in the same pass).
6. If workspace targets existing project codebase (`${WORKSPACE_ROOT}/shared/system-meta.md` has `project_path` or code exists nearby), for each re-run stage before synthesis:
   - read `${WORKSPACE_ROOT}/shared/research-index.json` if present to find reusable prior research matching current stage/topic/code refs
   - load only compact relevant sections from `${WORKSPACE_ROOT}/shared/research/*.md` (summary, code references, open questions) as a map
   - invoke `@commands/cl/research_codebase.md` with stage-focused query to fresh-validate live code
   - require saved research output under `${WORKSPACE_ROOT}/shared/research/`; keep the saved path for index sync and reporting
7. For markdown stage artifacts in `patch` mode:
   - read existing artifact first
   - generate candidate updated artifact from current inputs
   - compute changed sections by stable heading/block (`#`, `##`, `###`, tables directly under heading, diagram fences directly under heading)
   - preserve untouched sections byte-for-byte
   - replace only sections proven affected by current change or upstream evidence
   - if section boundaries are ambiguous, heading structure changed, or >40% of sections change, stop patch mode and ask to switch to `--rewrite`
   - present `changed sections` summary plus unified diff before write confirmation
8. For non-markdown structured artifacts (`openapi.yaml`, `.proto`, generated interface specs, machine-readable tables where row order may rebalance), prefer `--rewrite` unless stage rule defines safe block-level patching.
9. Special rule for `update 04`:
   - Refresh component diagrams, component sequences, component scope, and `output/{slug}-component-code-map.md`.
   - If `project_path` contains existing code, rebuild code map in `discovery` mode from actual files.
   - If code was newly generated after prior design, rebuild same map in `generated` mode from generated files.
   - Keep rows for planned components whose implementation still does not exist: mark `[MISSING — implementation not yet generated]` rather than dropping them.
   - In `patch` mode, preserve unchanged narrative sections and replace only changed component rows/sections when mapping remains structurally stable.
10. Use git as review guardrail, not source-of-truth engine:
   - inspect candidate changes with `git diff -- <artifact>` when repo exists
   - use git history for rollback/audit if needed
   - do not infer semantic section impact from git alone
11. After each confirmed artifact write/patch, invoke `skills/bubat-sync-index` for touched paths and any saved `${WORKSPACE_ROOT}/shared/research/*.md` paths from step 6.
12. Append a note to `{slug}-tech-decisions.md` marking which stages were updated, why, whether mode was `patch` or `rewrite`, and which research docs were used/saved (ask user for reason).
13. Sync tech-decisions artifact too if it was updated.
14. After all stages complete, invoke skill `bubat-status` to confirm.

Rule:
- same existing-project precision rule as `stage <id>` applies during `update <stage(s)>`
- codebase research sharpens rerun accuracy; confirmed BUBAT artifacts remain source of truth
- patch mode allowed only when artifact headings/blocks are stable enough for safe targeted replacement
