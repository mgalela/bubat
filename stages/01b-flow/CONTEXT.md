# Stage 01b: Business Flows

Stage id: `01b-flow`

Purpose: capture business flows, user journeys, and key scenarios for downstream sequence diagrams and tests.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#01b-flow`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

## Stage-Specific Rules

1. Load discovery outputs and system metadata.
2. Read all `stages/01b-flow/references/` guides.
3. Identify user roles, business flows, happy paths, failure paths, triggers, preconditions, and postconditions.
4. Keep flows business-level: no container/component/technology names.
5. Select key scenarios that must receive downstream sequence diagrams.
6. Confirm flow list and scenario list before saving.
7. Cite discovery/raw sources for extracted facts.

## Audit Focus

- each user role has at least one flow or explicit `[N/A]`
- flows have start, end, happy path, failure path
- key scenarios have trigger, actors, preconditions, postconditions
- no tech leakage in business flow diagrams

## Outputs

See `shared/output-catalog.md`:
- `{slug}-flows.md`
- `{slug}-scenarios.md`
