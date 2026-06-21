---
name: bubat-bridge
description: Run Stage 06 bridge to generate cavekit SPEC.md and interface specs. Use when user types "bridge".
---

# BUBAT Bridge

1. Read `shared/stage-runbook.md`, `shared/stage-index.md`, `shared/output-catalog.md`, and `shared/stage-gates.md`.
2. Run stage `06-spec` using `stages/06-spec/CONTEXT.md`.
3. Load all available `01–04` outputs directly. Do not use Stage 05 document as source.
4. Load latest relevant `triage/*-impact.md` if feature/change workflow is active.
5. Generate:
   - `stages/06-spec/output/SPEC.md`
   - `stages/06-spec/output/openapi.yaml` if HTTP contracts exist
   - `stages/06-spec/output/{slug}.proto` if gRPC contracts exist
   - `stages/06-spec/output/{slug}-interfaces.*` if language interfaces apply
   - `stages/06-spec/output/{slug}-extraction-map.md`
6. Apply Bridge Gate G7 before saving.
7. Report generated files and cavekit next commands.
