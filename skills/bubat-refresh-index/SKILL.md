---
name: bubat-refresh-index
description: Rebuild lightweight architecture artifact search index for cheap `where` / `trace` lookups. Use when user types `refresh index`, `rebuild index`, or asks to refresh architecture search map.
---

# BUBAT Refresh Index

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Goal:
- build ultra-cheap grep-friendly manifest at `${WORKSPACE_ROOT}/shared/artifact-manifest.ndjson`
- build detail indexes at `${WORKSPACE_ROOT}/shared/artifact-index.json` and `${WORKSPACE_ROOT}/shared/triage-index.json`
- keep default trace on manifest grep only
- keep core architecture detail index small and stable
- isolate volatile triage history into separate index
- avoid wide `trace` reads across many stage artifacts
- keep summaries short, stable, git-reviewable

## Inputs

Read first:
- `${WORKSPACE_ROOT}/shared/stage-index.md`
- `${WORKSPACE_ROOT}/shared/output-catalog.md`
- `${WORKSPACE_ROOT}/shared/system-meta.md` if present

Scan these paths for real artifacts:
- `${WORKSPACE_ROOT}/stages/*/output/` -> write to `artifact-manifest.ndjson` and `artifact-index.json`
- `${WORKSPACE_ROOT}/triage/` -> write to `triage-index.json`

Ignore:
- `.gitkeep`
- files starting with `TEMPLATE`
- reference docs, context docs, skill docs
- generated temp files

## Build Rules

For each artifact file found:

1. Infer metadata:
   - `path`
   - `stage`
   - `artifact`
   - `kind`: `stage-output` or `triage`
2. Derive `stage` from path or owner stage from `shared/output-catalog.md`.
3. Derive `artifact` from canonical filename where possible:
   - `*-flows.md` -> `flows`
   - `*-contracts.md` -> `contracts`
   - `*-component-code-map.md` -> `component-code-map`
   - `SPEC.md` -> `SPEC`
   - etc.
4. Read only enough to extract compact summary:
   - title or first heading
   - first non-empty paragraph under title/first heading
   - up to 5 headings total
5. Extract keywords from:
   - artifact name
   - stage concept
   - top headings
   - obvious domain terms repeated in headings/title
6. Keep entries compact:
   - manifest entry: `path`, `stage`, `artifact`, short `title`, max 5 `keywords`
   - detail entry `summary`: max 160 chars, 1 sentence
   - `headings`: max 6 for stage outputs, max 4 for triage
   - `keywords`: max 12 for stage outputs, max 8 for triage
   - no large excerpts
   - no full body text
7. Mark status:
   - `present` for real file
   - do not include missing expected artifacts in index
8. Sort entries by pipeline order, then path.
9. Split output:
   - stage outputs -> `shared/artifact-manifest.ndjson` and `shared/artifact-index.json`
   - triage docs -> `shared/triage-index.json`
10. Manifest format:
   - one JSON object per line
   - each line must be self-contained grep target
   - stable key order: `path`, `stage`, `artifact`, `title`, `keywords`
11. Triage index may be pruned for cost control:
   - keep newest entries first
   - if triage count large, keep latest 20 unless user asks full history index
12. Manifest must stay tiny:
   - no summaries
   - no headings
   - no triage entries
   - prefer stable canonical keywords over generated keyword floods

## Output Schema

Write `${WORKSPACE_ROOT}/shared/artifact-manifest.ndjson`:

```text
{"path":"stages/03-container/output/acme-contracts.md","stage":"03-container","artifact":"contracts","title":"Inter-container contracts","keywords":["contract","api","event","integration","container"]}
{"path":"stages/04-component/output/acme-components.md","stage":"04-component","artifact":"components","title":"Component inventory and responsibilities","keywords":["component","gateway","adapter","external","integration"]}
```

Write `${WORKSPACE_ROOT}/shared/artifact-index.json`:

```json
{
  "version": 1,
  "generatedAt": "YYYY-MM-DD",
  "artifacts": [
    {
      "path": "stages/03-container/output/acme-contracts.md",
      "stage": "03-container",
      "artifact": "contracts",
      "kind": "stage-output",
      "summary": "Inter-container APIs, events, and failure contracts.",
      "headings": ["HTTP APIs", "Events", "Failure Contracts"],
      "keywords": ["contract", "api", "event", "integration"]
    }
  ]
}
```

Write `${WORKSPACE_ROOT}/shared/triage-index.json`:

```json
{
  "version": 1,
  "generatedAt": "YYYY-MM-DD",
  "triage": [
    {
      "path": "triage/20260621-payment-retry-impact.md",
      "stage": "triage",
      "artifact": "impact",
      "kind": "triage",
      "summary": "Impact report for payment retry feature across flows, contracts, and components.",
      "headings": ["Change Class", "Affected Stages", "Minimum Update"],
      "keywords": ["payment", "retry", "impact", "update"]
    }
  ]
}
```

## Output Discipline

- overwrite whole `shared/artifact-manifest.ndjson`
- pretty-print JSON with stable key order for git diff for detail indexes
- overwrite whole `shared/artifact-index.json`
- overwrite whole `shared/triage-index.json`
- report count of indexed artifacts by stage
- if no stage outputs exist yet, write empty `shared/artifact-manifest.ndjson`
- if no stage outputs exist yet, write valid empty detail artifact index with empty `artifacts` array
- if no triage docs exist yet, write valid empty triage index with empty `triage` array

## After Build

Return concise result:

```text
Artifact indexes refreshed.
- manifest artifacts: N
- detail artifacts: N
- indexed triage docs: N
- paths:
  - shared/artifact-manifest.ndjson
  - shared/artifact-index.json
  - shared/triage-index.json

Use:
- where <term>
- trace <term>
- trace summary <n>
```
