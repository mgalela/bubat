---
name: bubat-graphify-sync
description: Sync completed BUBAT stage outputs back into project graphify graph. Use when user types "sync graphify".
---

# BUBAT Graphify Sync

## Prerequisites

- `project_path` set in `shared/system-meta.md`
- `<project_path>/graphify-out/graph.json` exists
- at least one `stages/*/output/*.md` exists

## Process

1. Read `shared/system-meta.md` and get `project_path`.
   - If missing or `Not provided`, stop: `Set project_path first by running setup.`
2. Check `<project_path>/graphify-out/graph.json`.
   - If missing, stop: `Run graphify <project_path> first to initialize project graph.`
3. Collect BUBAT output files:
   - `stages/01-discovery/output/*.md`
   - `stages/01b-flow/output/*.md`
   - `stages/01c-bounded-context/output/*.md`
   - `stages/01d-data-model/output/*.md`
   - `stages/02-context/output/*.md`
   - `stages/03-container/output/*.md`
   - `stages/04-component/output/*.md`
   - `stages/05-document/output/*.md`
   - `triage/*-impact.md`
4. Present count and destination:
   `Found N BUBAT files across X sources. Copy to <project_path>/docs/architecture/bubat/ and run graphify update. Proceed?`
5. On confirmation:

```bash
mkdir -p <project_path>/docs/architecture/bubat
cp stages/01-discovery/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/01b-flow/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/01c-bounded-context/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/01d-data-model/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/02-context/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/03-container/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/04-component/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp stages/05-document/output/*.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
cp triage/*-impact.md <project_path>/docs/architecture/bubat/ 2>/dev/null || true
```

6. Run:

```bash
graphify <project_path> --update
```

7. Report:
   - files copied
   - graphify update status
   - notable new communities/connections if graphify report exposes them

## What Graphify Gains

| BUBAT output | Extraction value |
|---|---|
| Discovery | purpose, roles, dependencies |
| Flows | flow names, step sequences |
| BC map | domain boundaries, context edges |
| Data model | entities, relationships |
| Diagrams | inferred architecture edges |
| Code map | architecture component ↔ code file links |
| Triage impact | feature intent ↔ affected code/design links |
| ADR log | decision rationale edges |
