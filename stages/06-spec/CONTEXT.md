# Stage 06: Cavekit SPEC.md Bridge

Convert all C4ICM architecture outputs into a `SPEC.md` ready for [cavekit](https://github.com/JuliusBrussee/cavekit) spec-driven development.

Zero information loss. Every architectural decision, constraint, interface, and invariant must survive the translation. Compress prose → caveman encoding (fragments, symbols, pipe tables). Do NOT summarize away specifics.

## Inputs

| Source | File/Location | Section/Scope | Maps To |
|--------|--------------|---------------|---------|
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | Full file | §G, §C, §V |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | §C, §R |
| Business flows | `../01b-flow/output/{{SYSTEM_SLUG}}-flows.md` | Full file | §I, §V |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | §V, §T |
| Bounded context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-bounded-contexts.md` | Full file | §V, §C |
| Context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-context-map.md` | Full file | §I, §V |
| Domain data model | `../01d-data-model/output/{{SYSTEM_SLUG}}-data-model.md` | Full file | §V, §I |
| Container diagram + inventory | `../03-container/output/{{SYSTEM_SLUG}}-containers.md` | Full file | §I, §T |
| Interface contracts | `../03-container/output/{{SYSTEM_SLUG}}-contracts.md` | Full file | §I |
| Container sequences | `../03-container/output/{{SYSTEM_SLUG}}-sequences-l2.md` | Full file | §V, §T |
| Component diagrams | `../04-component/output/{{SYSTEM_SLUG}}-components.md` | Full file | §I, §T |
| Component scope | `../04-component/output/{{SYSTEM_SLUG}}-component-scope.md` | Full file | §T |
| Component sequences | `../04-component/output/{{SYSTEM_SLUG}}-sequences-l3.md` | Full file | §V |
| System identity | `../../shared/system-meta.md` | Full file | §G, §C |

Load all available inputs. If a file is missing (stage not yet run), note it as `[MISSING — run stage XX first]` in the relevant section. Do not skip sections.

## Caveman Encoding Rules

Apply to all prose in SPEC.md output:

| Rule | Example Before | Example After |
|------|---------------|---------------|
| Drop articles | "the system must validate" | "system ! validate" |
| Drop filler | "basically just sends" | "sends" |
| Fragments OK | "This requires authentication" | "! auth" |
| Short synonyms | "implements", "performs" | `→`, `=` |
| Must = `!` | "must not be null" | `! null` |
| Forbidden = `⊥` | "never expose raw password" | `⊥ expose raw pwd` |
| For all = `∀` | "for all users" | `∀ users` |
| Leads to = `→` | "triggers a notification" | `→ notification` |
| At most = `≤` | "at most 200ms" | `≤ 200ms` |
| At least = `≥` | "at least 99.9% uptime" | `≥ 99.9% uptime` |

Pipe tables over prose lists. Numbers over ranges where possible. Keep: technical terms, proper nouns, version numbers, URLs, field names, status codes.

## Process

1. Read `shared/system-meta.md` — extract system name, slug, purpose, tech stack.
2. Read `01-discovery` outputs — extract: one-line purpose, NFR table, tech constraints, ruled-out tech, compliance requirements.
3. Read `01b-flow` outputs — extract: user roles and their primary actions, scenario preconditions and postconditions as testable invariants.
4. Read `01c-bounded-context` outputs — extract: BC names, ubiquitous language terms, context map relationships (upstream/downstream), domain rules per BC.
5. Read `01d-data-model` outputs — extract: entity names, required fields, uniqueness constraints, FK relationships, storage hints.
6. Read `03-container` outputs — extract: container names + tech + purpose, all interface contracts (protocol, format, endpoint, auth, SLA, error handling), container-level sequence invariants.
7. Read `04-component` outputs — extract: component names per container, internal interfaces, component-level invariants from sequences.
8. Assemble §G — single compressed line from system purpose.
9. Assemble §C — all constraints: NFRs, tech locks, org constraints, compliance, ruled-out tech.
10. Assemble §I — all external surfaces: APIs, CLIs, files, env vars, event topics, external system contracts.
11. Assemble §R — if tech decisions log contains research findings or spike results, compress and list here.
12. Assemble §V — number every testable invariant. Draw from: BC domain rules, data model constraints, scenario postconditions, sequence diagram guarantees, NFR thresholds. Every invariant must be verifiable in code or tests.
13. Assemble §T — generate initial task list from container inventory. One task cluster per container. Use `[ ]` status. Sequence by dependency order from container diagram.
14. Add §B — empty table with headers only.
15. Generate extraction map artifact.
16. Pause at checkpoint.
17. Save both artifacts to `output/`.

## Invariant Extraction Rules

Pull invariants from every source, not just one. Miss nothing:

| Source | What to Extract as §V |
|--------|----------------------|
| Discovery NFRs | Performance thresholds, availability %, RTO/RPO values, compliance mandates |
| Business flows | Pre/postconditions per scenario, business rules enforced in flow |
| Bounded contexts | Aggregate invariants, ubiquitous language constraints, BC boundary rules |
| Data model | NOT NULL constraints, unique keys, FK integrity, valid enum values, field length limits |
| Interface contracts | SLA thresholds, auth requirements, error code guarantees, retry limits |
| Sequence diagrams | Ordering invariants, idempotency requirements, rollback guarantees |
| Tech decisions | Patterns that mandate behavior (e.g., "event-sourced → events are immutable") |

## §T Task Generation Rules

Map containers to tasks by dependency order (leaf containers first, orchestrators last):

```
§T
| # | Task | Status | Depends |
|---|------|--------|---------|
| T1 | build [container-name] ([tech]) | [ ] | — |
| T2 | build [container-name] ([tech]) | [ ] | T1 |
...
```

For containers that have Level 3 component diagrams, expand into subtasks:
```
| T2.1 | impl [component-name] | [ ] | T1 |
| T2.2 | impl [component-name] | [ ] | T2.1 |
```

Status symbols: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 14 | Invariant count by source, task count, any MISSING inputs | Fill gaps, confirm coverage before save |

## Audit

| Check | Pass Condition |
|-------|---------------|
| §G is one line | Single compressed sentence, no line breaks |
| All NFRs in §C | Every row from discovery NFR table appears somewhere in §C or §V |
| All contracts in §I | Every entry from contracts artifact has an §I entry |
| Invariants numbered | All §V items use `§V.N` format |
| No prose paragraphs | Every section uses fragments, symbols, or pipe tables — zero paragraph prose |
| No placeholders | No `{{PLACEHOLDER}}` strings remain |
| MISSING inputs noted | Any skipped source files explicitly noted in affected sections |
| §T ordered by dependency | No task depends on a task with a higher number unless explicitly noted |
| Extraction map complete | Every §V item traces back to a source artifact |

## Output

| Artifact | Location | Format |
|----------|----------|--------|
| Cavekit spec | `output/SPEC.md` | Drop this file into project root to start cavekit loop |
| Extraction map | `output/{{SYSTEM_SLUG}}-extraction-map.md` | Traceability: which C4ICM section produced which SPEC entry |

---

## SPEC.md Template

Output must follow this exact structure. Fill every section. Do not add or remove section headers.

```markdown
# SPEC — {{SYSTEM_NAME}}
> C4ICM bridge v1 · generated {{DATE}} · source: C4ICM/stages/06-spec/output/{{SYSTEM_SLUG}}-extraction-map.md

## §G GOAL
{{one compressed line: what system does, for whom, core value}}

## §C CONSTRAINTS
<!-- NFRs, tech locks, compliance, ruled-out tech, org constraints -->
| # | Constraint | Source |
|---|-----------|--------|
| C1 | {{NFR or tech lock}} | discovery/NFR |
| C2 | ⊥ {{forbidden tech or pattern}} | tech-decisions |
...

## §I INTERFACES
<!-- All external surfaces: APIs, CLIs, files, env vars, event topics, external systems -->

### External Systems
| Consumer → Producer | Protocol | Format | Auth | SLA | Notes |
|--------------------|----------|--------|------|-----|-------|
| {{container}} → {{ext-system}} | HTTPS | JSON | Bearer | ≤Xs | {{key detail}} |

### APIs / Endpoints
| Method | Path | Auth | Request | Response | Errors |
|--------|------|------|---------|----------|--------|
| POST | /{{path}} | {{auth}} | {{key fields}} | {{key fields}} | {{codes}} |

### Events / Topics
| Topic | Producer | Consumer | Format | Key Fields |
|-------|----------|----------|--------|-----------|
| {{topic}} | {{container}} | {{container}} | JSON | {{fields}} |

### Files / Config
| Name | Type | Owner | Purpose |
|------|------|-------|---------|
| {{name}} | env var / file / CLI flag | {{container}} | {{purpose}} |

## §R RESEARCH
<!-- Optional. Only populate if tech-decisions log contains spike findings or external research. -->
| # | Finding | Source | Date |
|---|---------|--------|------|

## §V INVARIANTS
<!-- Numbered. Testable. Every item verifiable in code or tests. -->
| # | Invariant | Source |
|---|-----------|--------|
| §V.1 | {{testable rule}} | {{source artifact}} |
...

## §T TASKS
| # | Task | Status | Depends |
|---|------|--------|---------|
| T1 | {{task}} | [ ] | — |
...

## §B BUGS
| # | Bug | Status | Fix |
|---|-----|--------|-----|
```

---

## Extraction Map Template

```markdown
# {{SYSTEM_SLUG}}-extraction-map.md
<!-- Traceability: C4ICM artifact → SPEC.md entry -->

| SPEC Entry | Source Artifact | Source Section | Verbatim Excerpt (truncated) |
|------------|----------------|----------------|------------------------------|
| §G | system-meta.md | purpose | "{{excerpt}}" |
| §C.1 | {slug}-discovery.md | NFR / Availability | "{{excerpt}}" |
| §V.3 | {slug}-bounded-contexts.md | Order BC / aggregate rule | "{{excerpt}}" |
...
```

Every §V and §C entry must have a row in this map. §I and §T entries are encouraged but optional.
