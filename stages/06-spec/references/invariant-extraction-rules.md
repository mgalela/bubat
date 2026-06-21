# Invariant Extraction Rules

Pull invariants from every source. Every §V item must be testable in code or tests.

| Source | Extract as §V |
|--------|---------------|
| Discovery NFRs | latency, availability, RTO/RPO, compliance mandates |
| Business flows | preconditions, postconditions, business rules |
| Bounded contexts | aggregate invariants, domain rules, boundary rules |
| Data model | NOT NULL, unique, FK integrity, enum values, length/range limits |
| Interface contracts | auth, SLA, error codes, retry/idempotency guarantees |
| Container sequences | ordering, consistency, side effects, failure behavior |
| Component sequences | internal validation, state transition, delegation guarantees |

Rules:
1. Number all invariants `§V.N`.
2. Use observable/testable wording.
3. Include source artifact in extraction map.
4. Do not invent invariants unsupported by upstream artifacts.
5. If missing source detail blocks testability, mark TODO in extraction map.
