# Stage 06: Cavekit SPEC.md Bridge + Interface Specs

Convert all BUBAT architecture outputs into:
1. `SPEC.md` — ready for [cavekit](https://github.com/JuliusBrussee/cavekit) spec-driven development
2. Interface spec artifacts — OpenAPI YAML, proto3, and language-specific module interfaces

Zero information loss. Every architectural decision, constraint, interface, and invariant must survive the translation.

## Inputs

| Source | File/Location | Section/Scope | Maps To |
|--------|--------------|---------------|---------|
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | Full file | §G, §C, §V |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | §C, §R |
| Business flows | `../01b-flow/output/{{SYSTEM_SLUG}}-flows.md` | Full file | §I, §V |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | §V, §T |
| Bounded context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-bounded-contexts.md` | Full file | §V, §C |
| Context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-context-map.md` | Full file | §I, §V |
| Domain entity inventory | `../01d-data-model/output/{{SYSTEM_SLUG}}-domain-entities.md` | Full file | §V, §I |
| Cross-BC data dependencies | `../01d-data-model/output/{{SYSTEM_SLUG}}-data-dependencies.md` | Full file | §I, §V |
| Storage hints | `../01d-data-model/output/{{SYSTEM_SLUG}}-storage-hints.md` | Full file | §C, §T |
| Container diagram + inventory | `../03-container/output/{{SYSTEM_SLUG}}-containers.md` | Full file | §I, §T |
| Interface contracts | `../03-container/output/{{SYSTEM_SLUG}}-contracts.md` | Full file | §I, OpenAPI, proto |
| Container sequences | `../03-container/output/{{SYSTEM_SLUG}}-sequences-l2.md` | Full file | §V, §T |
| Component diagrams | `../04-component/output/{{SYSTEM_SLUG}}-components.md` | Full file | §I, §T, interfaces |
| Component scope | `../04-component/output/{{SYSTEM_SLUG}}-component-scope.md` | Full file | §T |
| Component sequences | `../04-component/output/{{SYSTEM_SLUG}}-sequences-l3.md` | Full file | §V, interfaces |
| System identity | `../../shared/system-meta.md` | Full file | §G, §C, interface format detection |
| Interface gen rules | `references/interface-gen-rules.md` | Full file | Which formats to generate |
| OpenAPI template | `references/openapi-template.yaml` | Full file | openapi.yaml structure |
| Proto template | `references/proto-template.proto` | Full file | {slug}.proto structure |
| Module interface patterns | `references/module-interface-patterns.md` | Full file | Language-specific interface stubs |

Load all available inputs. If a file is missing (stage not yet run), note it as `[MISSING — run stage XX first]` in the relevant section. Do not skip sections.

## Stage Gate

Apply `../../shared/stage-gates.md`: input gate before work starts; stage audit, placeholder, and traceability gates before saving. Bridge gate (G7) before saving SPEC.md.

## Caveman Encoding Rules

Apply to all prose in SPEC.md output only (not to interface spec files):

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

### Part A — SPEC.md (cavekit bridge)

1. Read `shared/system-meta.md` — extract system name, slug, purpose, tech stack, interface formats.
2. Read `01-discovery` outputs — extract: one-line purpose, NFR table, tech constraints, ruled-out tech, compliance requirements.
3. Read `01b-flow` outputs — extract: user roles and their primary actions, scenario preconditions and postconditions as testable invariants.
4. Read `01c-bounded-context` outputs — extract: BC names, ubiquitous language terms, context map relationships (upstream/downstream), domain rules per BC.
5. Read `01d-data-model` outputs — extract: entity names, required fields, uniqueness constraints, FK relationships, storage hints.
6. Read `03-container` outputs — extract: container names + tech + purpose, all interface contracts (protocol, format, endpoint, auth, SLA, error handling), container-level sequence invariants.
7. Read `04-component` outputs — extract: component names per container, internal interfaces, component-level invariants from sequences.
8. Assemble §G — single compressed line from system purpose.
9. Assemble §C — all constraints: NFRs, tech locks, org constraints, compliance, ruled-out tech.
10. Assemble §I — all external surfaces: APIs, CLIs, files, env vars, event topics, external system contracts. Add pointer line for each generated spec file: `→ see openapi.yaml`, `→ see {slug}.proto`, `→ see {slug}-interfaces.{ext}`.
11. Assemble §R — if tech decisions log contains research findings or spike results, compress and list here.
12. Assemble §V — number every testable invariant. Draw from: BC domain rules, data model constraints, scenario postconditions, sequence diagram guarantees, NFR thresholds. Every invariant must be verifiable in code or tests.
13. Assemble §T — generate initial task list from container inventory. One task cluster per container. Use `[ ]` status. Sequence by dependency order from container diagram. Expand containers with Level 3 diagrams into subtasks.
14. Add §B — empty table with headers only.
15. Generate extraction map artifact.

### Part B — Interface Specs

16. Read `{{INTERFACE_FORMATS}}` from system-meta.md. If value is "Auto-detect", apply rules from `references/interface-gen-rules.md` to determine formats.
17. **OpenAPI** (if HTTP contracts exist):
    a. For each contract row where `Protocol` = HTTPS/HTTP: map Endpoint → path+method, Key Request Fields → requestBody schema, Key Response Fields → response schema, Auth → security scheme, Error Handling → response codes, SLA → `x-sla` extension.
    b. Collect all unique schemas into `components/schemas`.
    c. Assemble one `openapi.yaml` using structure from `references/openapi-template.yaml`.
    d. If contract data is insufficient for a field: add `# TODO: [field name] missing in contracts.md`.
18. **proto3** (if gRPC contracts exist):
    a. For each contract row where `Protocol` = gRPC: derive service name from Producer label, rpc method from Endpoint field, request/response messages from Key Request/Response Fields.
    b. Group rpcs by Producer into one `service` block each.
    c. Assemble one `{slug}.proto` using structure from `references/proto-template.proto`.
    d. Choose rpc streaming type based on Direction field: Synchronous → unary, Asynchronous (fire-and-forget) → client stream or unary with empty response.
19. **Language interfaces** (if Go / TypeScript / Java in tech stack or INTERFACE_FORMATS):
    a. For each component in each Level 3 diagram:
       - Determine interface kind from component type tag using table in `references/interface-gen-rules.md`.
       - Derive method names from `sequences-l3.md` interactions involving this component.
       - If sequences-l3 missing or component not covered: generate skeleton from name + type, add `// TODO: derive from sequences`.
    b. Group interfaces by container.
    c. Assemble interface file(s) using patterns from `references/module-interface-patterns.md`.
    d. Replace all `{{EntityName}}`, `{{ContextName}}`, `{{ExternalSystem}}` placeholders with actual component names from the diagrams.
20. Pause at checkpoint — present interface spec summary before saving.
21. Save all artifacts to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 15 | Invariant count by source, task count, any MISSING inputs | Fill gaps, confirm coverage before Part B |
| Step 20 | Interface spec summary: formats generated, endpoint count (OpenAPI), service count (proto), interface count (language) | Confirm accuracy before save |

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
```

For containers with Level 3 component diagrams, expand into subtasks:
```
| T2.1 | impl [component-name] | [ ] | T1 |
| T2.2 | impl [component-name] | [ ] | T2.1 |
```

Status symbols: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked

## Audit

| Check | Pass Condition |
|-------|---------------|
| §G is one line | Single compressed sentence, no line breaks |
| All NFRs in §C | Every row from discovery NFR table appears in §C or §V |
| All contracts in §I | Every entry from contracts artifact has an §I entry |
| §I references generated specs | §I includes `→ see` pointer for each generated spec file |
| Invariants numbered | All §V items use `§V.N` format |
| No prose paragraphs | Every SPEC.md section uses fragments, symbols, or pipe tables |
| No placeholders | No `{{PLACEHOLDER}}` strings remain in SPEC.md |
| MISSING inputs noted | Any skipped source files explicitly noted in affected sections |
| §T ordered by dependency | No task depends on task with higher number unless explicitly noted |
| Extraction map complete | Every §V item traces back to a source artifact |
| OpenAPI completeness | Every HTTP contract row has ≥1 path entry; no contract row silently skipped |
| proto completeness | Every gRPC contract row has ≥1 rpc entry grouped by Producer |
| Interface completeness | Every component in a Level 3 diagram has ≥1 interface declaration (when language target applies) |
| Interface names match diagrams | Interface type names match component labels exactly (no paraphrasing) |
| TODOs documented | Any field with insufficient source data has `# TODO` comment; not silently omitted |

## Outputs

| Artifact | Location | Condition |
|----------|----------|-----------|
| Cavekit spec | `output/SPEC.md` | Always |
| Extraction map | `output/{{SYSTEM_SLUG}}-extraction-map.md` | Always |
| OpenAPI spec | `output/openapi.yaml` | HTTP contracts exist |
| proto3 definition | `output/{{SYSTEM_SLUG}}.proto` | gRPC contracts exist |
| Go interfaces | `output/{{SYSTEM_SLUG}}-interfaces.go` | Go in stack or formats |
| TypeScript interfaces | `output/{{SYSTEM_SLUG}}-interfaces.ts` | TS/Node in stack or formats |
| Java interfaces | `output/{{SYSTEM_SLUG}}-interfaces.java` | Java/Kotlin in stack or formats |

---

## SPEC.md Template

Output must follow this exact structure. Fill every section. Do not add or remove section headers.

```markdown
# SPEC — {{SYSTEM_NAME}}
> BUBAT bridge v1 · generated {{DATE}} · source: BUBAT/stages/06-spec/output/{{SYSTEM_SLUG}}-extraction-map.md

## §G GOAL
{{one compressed line: what system does, for whom, core value}}

## §C CONSTRAINTS
<!-- NFRs, tech locks, compliance, ruled-out tech, org constraints -->
| # | Constraint | Source |
|---|-----------|--------|
| C1 | {{NFR or tech lock}} | discovery/NFR |
| C2 | ⊥ {{forbidden tech or pattern}} | tech-decisions |

## §I INTERFACES
<!-- All external surfaces: APIs, CLIs, files, env vars, event topics, external systems -->
<!-- Generated spec files listed below each subsection where applicable -->

### External Systems
| Consumer → Producer | Protocol | Format | Auth | SLA | Notes |
|--------------------|----------|--------|------|-----|-------|
| {{container}} → {{ext-system}} | HTTPS | JSON | Bearer | ≤Xs | {{key detail}} |

### APIs / Endpoints
<!-- → see openapi.yaml for full OpenAPI 3.1 spec -->
| Method | Path | Auth | Request | Response | Errors |
|--------|------|------|---------|----------|--------|
| POST | /{{path}} | {{auth}} | {{key fields}} | {{key fields}} | {{codes}} |

### gRPC Services
<!-- → see {{SYSTEM_SLUG}}.proto for full proto3 definition -->
| Service | RPC | Request | Response | Notes |
|---------|-----|---------|----------|-------|
| {{ServiceName}} | {{RpcMethod}} | {{MessageName}} | {{MessageName}} | {{streaming type}} |

### Events / Topics
| Topic | Producer | Consumer | Format | Key Fields |
|-------|----------|----------|--------|-----------|
| {{topic}} | {{container}} | {{container}} | JSON | {{fields}} |

### Files / Config
| Name | Type | Owner | Purpose |
|------|------|-------|---------|
| {{name}} | env var / file / CLI flag | {{container}} | {{purpose}} |

### Module Interfaces
<!-- → see {{SYSTEM_SLUG}}-interfaces.{ext} for full language-specific declarations -->
| Component | Type | Container | Interface Kind |
|-----------|------|-----------|---------------|
| {{component}} | [Service] | {{container}} | {{ContextName}}Service |

## §R RESEARCH
<!-- Optional. Only populate if tech-decisions log contains spike findings or external research. -->
| # | Finding | Source | Date |
|---|---------|--------|------|

## §V INVARIANTS
<!-- Numbered. Testable. Every item verifiable in code or tests. -->
| # | Invariant | Source |
|---|-----------|--------|
| §V.1 | {{testable rule}} | {{source artifact}} |

## §T TASKS
| # | Task | Status | Depends |
|---|------|--------|---------|
| T1 | {{task}} | [ ] | — |

## §B BUGS
| # | Bug | Status | Fix |
|---|-----|--------|-----|
```

---

## Extraction Map Template

```markdown
# {{SYSTEM_SLUG}}-extraction-map.md
<!-- Traceability: BUBAT artifact → SPEC.md entry -->

| SPEC Entry | Source Artifact | Source Section | Verbatim Excerpt (truncated) |
|------------|----------------|----------------|------------------------------|
| §G | system-meta.md | purpose | "{{excerpt}}" |
| §C.1 | {slug}-discovery.md | NFR / Availability | "{{excerpt}}" |
| §V.3 | {slug}-bounded-contexts.md | Order BC / aggregate rule | "{{excerpt}}" |
| §I/openapi | {slug}-contracts.md | HTTP contract rows | "→ openapi.yaml paths" |
| §I/proto | {slug}-contracts.md | gRPC contract rows | "→ {slug}.proto services" |
| §I/interfaces | {slug}-components.md + sequences-l3 | component type tags | "→ {slug}-interfaces.{ext}" |
```

Every §V and §C entry must have a row in this map. §I entries are encouraged but optional.
