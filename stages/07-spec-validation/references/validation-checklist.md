# Validation Checklist

Reference for Stage 07. All checks applied against Stage 06 outputs.

## Category A — Completeness

| Check ID | Target | Pass Condition |
|----------|--------|----------------|
| A1 | §G | Single compressed line. No line break. No placeholder. |
| A2 | §C rows | Every row has non-blank Source column. |
| A3 | §V rows | Every row has non-blank Source column. |
| A4 | §V ↔ extraction map | Every §V.N has a corresponding row in extraction map. |
| A5 | §C ↔ extraction map | Every §C.N has a corresponding row in extraction map. |
| A6 | §I.External Systems | Subsection present. If no external systems: explicit empty table. |
| A7 | §I.APIs / Endpoints | Subsection present. If no HTTP APIs: explicit empty table. |
| A8 | §I.gRPC Services | Subsection present. If no gRPC: explicit empty table. |
| A9 | §I.Events / Topics | Subsection present. If no events: explicit empty table. |
| A10 | §I.Files / Config | Subsection present. If no files/config: explicit empty table. |
| A11 | §I.Module Interfaces | Subsection present. If no components: explicit empty table. |
| A12 | §T rows | Every row has Status and Depends populated. |
| A13 | §B | Headers-only table present (empty body is OK). |
| A14 | §V count | At least one §V invariant per upstream stage that ran. |

## Category B — Testability

### B1–B7: Invariant Type Classification

| Check ID | Pattern | Classification |
|----------|---------|----------------|
| B1 | Invariant contains a numeric threshold (any number + comparator present) | Proceed to B8–B12 threshold quality checks |
| B2 | Invariant asserts boolean state (is authenticated, is idempotent, is unique) | Pass |
| B3 | Invariant asserts sequence order (A before B, retry after C) | Pass |
| B4 | Invariant uses vague qualifier (quickly, reliably, well, appropriately) | Warn — rewrite with threshold |
| B5 | Invariant says "should" without measurable condition | Warn — replace with `!` + measurable condition |
| B6 | Invariant has no verifiable output (e.g., "system must be secure") | Fail — decompose into specific checks |
| B7 | Invariant references an external system behavior outside control | Info — mark as assumption, not test case |

### B8–B12: Threshold Quality (apply only when B1 triggered)

| Check ID | Check | Pass Condition | If Fail |
|----------|-------|----------------|---------|
| B8 | Threshold has value + unit + comparator | All three present | Blocking — threshold incomplete, not testable |
| B9 | Threshold has scope (named endpoint, operation, resource, or `∀` explicit) | Scope present | Warning — add scope; `[all]` is acceptable if explicit |
| B10 | Latency / throughput threshold has percentile or aggregation | p50/p95/p99/max/avg present | Warning — bare value tests wrong population |
| B11 | Availability / uptime threshold has measurement window | Window present (e.g., `rolling 30d`) | Warning — add window; determines SLO calculation period |
| B12 | Threshold value is physically achievable | Value > 0; availability ≤ 100%; latency > network baseline | Blocking if impossible; Warning if unrealistic (≤1ms cross-network) |

## Category C — Consistency

| Check ID | Check | Pass Condition |
|----------|-------|----------------|
| C1 | §C NFR → §V | Every performance/availability NFR in §C has ≥1 §V invariant with same or stricter threshold |
| C2 | §C conflicts | No two §C rows set contradictory bounds for same operation/resource |
| C3 | §T dependency cycle | Traverse Depends column: no cycle (A→B→A or longer chain) |
| C4 | §I SLA vs §C NFR | Every SLA value in §I table rows ≤ corresponding §C performance constraint |
| C5 | §T dependency order | Task T_N that depends on T_M has M < N (or cycle explicitly justified) |
| C6 | Interface spec → §I | Every openapi.yaml path exists as row in §I.APIs. Every proto rpc exists as row in §I.gRPC. |
| C7 | §V threshold conflicts | No two §V items target same operation + same metric + same percentile with different bound values |

## Category D — Interface Hygiene

| Check ID | Target | Pass Condition |
|----------|--------|----------------|
| D1 | openapi.yaml TODOs | Zero `# TODO` with "missing" or "insufficient" |
| D2 | .proto TODOs | Zero `// TODO` with "missing" or "insufficient" |
| D3 | -interfaces.* TODOs | Count of `// TODO: derive from sequences` noted (Non-blocking) |
| D4 | openapi.yaml schema refs | All `$ref` targets exist in `components/schemas` |
| D5 | proto syntax | All message field types are valid proto3 scalar or defined message types |
| D6 | Interface names | Interface/type names in language files match component labels in Stage 04 diagrams exactly |

## Severity Assignment

| Severity | When |
|----------|------|
| Blocking | Any A-series gap; any B6 (Fail testability); B8 (missing value/unit/comparator); B12 (impossible threshold); any D1/D2 (required field TODO); any C1 NFR without §V; any C3 cycle; any C7 §V threshold conflict |
| Warning | B4/B5 (vague but fixable); B9 (missing scope); B10 (missing percentile); B11 (missing availability window); B12 (unrealistic but not impossible); C4 SLA inconsistency; C6 spec/§I mismatch; D3 derive-TODO count > 20% of interfaces |
| Info | B7 (external assumption); B10 baseline load absent; D3 derive-TODO count ≤ 20%; A13 empty §B (expected) |
