---
name: bubat-trace
description: Locate architecture artifacts with cheap manifest grep first, optional detail summary second, optional file open last. Use for `where <term>`, `trace <term>`, `trace summary <n>`, `find artifact <term>`.
---

# BUBAT Trace

Resolve `WORKSPACE_ROOT` first:

- use `.` if `shared/stage-index.md` exists
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm workspace root

## Triggers

Accept:

- `where <term>`
- `trace <term>`
- `trace summary <n>`
- `find artifact <term>`
- `locate <term>`
- `trace deep <term>`

## Core Rule

Keep default trace cheap.

Priority:

1. grep `shared/artifact-manifest.ndjson`
2. read `shared/artifact-index.json` only for `trace summary <n>`
3. read artifact file only for `open <n>` / `open path <...>`
4. use deep search only for explicit `trace deep <term>`

If manifest missing or empty:

- do not broad-grep workspace
- use `shared/stage-index.md` and `shared/output-catalog.md` to return likely artifact paths
- recommend `refresh index`

## Process

### `trace <term>` / `where <term>`

- grep `shared/artifact-manifest.ndjson`
- rank by artifact/path/title/keyword match
- return top 3 only
- do not read detail index or artifact bodies

### `trace summary <n>`

- read `shared/artifact-index.json`
- look up selected result only
- return: stage, artifact, 1-sentence summary, up to 4 headings, path

### `open <n>` / `open path <...>`

- read selected artifact only
- prefer targeted excerpt first
- full file only if user asks `open full <n>` or `open full path <...>`

### `trace deep <term>`

- use only if user explicitly asks
- narrow search to likely canonical stage outputs
- max 3 files first
- no `docs/`, `references/`, `commands/`, or whole-workspace grep by default
- surface max 10 hits
- read max 2 excerpts, 60 lines each

## Heuristic Map

Use this concept routing before deep search:

| Query hints                                                    | Likely stage          | Likely artifact                                                                     |
| -------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------- |
| actor, goal, NFR, dependency                                   | `01-discovery`        | `{slug}-discovery.md`                                                               |
| flow, journey, scenario, use case                              | `01b-flow`            | `{slug}-flows.md`, `{slug}-scenarios.md`                                            |
| bounded context, domain term, context map                      | `01c-bounded-context` | `{slug}-bounded-contexts.md`, `{slug}-context-map.md`                               |
| entity, aggregate, relation, ER, storage                       | `01d-data-model`      | `{slug}-domain-entities.md`, `{slug}-er-model.md`, `{slug}-storage-hints.md`        |
| system context, external system                                | `02-context`          | `{slug}-context.md`                                                                 |
| container, service, contract, API, sequence L2                 | `03-container`        | `{slug}-containers.md`, `{slug}-contracts.md`, `{slug}-sequences-l2.md`             |
| component, module, responsibility, code map, symbol, file path | `04-component`        | `{slug}-components.md`, `{slug}-component-scope.md`, `{slug}-component-code-map.md` |
| final architecture doc                                         | `05-document`         | `{slug}-architecture.md`                                                            |
| SPEC, OpenAPI, proto, interface                                | `06-spec`             | `SPEC.md`, `openapi.yaml`, `{slug}.proto`, `{slug}-interfaces.*`                    |
| validation finding                                             | `07-spec-validation`  | `{slug}-spec-validation.md`                                                         |
| BDD, unit, integration, e2e, coverage                          | `08-test-scaffold`    | test scaffold outputs                                                               |
| impact, affected stages, pending change                        | `triage`              | `triage/*-impact.md`                                                                |

## Output

For `trace <term>`:

```text
Trace: <query>

Top matches
1. <artifact> — <stage>
   Title: <short title>
   Path: <workspace-relative path>
   Why: <match reason>

2. ...

Next:
- `trace summary 1`
- `open 1`
- `open full 1`
```

For `trace summary <n>`:

```text
Trace summary: <n>

<artifact> — <stage>
Summary: <1 sentence>
Headings:
- <heading>
- <heading>
Path: <workspace-relative path>

Next:
- `open <n>`
- `open full <n>`
```

## Rules

- `shared/artifact-manifest.ndjson`, `shared/artifact-index.json`, `shared/triage-index.json` = lookup cache, not source of truth
- source of truth priority: stages `01–04` > `06-spec` > triage/cache
- default trace = manifest grep only
- no broad workspace search in default mode
- if index stale/missing, fail cheap and recommend `refresh index`
