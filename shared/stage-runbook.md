# BUBAT Stage Runbook

Common protocol for running any BUBAT stage.

## Standard Stage Protocol

1. Read `shared/stage-gates.md` and apply relevant gates.
2. Read `shared/stage-index.md` for current stage inputs, references, outputs, and downstream consumers.
3. Check `raw/MANIFEST.md`; load only rows whose `Stages` contains current exact stage id.
4. Load required upstream artifacts and stage references.
5. If required inputs are missing, stop unless stage explicitly allows missing markers.
6. Execute stage-specific rules from `stages/<stage>/CONTEXT.md`.
7. Present checkpoint(s) before writing outputs.
8. Run stage audit plus placeholder and traceability gates.
9. Save outputs to `stages/<stage>/output/`.
10. Append ADR/tech decision entries only when rules require; never overwrite tech decisions log.

## Source-of-Truth Protocol

For architecture-significant changes:

1. Run `triage <request>` first.
2. Update affected stages in dependency order.
3. Run `bridge` before cavekit/code implementation.
4. After code changes, run `update 04` to refresh component code map.
5. Run `bridge` again if SPEC task pointers changed.

See `shared/architecture-source-of-truth.md`.

## Checkpoint Rule

Do not overwrite stage outputs until user confirms checkpoint result.

## Missing Input Rule

Use explicit marker only when allowed:

```text
[MISSING — reason]
```

Stage 06 may emit `[MISSING — run stage XX first]` by design. Other stages should stop on missing required upstream artifacts.
