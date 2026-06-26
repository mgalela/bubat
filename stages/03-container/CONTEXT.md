# Stage 03: Container Diagram

Stage id: `03-container`

Purpose: build C4 Level 2 container diagram, container inventory, inter-container contracts, and L2 sequences.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#03-container`, `shared/output-catalog.md`, `shared/stage-gates.md`, and `shared/c4-notation.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to inspect services, databases, queues, deployment units, contracts, and inter-service communication before drafting outputs

## Stage-Specific Rules

1. Load context diagram, data model, bounded context, and flow/scenario outputs.
2. Read `stages/03-container/references/`.
3. Identify deployable/runnable containers and data stores.
4. Map bounded contexts and entities to containers where relevant.
5. Define inter-container contracts: protocol, format, direction, endpoint/topic, auth, errors, SLA.
6. Render one C4 Level 2 diagram.
7. For each key scenario, render L2 sequence with container names exactly matching diagram.
8. Confirm container inventory, contracts, and sequences before saving.
9. Append non-obvious container/contract decisions to tech decisions log.

## Audit Focus

- containers are deployable/runnable units
- no components/classes in L2
- contracts cover every inter-container relationship
- sequences cover key scenarios
- names match upstream labels

## Outputs

See `shared/output-catalog.md`:
- `{slug}-containers.md`
- `{slug}-contracts.md`
- `{slug}-sequences-l2.md`
