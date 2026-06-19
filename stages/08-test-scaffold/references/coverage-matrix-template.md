# Coverage Matrix Template

Template for `{{SYSTEM_SLUG}}-test-coverage-matrix.md`. Fill during Stage 08 Part F.

## Matrix Structure

```markdown
# Test Coverage Matrix — {{SYSTEM_NAME}}
> Generated: {{DATE}} · Source: BUBAT/stages/08-test-scaffold/output/{{SYSTEM_SLUG}}-test-coverage-matrix.md

## Summary

| Test Type | Scenario Count | §V Invariants Covered |
|-----------|---------------|----------------------|
| BDD | {{N}} | {{N}} |
| Integration | {{N}} | {{N}} |
| Unit | {{N}} | {{N}} |
| E2E | {{N}} | {{N}} |
| **Total covered** | {{N}} | {{N}} / {{total §V}} |
| No scaffold | — | {{N}} |

## Coverage Detail

| §V # | Invariant (abbreviated) | Unit | Integration | E2E | BDD | Notes |
|------|------------------------|------|-------------|-----|-----|-------|
| §V.1 | {{invariant text, truncated}} | — | INT-3, INT-7 | — | Checkout feature | |
| §V.2 | {{invariant text}} | UNIT-OrderSvc-2 | — | — | — | |
| §V.3 | {{invariant text}} | — | — | E2E-5 | Order flow feature | |
| §V.4 | {{invariant text}} | — | — | — | — | No scaffold — manual test required |
| §V.5 | {{invariant text}} | — | — | — | — | No scaffold — assumption (external) |
| §V.6 | {{invariant text}} | — | INT-2 | — | — | Covered by §V.2 (duplicate) |
```

## Column Definitions

| Column | Content |
|--------|---------|
| §V # | Exact §V.N identifier from SPEC.md |
| Invariant (abbreviated) | First 60 chars of invariant text |
| Unit | Comma-separated UNIT-[Component]-N IDs, or "—" |
| Integration | Comma-separated INT-N IDs, or "—" |
| E2E | Comma-separated E2E-N IDs, or "—" |
| BDD | Feature name (abbreviated), or "—" |
| Notes | One of: blank / "No scaffold — manual test required" / "No scaffold — assumption (external)" / "No scaffold — process check" / "Covered by §V.N (duplicate)" |

## Uncovered Invariants Section

Append after matrix if any §V invariants have zero scaffold coverage:

```markdown
## Uncovered Invariants

The following §V invariants have no automated test scaffold. Each requires manual verification or a decision to add a scenario.

| §V # | Invariant | Reason | Owner |
|------|-----------|--------|-------|
| §V.4 | {{text}} | {{reason from test-strategy-guide.md}} | {{team/role}} |
```

Leave Owner column blank at generation time — for the team to fill.
