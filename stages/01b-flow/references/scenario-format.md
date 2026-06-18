# Scenario Format

Format for the `{slug}-scenarios.md` artifact. Each scenario is used as the source for
sequence diagrams in Stages 03 and 04.

## Scenario Table (overview)

```markdown
| ID | Scenario Name | Primary Actor | Trigger | Priority |
|----|---------------|---------------|---------|----------|
| SC-01 | Customer places order | Customer | User action | High |
| SC-02 | Payment failure retry | Customer | System event | High |
| SC-03 | Admin processes refund | Admin | User action | Medium |
```

Priority: High (critical path / high traffic), Medium (important but not critical), Low (edge case).

## Scenario Detail Block

One block per scenario:

```markdown
## SC-01: Customer Places Order

**Derived from flow:** Customer Checkout Flow (happy path)
**Primary actor:** Customer
**Supporting actors:** System, Payment Gateway, Email Service
**Trigger:** Customer submits order on checkout page

### Steps (happy path)
1. Customer submits cart with shipping details
2. System validates cart contents and stock
3. System requests payment authorisation from Payment Gateway
4. Payment Gateway approves charge
5. System creates order record
6. System sends confirmation email via Email Service
7. Customer sees order confirmation screen

### Failure cases
| Step | Failure | System Response |
|------|---------|-----------------|
| Step 2 | Item out of stock | Return error, highlight unavailable items |
| Step 3 | Payment Gateway unreachable | Retry 3× with backoff; surface timeout error to user |
| Step 4 | Payment declined | Return decline reason; allow customer to retry with different card |
| Step 6 | Email Service unreachable | Log failure; order still confirmed; email retried async |

### Notes
- Steps 3-4 must complete within 5s (NFR latency constraint)
- Step 5 must be atomic with step 4 -- no charge without order record
```

## Criteria for Selecting Scenarios

Pick scenarios that are:
- **High traffic** -- happens frequently, worth optimising and documenting
- **High complexity** -- crosses multiple actors or has non-trivial branching
- **Failure-critical** -- a failure here has significant user or business impact
- **Controversial** -- the team has debated how to handle this flow

Skip scenarios that are:
- Trivially simple (one actor, one step, no failure path)
- Purely internal with no user-visible effect
- Already fully documented in existing specs

## Traceability Rule

Every scenario must reference:
1. The flow it was derived from (by name)
2. The actors it involves (must match actors in that flow)

This ensures sequence diagrams in Stage 03-04 stay connected to the business intent captured here.
