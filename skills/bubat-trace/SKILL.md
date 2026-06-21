---
name: bubat-trace
description: Locate architecture artifacts by keyword, stage, concept, or artifact name with ultra-cheap grep-first manifest lookup. Use when user types `where <term>`, `trace <term>`, `trace summary <n>`, `find artifact <term>`, or asks where specific architecture information lives.
---

# BUBAT Trace / Where

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Goal:
- help user find architecture information fast after slim-down from `CLAUDE.md`
- keep default lookup cheap
- do not only list file paths
- return ranked matches with short summaries so user may decide whether to open file

## Triggers

Accept:
- `where <term>`
- `trace <term>`
- `trace summary <n>`
- `find artifact <term>`
- `locate <term>`
- `trace deep <term>` for more expensive fallback
- natural questions like `di mana doc contract?`, `cari payment flow`, `trace OrderCreated`

## Cost Model

Default mode = cheap shortlist.

Cheap shortlist must:
- grep `${WORKSPACE_ROOT}/shared/artifact-manifest.ndjson` first
- avoid reading `${WORKSPACE_ROOT}/shared/artifact-index.json` on first pass unless user asks `trace summary <n>`
- avoid reading `${WORKSPACE_ROOT}/shared/triage-index.json` unless query hints at change/impact/history
- avoid reading full artifact bodies on first pass
- avoid broad grep/search when manifest is missing or empty
- return top 3 matches plus open options

Deep mode allowed only when:
- user explicitly asks `trace deep <term>`
- or user selects `open <n>` after shortlist

If manifest or indexes are missing or empty, fail cheap:
- do not scan whole workspace
- do not grep broad keyword sets outside manifest
- return likely canonical artifacts from registries
- recommend `refresh index`
- allow user to opt into `trace deep <term>`

## Process

1. Parse mode first:
   - `trace <term>` / `where <term>` = manifest shortlist mode
   - `trace summary <n>` = detail-index mode for previously listed result number
   - `trace deep <term>` = narrow content-search mode
2. Read/search only files needed for current mode:
   - shortlist mode: grep `${WORKSPACE_ROOT}/shared/artifact-manifest.ndjson`
   - summary mode: read `${WORKSPACE_ROOT}/shared/artifact-index.json`
   - impact/history-oriented shortlist may also read `${WORKSPACE_ROOT}/shared/triage-index.json`
   - read `${WORKSPACE_ROOT}/shared/stage-index.md` and `${WORKSPACE_ROOT}/shared/output-catalog.md` only when manifest missing/empty or when registry fallback needed
   - read `${WORKSPACE_ROOT}/shared/system-meta.md` only if slug needed and not already obvious
3. Parse query intent into one or more classes:
   - stage id/name (`03`, `container`, `04-component`)
   - artifact name (`contracts`, `component-code-map`, `SPEC`, `architecture`)
   - architecture concept (`flow`, `bounded context`, `entity`, `contract`, `component`, `code map`, `OpenAPI`)
   - domain term (`payment`, `order`, `invoice`, event name, API path, symbol, component name)
4. Use manifest and registries to map likely owner stages and canonical artifact names before any file-content search.
5. Search in this order:
   - shortlist mode: grep exact and fuzzy terms in `shared/artifact-manifest.ndjson`
   - if query implies change impact, triage history, or pending work: exact and fuzzy matches in `shared/triage-index.json`
   - summary mode: look up selected result path in `shared/artifact-index.json`
   - registry hits from `shared/output-catalog.md` and expected stage output paths from `shared/stage-index.md` only if manifest missing/empty or tie-break needed
   - if manifest grep has usable hits, stop there
   - if manifest missing or empty, stop with registry-guided shortlist and recommend `refresh index`
   - only in explicit deep mode: run narrow grep/search against likely canonical artifact files under `${WORKSPACE_ROOT}/stages/<likely-stage>/output/`
   - search `${WORKSPACE_ROOT}/triage/` only if query asks for impact/change/history and only in deep mode or indexed mode
   - read actual artifact excerpts only after user asks to open result or explicitly requests deep trace
6. Rank results:
   - exact artifact name match
   - exact stage owner match
   - filename/path match
   - keyword hit from artifact index
   - heading hit from artifact index
   - grep hit in content search
   - triage hit as supporting context, not primary source, unless user asked about pending change impact
7. Shortlist mode must use manifest grep hits on title/path/keywords only. Do not load detail summaries on first pass.
8. `trace summary <n>` may use `shared/artifact-index.json` to show 1 short summary and up to 4 headings for chosen result only.
9. If manifest missing or stale:
   - say so briefly
   - recommend `refresh index`
   - do not continue into broad grep fallback in default mode
   - instead return registry-guided canonical artifact shortlist
10. Ask whether to open one or more files. If user selects, read chosen file(s) and present targeted excerpt first, full file only on request.
11. For `open <n>` or `open path <...>`:
   - read only targeted file
   - prefer matching heading block or nearby lines
   - avoid full file unless user says `open full <n>` or `open full path <...>`
12. For explicit `trace deep <term>` fallback:
   - restrict search to likely owner stages from heuristic map and registries
   - search max 3 canonical artifact files first; only expand if user asks
   - do not search `docs/`, `references/`, `commands/`, or whole workspace by default
   - surface max 10 grep hits
   - read max 2 targeted excerpts, 60 lines each

## Output Format

```text
Trace: <user query>

Top matches
1. <artifact> — <stage>
   Why: <manifest/registry/triage match>
   Title: <short title>
   Path: <workspace-relative path>

2. ...

Index:
- source: artifact-manifest.ndjson / triage-index / registry / narrow grep
- status: fresh / missing / stale-possible

If manifest missing/empty:
- no deep search run
- next: `refresh index` or `trace deep <term>`

Next:
- `trace summary 1`
- `open 1`
- `open full 1`
- `open path <workspace-relative-path>`
```

For `trace summary <n>`:

```text
Trace summary: <n>

<artifact> — <stage>
Summary: <1 sentence>
Headings:
- <heading>
- <heading>
- <heading>
Path: <workspace-relative path>

Next:
- `open <n>`
- `open full <n>`
```

## Heuristic Map

Use this concept routing before deep search:

| Query hints | Likely stage | Likely artifact |
|-------------|--------------|-----------------|
| actor, goal, NFR, dependency | `01-discovery` | `{slug}-discovery.md` |
| flow, journey, scenario, use case | `01b-flow` | `{slug}-flows.md`, `{slug}-scenarios.md` |
| bounded context, domain term, context map | `01c-bounded-context` | `{slug}-bounded-contexts.md`, `{slug}-context-map.md` |
| entity, aggregate, relation, ER, storage | `01d-data-model` | `{slug}-domain-entities.md`, `{slug}-er-model.md`, `{slug}-storage-hints.md` |
| system context, external system | `02-context` | `{slug}-context.md` |
| container, service, contract, API, sequence L2 | `03-container` | `{slug}-containers.md`, `{slug}-contracts.md`, `{slug}-sequences-l2.md` |
| component, module, responsibility, code map, symbol, file path | `04-component` | `{slug}-components.md`, `{slug}-component-scope.md`, `{slug}-component-code-map.md` |
| final architecture doc | `05-document` | `{slug}-architecture.md` |
| SPEC, OpenAPI, proto, interface | `06-spec` | `SPEC.md`, `openapi.yaml`, `{slug}.proto`, `{slug}-interfaces.*` |
| validation finding | `07-spec-validation` | `{slug}-spec-validation.md` |
| BDD, unit, integration, e2e, coverage | `08-test-scaffold` | test scaffold outputs |
| impact, affected stages, pending change | `triage` | `triage/*-impact.md` |

## Rules

- registries remain authoritative for artifact ownership and routing
- `shared/artifact-manifest.ndjson`, `shared/artifact-index.json`, and `shared/triage-index.json` are lookup caches, not source of truth
- source-of-truth priority: stages `01–04` > `06-spec` > code map/triage support context
- default trace must stay ultra-cheap: manifest grep only, top 3, no broad multi-file reads on first pass
- `trace summary <n>` is detail step; `open <n>` is file step
- if manifest missing or empty, fail cheap and do not broad-grep workspace
- do not claim absence until manifest/registry path checked and relevant available index checked
- if no exact hit, return closest likely artifacts plus next search hint
- if many hits, group by stage and prefer canonical owner artifact over incidental mention
- if user wants richer summary, use `trace summary <n>` or open only selected result, not all candidates
- deep mode may search contents, but only with narrow canonical scope and hard limits
