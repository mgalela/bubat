---
name: bubat-r-feed-bubat
description: Deterministically feed BUBAT-R reconstruction outputs into BUBAT raw/SOURCES.md and raw/MANIFEST.md. Use when user types `bubat-r feed bubat [path]` or asks to map reconstruction outputs into BUBAT.
---

# BUBAT-R Feed BUBAT

Create/update deterministic BUBAT raw manifest entries for a BUBAT-R reconstruction folder.

## Resolve Workspace Root

Use `WORKSPACE_ROOT`:
- `.` if `shared/stage-index.md` exists in current directory
- else `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

## Resolve Reconstruction Path

Input command:

```text
bubat-r feed bubat [target-path]
```

Resolve reconstruction folder in order:
1. `[target-path]` if provided
2. `reconstruction/` from current directory
3. `${WORKSPACE_ROOT}/reconstruction/`
4. if `WORKSPACE_ROOT` is `.bubat`, sibling project root `reconstruction/`

Path must be directory. Prefer relative path from current/project root in manifest rows.

## Required Files

Warn if missing; do not fail unless all three primary files missing:

- `02-coverage-ledger.md`
- `11-reference-design.md`
- `12-drift-ambiguity-report.md`

## Update raw/SOURCES.md

Create `${WORKSPACE_ROOT}/raw/SOURCES.md` if missing.
Add or update one row:

```md
| <reconstruction-path>/ | dir | yes | BUBAT-R reconstruction outputs |
```

Do not duplicate existing path row.

## Update raw/MANIFEST.md

Create `${WORKSPACE_ROOT}/raw/MANIFEST.md` if missing.
Preserve existing non-BUBAT-R rows.
Replace any existing block with same source path:

```md
<!-- BEGIN BUBAT-R: <reconstruction-path> -->
...
<!-- END BUBAT-R: <reconstruction-path> -->
```

If no block exists, append block after table header or at file end.

Use exact rows below for files that exist. If optional file missing, omit row and report missing.

| File | Stages | Notes |
| ---- | ------ | ----- |
| `<reconstruction-path>/01-evidence-catalog.md` | `01-discovery, 04-component` | BUBAT-R evidence/source catalog; code and artifact references |
| `<reconstruction-path>/02-coverage-ledger.md` | `01-discovery, 01b-flow, 01c-bounded-context, 01d-data-model, 02-context, 03-container, 04-component` | BUBAT-R coverage and confidence ledger; primary input |
| `<reconstruction-path>/03-main-spine.md` | `02-context, 03-container, 04-component` | Main execution spine, entrypoints, runtime path |
| `<reconstruction-path>/04-runtime-map.md` | `02-context, 03-container` | Runtime topology, deploy units, infrastructure |
| `<reconstruction-path>/05-behavior-spine.md` | `01b-flow, 03-container, 04-component` | User/business behavior and scenario spine |
| `<reconstruction-path>/06-ownership-map.md` | `01c-bounded-context, 03-container, 04-component` | Ownership boundaries, services, modules |
| `<reconstruction-path>/07-domain-map.md` | `01c-bounded-context, 01d-data-model` | Domain terms, aggregates, entities |
| `<reconstruction-path>/08-contract-map.md` | `03-container, 04-component, 06-spec` | APIs, events, integration contracts |
| `<reconstruction-path>/09-component-map.md` | `04-component` | Internal components/modules |
| `<reconstruction-path>/10-code-trace-map.md` | `04-component` | Component to file/symbol/line trace |
| `<reconstruction-path>/11-reference-design.md` | `01-discovery, 01b-flow, 01c-bounded-context, 01d-data-model, 02-context, 03-container, 04-component, 05-document` | BUBAT-R reconstructed reference design; primary input |
| `<reconstruction-path>/12-drift-ambiguity-report.md` | `01-discovery, 02-context, 03-container, 04-component` | Drift, ambiguity, unknowns; primary input |
| `<reconstruction-path>/13-readiness-verdict.md` | `01-discovery, 05-document` | Takeover/change readiness verdict |

For `gaps/*.md`, add row per file:

```md
| <reconstruction-path>/gaps/<file>.md | 01-discovery, 02-context, 03-container, 04-component | BUBAT-R deep gap evidence for specific risk/unknown |
```

For `docs-feed/*.md`, add row per file:

```md
| <reconstruction-path>/docs-feed/<file>.md | 01-discovery, 02-context, 03-container, 04-component | BUBAT-R verified late/stale document feed |
```

## Report

After save, report:
- source path registered
- manifest block updated
- missing expected files
- next step: `stage 01`, then continue through `stage 04`
