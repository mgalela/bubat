# Stage 08: Test Scaffold

Derive test scenario scaffolds from validated Stage 06 spec outputs.
Produces BDD feature files, unit test scenario lists (TDD), integration test scenarios (per contract), E2E test scenarios (per business flow), and a coverage matrix mapping §V invariants to test scenarios.

Output is framework-agnostic and language-agnostic — scenario text only, not runnable code.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Validation report | `../07-spec-validation/output/{{SYSTEM_SLUG}}-spec-validation.md` | Blocking findings | Gate: no Blocking findings allowed |
| Cavekit spec | `../06-spec/output/SPEC.md` | §V, §C, §I, §T | Primary scenario source |
| Extraction map | `../06-spec/output/{{SYSTEM_SLUG}}-extraction-map.md` | Full file | Traceability labels for matrix |
| OpenAPI spec | `../06-spec/output/openapi.yaml` | Full file | Integration test endpoint source (if exists) |
| proto3 definition | `../06-spec/output/{{SYSTEM_SLUG}}.proto` | Full file | Integration test RPC source (if exists) |
| Business flows | `../01b-flow/output/{{SYSTEM_SLUG}}-flows.md` | Full file | E2E and BDD scenario source |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | E2E and BDD scenario source |
| Component scope | `../04-component/output/{{SYSTEM_SLUG}}-component-scope.md` | Full file | Unit test target identification |
| Test strategy guide | `references/test-strategy-guide.md` | Full file | §V → test type mapping rules |
| BDD template | `references/bdd-template.md` | Full file | Gherkin feature structure |
| Coverage matrix template | `references/coverage-matrix-template.md` | Full file | Matrix structure |

If validation report has Blocking findings, stop: "Resolve Blocking findings in Stage 07 report before generating test scaffolds."
If SPEC.md is missing, stop: "Run stage 06 first."

## Stage Gate

Apply `../../shared/stage-gates.md`: G1 Input gate (Stage 07 report required, zero Blocking findings); G8 Test Scaffold gate before saving outputs.

## Process

1. Read validation report — confirm zero Blocking findings. Stop if any exist.
2. Read SPEC.md — index all §V invariants with Source column.
3. Read test-strategy-guide.md — load §V source type → test type mapping rules.

### Part A — §V → Test Type Mapping

4. For each §V invariant: assign primary test type(s) using `references/test-strategy-guide.md`.
   - **Unit**: invariant about single component's internal logic, state transitions, or data rules
   - **Integration**: invariant about contract between containers (protocol, format, auth, error codes, SLA)
   - **E2E**: invariant spanning multiple actors or container boundaries in a business flow
   - **BDD**: invariant expressible as observable user-facing behavior (when X, user sees Y)
   - One invariant may map to multiple types
5. Build initial §V coverage matrix rows (§V.N → test types assigned).

### Part B — BDD Feature Files

6. Read business flows and key scenarios.
7. For each key scenario from `scenarios.md`: derive one BDD Feature with:
   - Feature name: scenario name
   - Background: shared preconditions across scenarios in same flow
   - Scenario (happy path): trigger → steps → postcondition as Then assertion
   - Scenario (failure path): at least one failure case per documented failure path in flows
   - Given/When/Then steps: derived from scenario trigger, ordered steps, and postconditions
   - Steps use domain language only — no container, component, or tech names
8. For each §V invariant mapped to BDD not already covered above: generate one additional Scenario within the most relevant Feature.
9. Use structure from `references/bdd-template.md`.
10. Pause at checkpoint 1 — confirm BDD feature list before proceeding to integration + unit scaffolds.

### Part C — Integration Test Scenarios

11. Source: openapi.yaml paths + proto rpc methods + §V invariants mapped to Integration.
12. For each HTTP endpoint in openapi.yaml:
    - Happy path: valid request body → expected status code + response shape
    - Auth failure: missing/invalid credential → 401 or 403
    - Validation failure: malformed or missing required field → 400 + error body shape
    - SLA assertion: response time ≤ x-sla value (if present)
    - Idempotency: duplicate request with same idempotency key → same response, no side effect (if applicable)
13. For each gRPC RPC in proto:
    - Happy path, error status code, timeout/deadline scenario.
14. For each §V invariant mapped to Integration not covered by steps 12-13: add targeted named scenario.
15. Number scenarios sequentially: INT-1, INT-2, ...
16. Output as table: scenario ID, name, precondition, action, expected outcome, §V reference.

### Part D — Unit Test Scenarios

17. Source: component scope (`04-component`) + §V invariants mapped to Unit.
18. For each component in component scope: list testable behaviors from scope description.
    - Identify: inputs, outputs, state transitions, error cases documented.
19. For each §V invariant mapped to Unit: generate test case with precondition + action + assertion.
20. Group by component. Number sequentially within component: UNIT-[Component]-1, UNIT-[Component]-2, ...
21. Output as grouped list — component name as header, scenario rows below.

### Part E — E2E Test Scenarios

22. Source: business flows (all happy + failure paths) + §V invariants mapped to E2E.
23. For each distinct path in each flow (happy + each failure):
    - Entry point: actor, initial state
    - Steps: ordered actions at system boundary only (UI click, API call, file upload — no internals)
    - Exit assertion: observable outcome (page shown, email received, data persisted per §V)
24. Number: E2E-1, E2E-2, ...
25. No internal component references in steps.

### Part F — Coverage Matrix

26. For each §V.N invariant: mark which scaffold IDs cover it.
27. §V invariants with zero coverage: status = "No scaffold — manual test required".
28. Use template from `references/coverage-matrix-template.md`.

### Part G — Finalize

29. Pause at checkpoint 2 — present coverage summary before save.
30. Save all artifacts to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 10 | BDD feature list: feature names, scenario count per feature, §V invariants mapped to BDD | Add, remove, or rename features before integration + unit scaffolds are derived |
| Step 29 | Coverage summary: scenario count per type, list of §V invariants with "manual test" status | Accept gaps or request additional scenarios before save |

## Audit

| Check | Pass Condition |
|-------|---------------|
| All §V in matrix | Every §V.N has a row in coverage matrix |
| BDD steps domain-language | No container, component, or tech name in Given/When/Then steps |
| Integration scenarios trace to §I | Every INT-N cites an endpoint or RPC from §I |
| Unit scenarios trace to components | Every UNIT-X-N names a specific component from component-scope |
| E2E steps at system boundary | No E2E step references internal components |
| Uncovered invariants flagged | "No scaffold" rows include "manual test required" note |
| Scenario IDs unique | No duplicate INT-N, UNIT-X-N, E2E-N, or BDD scenario name |

## Outputs

| Artifact | Location | Condition |
|----------|----------|-----------|
| BDD feature files | `output/{{SYSTEM_SLUG}}-bdd-features.md` | Always |
| Integration test scenarios | `output/{{SYSTEM_SLUG}}-integration-tests.md` | HTTP or gRPC contracts exist in §I |
| Unit test scenarios | `output/{{SYSTEM_SLUG}}-unit-tests.md` | Component scope available |
| E2E test scenarios | `output/{{SYSTEM_SLUG}}-e2e-tests.md` | Business flows available |
| Test coverage matrix | `output/{{SYSTEM_SLUG}}-test-coverage-matrix.md` | Always |
