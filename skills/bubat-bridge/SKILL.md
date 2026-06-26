---
name: bubat-bridge
description: Run Stage 06 bridge to generate cavekit SPEC.md and interface specs. Use when user types "bridge".
---

# BUBAT Bridge

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

1. Read `${WORKSPACE_ROOT}/shared/stage-runbook.md`, `${WORKSPACE_ROOT}/shared/stage-index.md`, `${WORKSPACE_ROOT}/shared/output-catalog.md`, and `${WORKSPACE_ROOT}/shared/stage-gates.md`.
2. Run stage `06-spec` using `${WORKSPACE_ROOT}/stages/06-spec/CONTEXT.md`.
3. Load all available `01–04` outputs directly. Do not use Stage 05 document as source.
4. Load latest relevant `${WORKSPACE_ROOT}/triage/*-impact.md` if feature/change workflow is active.
5. Generate:
   - `${WORKSPACE_ROOT}/stages/06-spec/output/SPEC.md`
   - `${WORKSPACE_ROOT}/stages/06-spec/output/openapi.yaml` if HTTP contracts exist
   - `${WORKSPACE_ROOT}/stages/06-spec/output/{slug}.proto` if gRPC contracts exist
   - `${WORKSPACE_ROOT}/stages/06-spec/output/{slug}-interfaces.*` if language interfaces apply
   - `${WORKSPACE_ROOT}/stages/06-spec/output/{slug}-extraction-map.md`
6. Apply Bridge Gate G7 before saving.
7. Report generated files and cavekit next commands.
