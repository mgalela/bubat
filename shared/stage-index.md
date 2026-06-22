# BUBAT Stage Index

Registry for stage routing, inputs, references, outputs, and downstream dependencies. Use with `shared/stage-runbook.md`.

## Pipeline

`01-discovery → 01b-flow → 01c-bounded-context → 01d-data-model → 02-context → 03-container → 04-component → 05-document → 06-spec → 07-spec-validation → 08-test-scaffold`

## Stages

| Stage | Purpose | Required Inputs | References | Outputs |
|-------|---------|-----------------|------------|---------|
| `01-discovery` | Gather system info, users, dependencies, NFRs, tech decisions | `shared/system-meta.md`, `raw/MANIFEST.md`; optional `<project_path>/graphify-out/` | `stages/01-discovery/references/` | `{slug}-discovery.md`, `{slug}-tech-decisions.md` |
| `01b-flow` | Capture business flows and key scenarios | `01-discovery/output/`, `shared/system-meta.md` | `stages/01b-flow/references/` | `{slug}-flows.md`, `{slug}-scenarios.md` |
| `01c-bounded-context` | Identify bounded contexts and context relationships | `01b-flow/output/`, `01-discovery/output/`, `shared/system-meta.md` | `stages/01c-bounded-context/references/` | `{slug}-bounded-contexts.md`, `{slug}-context-map.md` |
| `01d-data-model` | Convert BC aggregates to entity model and storage hints | `01c-bounded-context/output/`, `01b-flow/output/`, `shared/system-meta.md` | `stages/01d-data-model/references/` | `{slug}-domain-entities.md`, `{slug}-er-model.md`, `{slug}-data-dependencies.md`, `{slug}-storage-hints.md` |
| `02-context` | Build C4 Level 1 system context | `01c-bounded-context/output/`, `01-discovery/output/`, `shared/c4-notation.md` | `stages/02-context/references/` | `{slug}-context.md` |
| `03-container` | Build C4 Level 2 containers, contracts, sequences | `02-context/output/`, `01d-data-model/output/`, `01c-bounded-context/output/`, `01b-flow/output/`, `shared/c4-notation.md` | `stages/03-container/references/` | `{slug}-containers.md`, `{slug}-contracts.md`, `{slug}-sequences-l2.md` |
| `04-component` | Build C4 Level 3 components, component sequences, scope, code map | `03-container/output/`, `01-discovery/output/`, `shared/system-meta.md`, `shared/c4-notation.md` | `stages/04-component/references/` | `{slug}-components.md`, `{slug}-component-scope.md`, `{slug}-sequences-l3.md`, `{slug}-component-code-map.md` |
| `05-document` | Assemble final architecture document and optional FSD markdown | `01-discovery/output/`, `01b-flow/output/`, `01c-bounded-context/output/`, `01d-data-model/output/`, `02-context/output/`, `03-container/output/`, `04-component/output/` | `stages/05-document/references/`, `tools/docx-generator/templates/` | `{slug}-architecture.md`, optional `{slug}-fsd.md` |
| `06-spec` | Bridge architecture outputs to cavekit `SPEC.md` and interface specs | all available `01–04` outputs, `shared/system-meta.md`, optional `triage/*-impact.md` | `stages/06-spec/references/` | `SPEC.md`, `openapi.yaml`, `{slug}.proto`, `{slug}-interfaces.*`, `{slug}-extraction-map.md` |
| `07-spec-validation` | Validate Stage 06 outputs | `06-spec/output/`, `shared/system-meta.md` | `stages/07-spec-validation/references/` | `{slug}-spec-validation.md` |
| `08-test-scaffold` | Derive BDD/unit/integration/e2e scenarios | `07-spec-validation/output/`, `06-spec/output/`, `01b-flow/output/`, `04-component/output/` | `stages/08-test-scaffold/references/` | `{slug}-bdd-features.md`, `{slug}-unit-tests.md`, `{slug}-integration-tests.md`, `{slug}-e2e-tests.md`, `{slug}-coverage-matrix.md` |

## Load Boundaries

| Stage | Do Not Load |
|-------|-------------|
| `01-discovery` | `01b-flow` through `05-document` |
| `01b-flow` | `01c-bounded-context` through `05-document` |
| `01c-bounded-context` | `01d-data-model` through `05-document` |
| `01d-data-model` | `02-context` through `05-document` |
| `02-context` | `03-container` through `05-document` |
| `03-container` | `04-component`, `05-document` |
| `04-component` | `05-document` |
| `05-document` | `06-spec` |
| `06-spec` | `05-document` (use source stages directly) |
| `07-spec-validation` | all except `06-spec/output`, `shared/system-meta.md`, `07` references |
| `08-test-scaffold` | discovery through `05-document`, except explicitly listed inputs |

## Triggers

| Trigger | Skill / Stage |
|---------|---------------|
| `stage <id>` | `skills/bubat-stage/SKILL.md` |
| `setup` | setup questionnaire |
| `raw route` | `skills/bubat-raw-route/SKILL.md` |
| `status` | `skills/bubat-status/SKILL.md` |
| `where <term>` / `trace <term>` / `find artifact <term>` | `skills/bubat-trace/SKILL.md` |
| `refresh index` | `skills/bubat-refresh-index/SKILL.md` |
| `sync index <path(s)>` | `skills/bubat-sync-index/SKILL.md` |
| `diagram <stage>` | `skills/bubat-diagram/SKILL.md` |
| `update <stages>` | `skills/bubat-update/SKILL.md` |
| `triage <idea>` | `skills/bubat-triage/SKILL.md` |
| `bridge` | `skills/bubat-bridge/SKILL.md` or `stages/06-spec/CONTEXT.md` |
| `sync graphify` | `skills/bubat-graphify-sync/SKILL.md` |
