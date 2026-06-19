# Stage 07: Spec Validation

Validate Stage 06 outputs (SPEC.md, interface specs, extraction map) for completeness, testability, consistency, and interface hygiene.
Produce a validation report with severity-rated findings and fix suggestions, and a scorecard summarizing pass/fail per check category.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Cavekit spec | `../06-spec/output/SPEC.md` | Full file | Primary validation target |
| Extraction map | `../06-spec/output/{{SYSTEM_SLUG}}-extraction-map.md` | Full file | Traceability coverage check |
| OpenAPI spec | `../06-spec/output/openapi.yaml` | Full file | Interface hygiene check (if exists) |
| proto3 definition | `../06-spec/output/{{SYSTEM_SLUG}}.proto` | Full file | Interface hygiene check (if exists) |
| Go interfaces | `../06-spec/output/{{SYSTEM_SLUG}}-interfaces.go` | Full file | Interface hygiene check (if exists) |
| TypeScript interfaces | `../06-spec/output/{{SYSTEM_SLUG}}-interfaces.ts` | Full file | Interface hygiene check (if exists) |
| Java interfaces | `../06-spec/output/{{SYSTEM_SLUG}}-interfaces.java` | Full file | Interface hygiene check (if exists) |
| System identity | `../../shared/system-meta.md` | Full file | Context for validation |
| Validation checklist | `references/validation-checklist.md` | Full file | All check definitions |
| Testability patterns | `references/testability-patterns.md` | Full file | Classifying invariant testability |

Load all available inputs. If SPEC.md is missing, stop: "Run stage 06 first."

## Stage Gate

Apply `../../shared/stage-gates.md`: input gate before work starts (SPEC.md required); stage audit, placeholder, and traceability gates before saving outputs.

## Process

1. Read SPEC.md — identify: §G (one line?), §C rows, §V rows, §I subsections, §T rows, §B headers.
2. Read extraction map — index all §V and §C entries that have source rows.
3. Read all available interface spec files — count `# TODO` / `// TODO` comments.

### Part A — Completeness Checks

4. §G: confirm single compressed line, no line breaks.
5. §C: every row has Source column populated. Flag any blank Source.
6. §V: every row has Source column populated. Every entry appears in extraction map. Flag missing entries.
7. §I: each subsection present (empty table is OK if explicit). Flag any subsection silently absent.
8. §T: every row has Status and Depends populated. Flag blank Depends (expect "—" for none).
9. §B: headers-only table present (even if empty).
10. Extraction map: every §C.N and §V.N has a row. Flag gaps.

### Part B — Testability Checks

11. For each §V invariant: classify using `references/testability-patterns.md`.
    - **Pass**: measurable condition with clear pass/fail (boolean, state assertion, sequence order, or threshold with full anatomy).
    - **Warn**: vague but fixable (e.g., "system should respond quickly" → rewrite as `[endpoint] latency ≤ 200ms [p99]`).
    - **Fail**: untestable as written (e.g., "system must be reliable") or threshold is physically impossible.
12. For every invariant that contains a numeric threshold (B1 triggered): apply threshold quality sub-checks B8–B12 from `references/validation-checklist.md`:
    - B8: value + unit + comparator all present (Blocking if not)
    - B9: scope present — named endpoint, operation, resource, or explicit `∀` (Warning if not)
    - B10: latency/throughput threshold has percentile or aggregation method (Warning if not)
    - B11: availability/uptime threshold has measurement window (Warning if not)
    - B12: value is physically achievable — not ≤ 0, not > 100% for rates, not < network baseline for cross-service latency (Blocking if impossible; Warning if unrealistic)
13. For every Warn or Fail invariant: generate a concrete rewritten version using the full threshold anatomy: `[scope] [metric] [comparator] [value][unit] [[percentile]] [[window]]`.

### Part C — Consistency Checks

14. §C vs §V: each NFR threshold in §C → corresponding measurable §V invariant exists. Flag missing.
15. §C internal conflicts: scan for contradictions (e.g., C3 says ≤100ms, C7 says ≤500ms for same operation).
16. §T dependency cycle: traverse Depends column — flag any cycle explicitly.
17. §I SLA vs §C NFR: every SLA value in §I.APIs and §I.External Systems consistent with §C performance constraints.
18. §V threshold conflicts (C7): for any two §V items targeting same operation + same metric + same percentile — flag if bound values differ. Different percentiles on same operation are not a conflict.

### Part D — Interface Hygiene

19. Count `# TODO` / `// TODO` comments across all interface spec files (openapi.yaml, .proto, -interfaces.*).
20. For each TODO: classify as Blocking (missing required field) or Non-blocking (optional enhancement).
21. Flag all Blocking TODOs as findings.

### Part E — Assemble Report

22. Group all findings by category: Completeness / Testability / Consistency / Interface Hygiene.
23. Assign severity per finding: Blocking (must fix before Stage 08) / Warning (should fix) / Info (nice to have).
24. For every Blocking and Warning finding: include specific fix text — not just "fix this", but the corrected invariant or instruction.
25. Pause at checkpoint — present finding summary before saving.

### Part F — Scorecard

26. Tally pass/warn/fail per check category.
27. Compute overall status: Pass (zero Blocking) / Warning (Warnings only) / Fail (any Blocking).

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 25 | Finding list: count by severity and category, top 5 Blocking findings with fix text | Fix issues in Stage 06 output, or accept warnings before report is saved |

## Audit

| Check | Pass Condition |
|-------|---------------|
| All §V rows evaluated | Every §V.N has a testability classification in report |
| All §C rows evaluated | Every §C.N has a completeness check result |
| Findings have fix text | Every Blocking/Warning finding includes rewritten version or specific fix instruction |
| Extraction map gaps listed | Every §V/§C gap is a named finding with severity |
| Severity assigned to all | No finding without severity rating |
| Scorecard totals match | Count in scorecard = sum of individual findings per category |

## Outputs

| Artifact | Location | Condition |
|----------|----------|-----------|
| Validation report | `output/{{SYSTEM_SLUG}}-spec-validation.md` | Always |
| Validation scorecard | `output/{{SYSTEM_SLUG}}-spec-scorecard.md` | Always |
