---
name: bubat-sync-index
description: Incrementally sync artifact lookup indexes after artifact write/update/delete. Use after stage outputs, triage artifacts, research docs, or bridge outputs change.
---

# BUBAT Sync Index

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Goal:
- keep trace indexes fresh after each saved artifact
- avoid full `refresh index` rebuild for small changes
- update only entries for changed paths

## When To Use

Run after successful confirmed write for:
- `stages/*/output/*`
- `triage/*-impact.md`
- `shared/research/*.md`
- Stage 06 outputs such as `SPEC.md`, `openapi.yaml`, `{slug}.proto`, `{slug}-interfaces.*`, `{slug}-extraction-map.md`

Do not run:
- before checkpoint confirmation
- for temp files
- for unchanged dry-run previews

## Inputs

Given one or more changed workspace-relative paths:
- read `${WORKSPACE_ROOT}/shared/output-catalog.md`
- read `${WORKSPACE_ROOT}/shared/stage-index.md` only if stage ownership/path routing unclear
- read current index files if present:
  - `${WORKSPACE_ROOT}/shared/artifact-manifest.ndjson`
  - `${WORKSPACE_ROOT}/shared/artifact-index.json`
  - `${WORKSPACE_ROOT}/shared/triage-index.json`
  - `${WORKSPACE_ROOT}/shared/research-index.json`

## Process

1. Normalize changed paths.
2. Classify each path:
   - `stage-output`
   - `triage`
   - `codebase-research`
   - unsupported -> skip with note
3. For each supported path:
   - if file exists, read only enough to refresh metadata:
     - title or first heading
     - first non-empty paragraph for summary
     - up to 4 headings for detail index
     - compact keywords
     - for research docs, frontmatter metadata plus compact `code_refs` and `artifacts`
   - if file no longer exists, remove matching entry from relevant index files
4. Update indexes incrementally:
   - `shared/artifact-manifest.ndjson`
     - one line per stage-output artifact
     - replace existing line for same path or append new line
   - `shared/artifact-index.json`
     - replace existing object for same path or append new object
   - `shared/triage-index.json`
     - replace existing object for same path or append new object
   - `shared/research-index.json`
     - replace existing object for same path or append new object
5. Preserve other entries unchanged.
6. Keep manifest tiny:
   - fields only `path`, `stage`, `artifact`, `title`, `keywords`
   - max 5 keywords
7. Keep detail indexes compact:
   - `summary` max 160 chars for artifacts/triage, max 200 chars for research
   - headings max 6 for stage outputs, max 4 for triage/research
   - keywords max 12 for stage outputs/research, max 8 for triage
   - research `code_refs` max 12, `artifacts` max 8
8. Sort touched index file after update:
   - stage-output entries by pipeline order then path
   - triage entries newest-first or path order if date unclear
   - research entries newest-first by frontmatter date or filename date
9. Report updated/removed/skipped paths.

## Output

```text
Index sync complete.
- updated: N
- removed: N
- skipped: N
- manifest: shared/artifact-manifest.ndjson
- artifact detail: shared/artifact-index.json
- triage detail: shared/triage-index.json
- research detail: shared/research-index.json
```

## Rule

Use `refresh index` only when:
- index drift suspected
- many artifacts changed at once
- index files missing/corrupt
- migrating old workspace to new index format
