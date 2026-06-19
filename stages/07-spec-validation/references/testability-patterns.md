# Testability Patterns

Classify each §V invariant as Pass / Warn / Fail. For every Warn/Fail: generate rewrite.

## Classification Rules

### Pass — invariant is directly testable as written

Patterns that pass without rewrite:

| Pattern | Example |
|---------|---------|
| Numeric threshold with full anatomy (see below) | `[POST /checkout] response time ≤ 200ms [p99]` |
| Boolean assertion | `token ! null on login success` |
| Cardinality constraint | `∀ order: line_items ≥ 1` |
| State machine assertion | `order status ∈ {pending, confirmed, shipped, cancelled}` |
| Uniqueness constraint | `email unique per tenant` |
| Ordering invariant | `payment ! process before inventory reserve` |
| Idempotency assertion | `POST /checkout idempotent ∀ duplicate request_id` |
| Error code guarantee | `invalid token → 401, expired token → 401, no token → 401` |
| Immutability assertion | `events ⊥ mutate after publish` |
| Format constraint | `phone_number matches ^\\+[1-9]\\d{7,14}$` |

## Threshold Quality Sub-Check

Apply to every invariant that contains a numeric threshold, before assigning Pass.

### Required components (missing any → Warn minimum)

| Component | Required | If absent | Example |
|-----------|----------|-----------|---------|
| Value | Yes | Fail | `200` |
| Unit | Yes | Fail | `ms`, `%`, `req/s`, `bytes`, `MB` |
| Comparator | Yes | Fail | `≤`, `≥`, `=`, `∈ [lo, hi]` |
| Scope | Yes | Warn | `[POST /checkout]`, `[∀ write ops]`, `[login endpoint]` |
| Percentile / aggregation | For latency / throughput metrics | Warn | `p99`, `p95`, `p50`, `max`, `avg` |
| Measurement window | For availability / rate metrics | Warn | `rolling 30d`, `per calendar month`, `per request burst` |
| Baseline load | For performance metrics | Info | `at 500 concurrent users`, `at 1000 req/s` |

**Threshold anatomy — minimum for Pass:**

```
[scope] [metric] [comparator] [value][unit] [[percentile]]
```

Examples:
- `[POST /checkout] response time ≤ 200ms [p99]` → Pass
- `[all endpoints] response time ≤ 500ms [p95]` → Pass (broad scope OK if explicit)
- `response time ≤ 200ms` → Warn (missing scope, missing percentile)
- `≤ 200ms` → Warn (missing scope, metric name, percentile)
- `respond quickly` → Fail (no threshold at all)

**Availability / uptime anatomy — minimum for Pass:**

```
[scope] uptime ≥ [value]% [measurement window]
```

Examples:
- `service uptime ≥ 99.9% [rolling 30d]` → Pass
- `uptime ≥ 99.9%` → Warn (missing scope and window)
- `must be available` → Fail

### Impossible / unrealistic thresholds → Fail or Warn

| Pattern | Classification | Reason |
|---------|---------------|--------|
| `≤ 0ms` | Fail | Physically impossible |
| `≥ 100.1%` availability | Fail | Mathematically impossible |
| `≤ 0` count/size | Fail | Impossible unless constraint means "zero allowed" — rewrite as boolean |
| `≤ 1ms` for cross-network call | Warn | Unrealistic for network I/O; flag with "verify against network baseline" |
| Threshold stricter than §C NFR without justification | Warn | May be intentional margin — ask to confirm or cite ADR |

### Threshold conflicts across §V items

If two §V invariants reference same operation + same metric with different thresholds:
- Example: `§V.3: [POST /orders] latency ≤ 200ms [p99]` and `§V.11: [POST /orders] latency ≤ 500ms [p95]` — different percentiles, not a conflict
- Example: `§V.3: [POST /orders] latency ≤ 200ms [p99]` and `§V.11: [POST /orders] latency ≤ 500ms [p99]` — same percentile, conflicting bounds → Blocking

Flag as C7 finding (see validation-checklist.md Category C).

---

### Warn — testable intent, untestable phrasing

Patterns that need rewording:

| Anti-pattern | Problem | Rewrite instruction |
|--------------|---------|---------------------|
| `response time ≤ 200ms` (no scope, no percentile) | Incomplete threshold | Add scope + percentile: `[endpoint] response time ≤ 200ms [p99]` |
| `uptime ≥ 99.9%` (no window) | Incomplete threshold | Add window: `uptime ≥ 99.9% [rolling 30d]` |
| "respond quickly" | No threshold | Add measured SLA from §I or §C |
| "should handle errors gracefully" | No observable outcome | Specify: which error, which HTTP/gRPC code, which response body field |
| "must be available" | No SLA figure | Pull uptime % from §C NFR |
| "data must not be lost" | No scope | Scope to: which entity, which operation, which failure scenario |
| "should validate input" | No criteria | List: which fields, which rules, which error response |
| "must scale" | No metric | Add: RPS target, latency at target, from §C |
| "auth required" (alone) | Ambiguous: which method | Specify: Bearer / API key / mTLS; which endpoints |

Rewrite formula: `[scope] [metric] [comparator] [value][unit] [[percentile]] [[window]]`

### Fail — invariant cannot be tested as written

Patterns that must be decomposed:

| Anti-pattern | Problem | Fix instruction |
|--------------|---------|-----------------|
| "system must be secure" | Not a condition | Decompose into specific §V items (auth, encryption, input validation, etc.) |
| "system must be reliable" | Not measurable | Replace with uptime %, RTO, RPO from §C |
| "user experience must be good" | Subjective | Remove or replace with measurable proxy (load time, error rate) |
| "comply with regulations" | Underdefined | Name specific regulation + testable control (e.g., `⊥ store card PAN unencrypted → PCI-DSS 3.4`) |
| "follow best practices" | No condition | Remove or link to specific documented standard with testable criteria |

## Rewrite Template

```
Original: "{{original text}}"
Classification: {{Pass / Warn / Fail}}
Reason: {{one sentence why}}
Rewrite: "{{rewritten invariant using caveman encoding}}"
Test type: {{unit / integration / e2e / manual}}
```

## Special Cases

| Case | How to handle |
|------|--------------|
| External system SLA (out of our control) | Pass — but label source as assumption, add B7 Info finding |
| Regulatory compliance invariant | Warn if regulation named but control not specified; Pass if control explicit |
| Architecture constraint from tech decision | Pass if phrased as a falsifiable code-level rule; Warn if phrased as a process rule |
| Performance invariant with p50/p95/p99 split | Pass — more precise than single threshold (still needs scope) |
| Invariant that duplicates another §V | Info — flag duplicate, suggest merge |
