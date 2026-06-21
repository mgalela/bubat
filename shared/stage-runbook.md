# BUBAT Stage Runbook

Common protocol for running any BUBAT stage.

## Standard Stage Protocol

1. Read `shared/stage-gates.md` and apply relevant gates.
2. Read `shared/stage-index.md` for current stage inputs, references, outputs, and downstream consumers.
3. Check `raw/MANIFEST.md`; load only rows whose `Stages` contains current exact stage id.
4. Load required upstream artifacts and stage references.
5. If `project_path` points to existing codebase:
   - read `shared/research-index.json` if present to find reusable prior codebase research for current stage/topic/code refs
   - load only compact relevant prior research from `shared/research/*.md` (summary, code references, open questions) as a map
   - use `@commands/cl/research_codebase.md` before stage synthesis to perform focused fresh validation for current stage
   - require saved research output under `shared/research/`; use findings as evidence source, not replacement for upstream artifacts or raw materials
6. If required inputs are missing, stop unless stage explicitly allows missing markers.
7. Execute stage-specific rules from `stages/<stage>/CONTEXT.md`.
8. Present checkpoint(s) before writing outputs.
9. Run stage audit plus placeholder and traceability gates.
10. Save outputs to `stages/<stage>/output/`.
11. After successful confirmed save, incrementally sync changed output paths into lookup indexes via `skills/bubat-sync-index`. If codebase research was saved under `shared/research/`, sync that path too.
12. Append ADR/tech decision entries only when rules require; never overwrite tech decisions log.

## Source-of-Truth Protocol

For architecture-significant changes:

1. Run `triage <request>` first.
2. Update affected stages in dependency order.
3. Run `bridge` before cavekit/code implementation.
4. After code changes, run `update 04` to refresh component code map.
5. Run `bridge` again if SPEC task pointers changed.

See `shared/architecture-source-of-truth.md`.

## Checkpoint Rule

Do not overwrite or patch stage outputs until user confirms checkpoint result.

For `update` runs in patch mode:
- show changed sections first
- show diff summary before write
- preserve untouched sections exactly
- switch to full rewrite if patch safety rule fails

Index sync rule:
- sync indexes only after confirmed final write
- sync saved `shared/research/*.md` so reuse lookup stays current
- do not sync preview/dry-run output
- if incremental sync fails, keep artifact write and recommend `refresh index`

## Missing Input Rule

Use explicit marker only when allowed:

```text
[MISSING — reason]
```

Stage 06 may emit `[MISSING — run stage XX first]` by design. Other stages should stop on missing required upstream artifacts.
