# Architecture Source of Truth Operating Model

BUBAT stages `01` through `04` are the architecture source of truth for the application being built.

## Truth Hierarchy

| Layer | Artifact | Role |
|-------|----------|------|
| Architecture truth | `stages/01-discovery` through `stages/04-component` outputs | Business intent, domain boundaries, data model, containers, components |
| Implementation plan | `stages/06-spec/output/SPEC.md` + interface specs | Cavekit-ready build contract |
| Runtime implementation | Project codebase | Actual executable system |
| Trace index | `stages/04-component/output/{{SYSTEM_SLUG}}-component-code-map.md` | Component → file path / symbol / line span mapping |
| Change intent | `triage/{{DATE}}-{{FEATURE_SLUG}}-impact.md` | Feature request impact analysis and update plan |

## Feature Change Workflow

1. User submits feature/change request:
   ```text
   triage <feature request>
   ```
2. Triage reads architecture outputs and code map, then writes change impact artifact.
3. Triage identifies:
   - change class
   - entry stage(s)
   - affected flows, scenarios, bounded contexts, entities, containers, components, contracts
   - affected code map rows / files
   - minimum `update <stages>` command
   - whether `bridge` must run
4. User confirms plan.
5. Update affected stages in order.
6. Run Stage 06 bridge so cavekit receives updated spec and implementation pointers.
7. Cavekit updates/adds code.
8. Run `update 04` after code changes to refresh component code map.
9. Optionally run `bridge` again so SPEC.md task pointers match final code map.

## Change Classes

| Change Class | Typical Entry Stage | Required Follow-up |
|--------------|---------------------|--------------------|
| `business-feature` | `01b-flow` | update downstream through `04`, then `bridge` |
| `domain-change` | `01c-bounded-context` | update data/container/component impact, then `bridge` |
| `data-change` | `01d-data-model` | update containers/components/contracts, then `bridge` |
| `contract-change` | `03-container` | update component internals + interfaces, then `bridge` |
| `component-change` | `04-component` | update code map + `bridge` |
| `infra-change` | `03-container` | update deployment/container model + `bridge` if implementation tasks change |
| `bugfix-local` | `04-component` or none | update code map only if files/symbols changed |
| `refactor-local` | `04-component` | refresh code map; no domain/flow changes unless responsibility changes |

## Governance Rules

1. Architecture-significant changes must start with `triage`.
2. Code changes that alter business flow, domain meaning, data model, contract, container boundary, or component responsibility must update corresponding BUBAT stages before implementation.
3. `06-spec` is regenerated before cavekit implementation for architecture-significant changes.
4. After implementation, `update 04` refreshes component code map.
5. Code map stale rows are drift indicators, not design authority.
6. If code conflicts with architecture artifacts, resolve by either:
   - updating code to match architecture, or
   - rerunning affected BUBAT stages to accept new design.

## Drift Signals

| Signal | Meaning | Action |
|--------|---------|--------|
| Component has no code map row | planned/unimplemented or stale Stage 04 | add missing marker or map implementation |
| Code map file path missing from repo | moved/deleted code | refresh `update 04` |
| Symbol not found in mapped file | stale mapping | refresh row |
| New file implements architecture component but unmapped | hidden implementation drift | add code map row |
| Contract changed in code but not Stage 03 | architecture drift | update `03-container` and bridge |
| Domain entity changed in code but not Stage 01d | data model drift | update `01d-data-model` and downstream |
