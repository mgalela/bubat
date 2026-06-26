# BUBAT Output Catalog

Authoritative list of generated artifacts.

## Completion Criteria

| Stage | Minimum Complete When |
|-------|------------------------|
| `01-discovery` | `{slug}-discovery.md` and `{slug}-tech-decisions.md` exist |
| `01b-flow` | `{slug}-flows.md` and `{slug}-scenarios.md` exist |
| `01c-bounded-context` | `{slug}-bounded-contexts.md` and `{slug}-context-map.md` exist |
| `01d-data-model` | `{slug}-domain-entities.md`, `{slug}-er-model.md`, `{slug}-data-dependencies.md`, `{slug}-storage-hints.md` exist |
| `02-context` | `{slug}-context.md` exists |
| `03-container` | `{slug}-containers.md`, `{slug}-contracts.md`, `{slug}-sequences-l2.md` exist |
| `04-component` | `{slug}-components.md`, `{slug}-component-scope.md`, `{slug}-sequences-l3.md`, `{slug}-component-code-map.md` exist |
| `05-document` | `{slug}-architecture.md` exists; `{slug}-fsd.md` optional when FSD mode requested |
| `06-spec` | `SPEC.md` and `{slug}-extraction-map.md` exist; `openapi.yaml`, `{slug}.proto`, and `{slug}-interfaces.*` are conditional |
| `07-spec-validation` | `{slug}-spec-validation.md` exists |
| `08-test-scaffold` | BDD, unit, integration, E2E, and coverage matrix outputs exist |

## Artifact Catalog

| Artifact | Owner Stage | Consumed By | Purpose |
|----------|-------------|-------------|---------|
| `{slug}-discovery.md` | `01-discovery` | `01b`, `01c`, `02`, `05`, `06` | system boundary, users, dependencies, NFRs |
| `{slug}-tech-decisions.md` | `01-discovery` + append by later stages | `03`, `04`, `05`, `06` | ADR/decision log |
| `{slug}-flows.md` | `01b-flow` | `01c`, `01d`, `03`, `05`, `06`, `08` | business process flowcharts |
| `{slug}-scenarios.md` | `01b-flow` | `03`, `05`, `06`, `08` | key scenario definitions |
| `{slug}-bounded-contexts.md` | `01c-bounded-context` | `01d`, `02`, `03`, `06` | BC inventory, terms, domain rules |
| `{slug}-context-map.md` | `01c-bounded-context` | `02`, `03`, `06` | BC relationships |
| `{slug}-domain-entities.md` | `01d-data-model` | `03`, `06` | entity/aggregate inventory |
| `{slug}-er-model.md` | `01d-data-model` | `03`, `05` | ER diagram/model |
| `{slug}-data-dependencies.md` | `01d-data-model` | `03`, `06` | cross-BC data dependencies |
| `{slug}-storage-hints.md` | `01d-data-model` | `03`, `06` | storage recommendations |
| `{slug}-context.md` | `02-context` | `03`, `05` | C4 Level 1 diagram + narrative |
| `{slug}-containers.md` | `03-container` | `04`, `05`, `06` | C4 Level 2 diagram + inventory |
| `{slug}-contracts.md` | `03-container` | `04`, `05`, `06` | inter-container contracts |
| `{slug}-sequences-l2.md` | `03-container` | `04`, `05`, `06` | container-level sequences |
| `{slug}-components.md` | `04-component` | `05`, `06` | C4 Level 3 diagrams + narratives |
| `{slug}-component-scope.md` | `04-component` | `05`, `06`, `08` | selected containers, patterns, rationale |
| `{slug}-sequences-l3.md` | `04-component` | `05`, `06` | component-level sequences |
| `{slug}-component-code-map.md` | `04-component` | `05`, `06`, `08`, triage | component → file path/symbol/line span trace |
| `{slug}-architecture.md` | `05-document` | stakeholders, optional graphify | final architecture document |
| `{slug}-fsd.md` | `05-document` | DOCX generator, stakeholders | functional specification document markdown for DOCX/export |
| `SPEC.md` | `06-spec` | cavekit, `07`, `08` | implementation spec |
| `openapi.yaml` | `06-spec` | cavekit, `07`, `08` | HTTP API spec |
| `{slug}.proto` | `06-spec` | cavekit, `07`, `08` | gRPC API spec |
| `{slug}-interfaces.*` | `06-spec` | cavekit, `07` | language interface stubs |
| `{slug}-extraction-map.md` | `06-spec` | `07`, `08` | traceability map |
| `{slug}-spec-validation.md` | `07-spec-validation` | `08` | validation findings |
| `{slug}-bdd-features.md` | `08-test-scaffold` | test implementation | BDD feature scenarios |
| `{slug}-unit-tests.md` | `08-test-scaffold` | test implementation | unit scenario list |
| `{slug}-integration-tests.md` | `08-test-scaffold` | test implementation | integration scenario list |
| `{slug}-e2e-tests.md` | `08-test-scaffold` | test implementation | E2E scenario list |
| `{slug}-coverage-matrix.md` | `08-test-scaffold` | QA/review | invariant-to-test coverage |
| `triage/*-impact.md` | `bubat-triage` | `06-spec`, cavekit handoff | change impact and implementation targeting |
