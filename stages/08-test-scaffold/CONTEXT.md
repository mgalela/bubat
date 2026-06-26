# Stage 08: Test Scaffold

Stage id: `08-test-scaffold`

Purpose: derive framework-agnostic BDD, unit, integration, E2E scenarios and coverage matrix from validated Stage 06 spec outputs.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#08-test-scaffold`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to inspect current test suites, fixtures, seams, and coverage anchors before drafting outputs

## Stage-Specific Rules

1. Load Stage 07 validation report; stop if any Blocking findings exist.
2. Load `SPEC.md`, extraction map, OpenAPI/proto/interfaces if present, business flows/scenarios, component scope, and component code map.
3. Read `stages/08-test-scaffold/references/`.
4. Index all §V invariants and map each to test type(s): BDD, Unit, Integration, E2E.
5. Generate BDD features from business scenarios in domain language only.
6. Generate integration scenarios from HTTP paths, gRPC RPCs, and integration-class invariants.
7. Generate unit scenarios grouped by component; if code map exists, include target file path and line span.
8. Generate E2E scenarios from business flow happy/failure paths using only boundary-observable steps.
9. Generate coverage matrix mapping each §V invariant to scenario ids.
10. Confirm BDD list before integration/unit/E2E generation; confirm final matrix before saving.

## Audit Focus

- zero Blocking findings from Stage 07
- every §V has coverage row
- BDD uses domain language only
- integration scenarios trace to §I endpoint/RPC
- unit scenarios trace to component and code map where available
- E2E steps stay at system boundary
- scenario ids unique

## Outputs

See `shared/output-catalog.md`:
- `{slug}-bdd-features.md`
- `{slug}-unit-tests.md`
- `{slug}-integration-tests.md`
- `{slug}-e2e-tests.md`
- `{slug}-coverage-matrix.md`
