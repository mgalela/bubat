# Stage 02: Context Diagram

Stage id: `02-context`

Purpose: build C4 Level 1 system context diagram and narrative.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#02-context`, `shared/output-catalog.md`, `shared/stage-gates.md`, and `shared/c4-notation.md`.

## Stage-Specific Rules

1. Load discovery and bounded-context outputs.
2. Read `stages/02-context/references/` and C4 notation rules.
3. Identify system boundary, people, external systems, and high-level relationships.
4. Use names exactly from upstream artifacts.
5. Keep Level 1 only: no containers, components, databases, classes, or internals.
6. Present element table before drawing.
7. Render diagram and narrative.

## Audit Focus

- one system boundary
- all people/external systems clearly typed
- relationships have direction and meaningful verbs
- diagram title present
- no Level 2/3 detail leaks

## Outputs

See `shared/output-catalog.md`:
- `{slug}-context.md`
