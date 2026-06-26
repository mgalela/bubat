# Stage 01: Discovery

Stage id: `01-discovery`

Purpose: gather system boundary, users, external dependencies, NFRs, tech stack rationale, and initial ADR log.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#01-discovery`, `shared/output-catalog.md`, and `shared/stage-gates.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to inspect goals, actors, integrations, NFR signals, runtime boundaries, and supporting docs/code before drafting outputs

## Stage-Specific Rules

1. Read `shared/system-meta.md`.
2. Check `raw/MANIFEST.md` for rows containing `01-discovery`.
3. If `project_path` is set and `<project_path>/graphify-out/GRAPH_REPORT.md` + `graph.json` exist, read `references/graphify-guide.md` and use graphify as pre-fill source.
4. Read `references/discovery-guide.md` and ask only for missing topics.
5. Present pre-fill summary and gaps before interviewing.
6. Confirm each topic before saving.
7. Every extracted fact from raw/graphify must cite source.
8. Seed tech decisions log using `references/adr-template.md`.

## Audit Focus

- boundary clear
- users identified
- external dependencies listed
- NFRs captured or explicitly unknown
- tech stack rationale written
- no unresolved placeholders

## Outputs

See `shared/output-catalog.md`:
- `{slug}-discovery.md`
- `{slug}-tech-decisions.md`
