# Stage 07: Spec Validation

Stage id: `07-spec-validation`

Purpose: validate Stage 06 outputs for completeness, consistency, testability, and cavekit readiness.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#07-spec-validation`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to verify Stage 06 claims against existing contracts, modules, and test anchors before drafting outputs

## Stage-Specific Rules

1. Load all files in `stages/06-spec/output/` plus `shared/system-meta.md`.
2. Read `stages/07-spec-validation/references/`.
3. Validate `SPEC.md` sections §G/§C/§I/§R/§V/§T/§B.
4. Validate extraction map coverage for every §C and §V entry.
5. Validate generated OpenAPI/proto/interface specs where present.
6. Classify findings: Blocking / Major / Minor / Advisory.
7. Produce remediation guidance with source pointers.
8. Stage 08 may run only if report has zero Blocking findings.

## Audit Focus

- every required SPEC section exists
- every invariant is testable
- constraints are concrete or explicitly missing
- interfaces are syntactically plausible and traceable
- extraction map covers required entries
- no Blocking findings hidden as lower severity

## Outputs

See `shared/output-catalog.md`:
- `{slug}-spec-validation.md`
