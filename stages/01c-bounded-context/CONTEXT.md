# Stage 01c: Bounded Context

Stage id: `01c-bounded-context`

Purpose: identify bounded contexts, ubiquitous language, domain rules, and context relationships.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#01c-bounded-context`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to inspect domain terms, modules, ownership boundaries, integration seams, and language used in code/docs before drafting outputs

## Stage-Specific Rules

1. Load discovery and flow outputs.
2. Read `stages/01c-bounded-context/references/`.
3. Extract domain terms, business capabilities, aggregate candidates, ownership boundaries, and context relationships.
4. Map upstream/downstream relationships and integration patterns.
5. Preserve ubiquitous language exactly where possible.
6. Confirm BC list and context map before saving.
7. Cite source flow/scenario/discovery artifact for each major boundary decision.

## Audit Focus

- bounded contexts have clear responsibility and language
- context relationships are directional
- domain rules are stated as testable rules where possible
- no container/deployment concerns mixed into BC definition

## Outputs

See `shared/output-catalog.md`:
- `{slug}-bounded-contexts.md`
- `{slug}-context-map.md`
