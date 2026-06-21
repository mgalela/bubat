---
name: bubat-status
description: Show BUBAT pipeline completion status using shared stage index and output catalog. Use when user types "status" in a BUBAT workspace.
---

# BUBAT Status

Use shared registries; do not hardcode artifact lists.

## Process

1. Read `shared/stage-index.md` for pipeline order.
2. Read `shared/output-catalog.md` for Completion Criteria and expected artifacts per owner stage.
3. Read `shared/system-meta.md` to infer `{slug}` if available.
4. For each stage in pipeline order:
   - Find expected outputs from Completion Criteria first; use Artifact Catalog as fallback.
   - Check `stages/<stage>/output/` for files beyond `.gitkeep`.
   - Prefer matching expected artifact names when `{slug}` is known.
   - Mark:
     - `COMPLETE` if required owner-stage outputs exist.
     - `PARTIAL` if some outputs exist but expected set incomplete.
     - `PENDING` if no real output files exist.
     - `BLOCKED` if upstream required stage is `PENDING`.
5. Also check:
   - `triage/*-impact.md` count
   - Stage 04 code map existence
   - Stage 06 `SPEC.md` existence
   - Stage 07 Blocking findings if validation report exists
6. Display concise status table.

## Output Format

```text
Pipeline Status: BUBAT

| Stage | Status | Outputs | Notes |
|-------|--------|---------|-------|
| 01-discovery | COMPLETE/PARTIAL/PENDING/BLOCKED | N/M | ... |
...
| 08-test-scaffold | COMPLETE/PARTIAL/PENDING/BLOCKED | N/M | ... |

Source-of-truth:
- triage reports: N
- component code map: present/missing
- SPEC.md: present/missing
- validation blocking findings: N/unknown
```

## Rules

- `.gitkeep` does not count.
- Template files in `output/` do not count as completed artifacts unless stage output explicitly allows templates.
- If `{slug}` unknown, count any non-template markdown/spec file in stage output and mark exactness as `unknown slug`.
- Stage `05-document` is optional for cavekit; do not block Stage 06 because Stage 05 is pending.
