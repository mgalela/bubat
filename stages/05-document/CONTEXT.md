# Stage 05: Architecture Document

Stage id: `05-document`

Purpose: assemble C4 levels, flows, contracts, decisions, and implementation trace into audience-ready architecture document. Optionally assemble a functional specification document (FSD) markdown for DOCX export.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#05-document`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to cross-check assembled narrative against current repo structure, interfaces, and implementation trace before drafting outputs

## Stage-Specific Rules

1. Load outputs from stages `01`, `01b`, `01c`, `01d`, `02`, `03`, and `04` as needed by requested document mode.
2. For architecture mode, read `references/doc-template.md`.
3. For FSD mode, read `tools/docx-generator/templates/fsd-template.md` (workspace-root relative; this tool directory is independent from stages). FSD means Functional Specification Document; never interpret FSD as file structure/design or code layout.
4. Calibrate depth to audience in `shared/system-meta.md`.
5. Architecture mode: assemble sections: overview, NFRs, user flows, context, containers, sequences, contracts, components, implementation trace, tech rationale, decisions, open questions, traceability.
6. FSD mode: assemble sections: cover metadata, document history, overview, scope, glossary, user roles, functional flows, use cases, screen/API/action behavior, field descriptions, validation/business rules, configuration, traceability, approvals. Use stage outputs as sources:
   - `01-discovery`: goals, users, NFR/business constraints, dependencies.
   - `01b-flow`: business process flows, scenarios, main/alternate paths.
   - `01c-bounded-context`: terms, domain rules, context boundaries.
   - `01d-data-model`: entities, fields, relationships, storage hints when relevant to field/data descriptions.
   - `03-container`: contracts/APIs, sequences, external integration behavior.
   - `04-component`: component/code-map trace only when needed for implementation trace; keep FSD user/business oriented.
7. Use Stage 04 code map for architecture implementation trace and optional FSD traceability `Code Map` column.
8. Do not use Stage 06 as input.
9. Present requested mode(s), outline, source coverage, and approximate section sizes before saving.

## Audit Focus

Architecture mode:
- Level 1 and 2 present; Level 3 included if produced
- flows, sequences, contracts, NFRs present
- decisions pulled from tech decisions log
- traceability links Flow → Scenario → BC → Container → Component → Contract → Code Map
- audience-appropriate depth
- no placeholders

FSD mode:
- each feature/use case traces to source flow/scenario and bounded context where available
- fields/data rules trace to data model or explicit source notes
- actions, validations, alternate paths, and integrations trace to scenarios/contracts/sequences
- unknown mockups/screens are marked `[MISSING — source not provided]`, not invented
- no unresolved `{{PLACEHOLDER}}`

## Outputs

See `shared/output-catalog.md`:
- `{slug}-architecture.md`
- `{slug}-fsd.md` (optional; generated when FSD mode requested)
