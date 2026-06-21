# Stage 04: Component Diagrams

Stage id: `04-component`

Purpose: build C4 Level 3 component diagrams, component scope, component-level sequences, and component code map.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#04-component`, `shared/output-catalog.md`, `shared/stage-gates.md`, and `shared/c4-notation.md`.

## Stage-Specific Rules

1. Load Stage 03 outputs, discovery tech decisions, and system metadata.
2. Read `references/level3-rules.md`, `references/component-patterns.md`, and `references/component-code-map-template.md`.
3. Ask which containers need Level 3 deep-dive; not all containers need one.
4. For each selected container, choose implementation pattern: Layered / CQRS / Hexagonal / Feature Modules / Pipeline Worker / other.
5. Identify components, responsibilities, type tags, relationships, and architecturally significant GoF patterns.
6. Parse existing code/API docs when available to extract component candidates.
7. Build/refresh code map:
   - `discovery` mode: inspect existing code under `project_path`.
   - `generated` mode: after codegen, rerun/update Stage 04 and map generated files.
8. Confirm pattern, component list, GoF patterns, and code map rows before drawing.
9. Render one L3 diagram per selected container.
10. Render L3 sequences for scenarios touching selected containers.
11. Append triggered pattern/GoF ADRs to tech decisions log.

## Audit Focus

- each diagram stays inside one container
- components have type tags
- no internals of other containers
- relationships use component-level verbs
- GoF patterns noted in narrative
- sequences match diagram labels
- code map has row or explicit missing marker for every selected component

## Outputs

See `shared/output-catalog.md`:
- `{slug}-components.md`
- `{slug}-component-scope.md`
- `{slug}-sequences-l3.md`
- `{slug}-component-code-map.md`
