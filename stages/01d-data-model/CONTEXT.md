# Stage 01d: Data Model

Stage id: `01d-data-model`

Purpose: convert bounded context aggregates into entity model, relationships, cross-BC data dependencies, and storage hints.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#01d-data-model`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

## Stage-Specific Rules

1. Load bounded context and flow outputs.
2. Read `stages/01d-data-model/references/`.
3. Identify entities, aggregates, fields, identifiers, invariants, and relationships.
4. Distinguish ownership relationships from read/reference dependencies.
5. Assign storage hints from access pattern, consistency, query, and lifecycle needs.
6. Render ER model using configured diagram style.
7. Confirm entity inventory and relationship model before saving.
8. Cite BC/rule/scenario source for each entity or invariant.

## Audit Focus

- entities belong to bounded contexts
- required identifiers and relationships are clear
- cross-BC data dependencies are explicit
- storage hints include rationale
- ER labels match entity inventory

## Outputs

See `shared/output-catalog.md`:
- `{slug}-domain-entities.md`
- `{slug}-er-model.md`
- `{slug}-data-dependencies.md`
- `{slug}-storage-hints.md`
