# Stage 05: Architecture Document

Stage id: `05-document`

Purpose: assemble C4 levels, flows, contracts, decisions, and implementation trace into audience-ready architecture document.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#05-document`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

## Stage-Specific Rules

1. Load outputs from stages `01`, `01b`, `02`, `03`, and `04`.
2. Read `references/doc-template.md`.
3. Calibrate depth to audience in `shared/system-meta.md`.
4. Assemble sections: overview, NFRs, user flows, context, containers, sequences, contracts, components, implementation trace, tech rationale, decisions, open questions, traceability.
5. Use Stage 04 code map for implementation trace and traceability `Code Map` column.
6. Do not use Stage 06 as input.
7. Present outline and approximate section sizes before saving.

## Audit Focus

- Level 1 and 2 present; Level 3 included if produced
- flows, sequences, contracts, NFRs present
- decisions pulled from tech decisions log
- traceability links Flow → Scenario → BC → Container → Component → Contract → Code Map
- audience-appropriate depth
- no placeholders

## Outputs

See `shared/output-catalog.md`:
- `{slug}-architecture.md`
