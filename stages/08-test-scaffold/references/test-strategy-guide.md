# Test Strategy Guide

Rules for mapping §V invariants to test types. Apply during Stage 08 Part A.

## Primary Mapping — §V Source → Test Type

| §V Source Artifact | Primary Test Type | Secondary |
|-------------------|-------------------|-----------|
| Discovery NFR (performance threshold) | Integration | E2E |
| Discovery NFR (availability %, uptime) | E2E | — |
| Discovery compliance mandate | Integration | Unit |
| Business flow precondition | BDD | E2E |
| Business flow postcondition | BDD | E2E |
| Business flow failure path | BDD | Integration |
| Key scenario trigger | BDD | E2E |
| Bounded context aggregate rule | Unit | Integration |
| Bounded context BC boundary rule | Integration | — |
| Bounded context ubiquitous language | Unit | — |
| Data model NOT NULL / unique | Unit | Integration |
| Data model FK integrity | Integration | — |
| Data model enum values | Unit | — |
| Data model field length | Unit | — |
| Interface contract SLA | Integration | E2E |
| Interface contract auth requirement | Integration | — |
| Interface contract error code guarantee | Integration | — |
| Interface contract retry limit | Integration | — |
| Sequence ordering invariant | Integration | E2E |
| Sequence idempotency requirement | Integration | — |
| Sequence rollback guarantee | Integration | E2E |
| Tech decision pattern invariant | Unit | Integration |

## Test Type Decision Rules

### Unit test when:
- Invariant is about a single component's internal behavior
- Invariant is falsifiable without a running network or database
- Invariant is a data validation rule (format, length, enum, null check)
- Invariant is a state transition within one bounded context aggregate

### Integration test when:
- Invariant involves two or more containers communicating
- Invariant is about an HTTP/gRPC contract (status codes, schema, auth, SLA)
- Invariant is about FK integrity or cross-BC data consistency
- Invariant is about retry/idempotency behavior across a network call
- Invariant is about event ordering or at-least-once delivery

### E2E test when:
- Invariant spans the full user journey (entry point through final observable outcome)
- Invariant is about system availability or uptime from user's perspective
- Invariant requires multiple containers to be running simultaneously
- Invariant describes a business postcondition observable at the UI/API boundary

### BDD (Gherkin) when:
- Invariant is expressible as: "given [actor state], when [actor action], then [observable outcome]"
- Invariant originates from a business flow or key scenario
- Invariant describes user-visible behavior, not internal mechanics
- Product/non-technical stakeholders need to read and verify the test

## Multiple Type Assignment

When an invariant maps to multiple types, generate scenarios for all assigned types.
Priority order (highest coverage value first): BDD > Integration > E2E > Unit

Exception: If generating the higher-priority test type already fully verifies the invariant, skip lower-priority types and note in matrix: "covered by [type]".

## Invariants to Exclude from Scaffolding

| Pattern | Reason | Matrix entry |
|---------|--------|--------------|
| External system SLA (third-party) | Out of our control | "No scaffold — assumption (external)" |
| Process/team compliance invariant | Not automatable | "No scaffold — process check" |
| Duplicate of another §V | Already covered | "Covered by §V.N" |
