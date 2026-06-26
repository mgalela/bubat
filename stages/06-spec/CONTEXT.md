# Stage 06: Cavekit SPEC.md Bridge + Interface Specs

Stage id: `06-spec`

Purpose: convert BUBAT architecture truth (`01–04`) into cavekit `SPEC.md`, interface specs, and extraction map with zero information loss.

## Run Protocol

Use `shared/stage-runbook.md`, `shared/stage-index.md#06-spec`, `shared/output-catalog.md`, `shared/stage-gates.md`, and `skills/bubat-bridge/SKILL.md`.

Existing project precision:
- if `project_path` targets live repo, use `@commands/cl/research_codebase.md` to inspect existing interfaces, API contracts, modules, task anchors, and implementation constraints before drafting outputs

## Stage-Specific References

- `references/caveman-encoding.md`
- `references/spec-template.md`
- `references/extraction-map-template.md`
- `references/invariant-extraction-rules.md`
- `references/task-generation-rules.md`
- `references/interface-gen-rules.md`
- `references/openapi-template.yaml`
- `references/proto-template.proto`
- `references/module-interface-patterns.md`

## Stage-Specific Rules

1. Load all available outputs from stages `01–04` directly. Do not use Stage 05 document.
2. Load `shared/system-meta.md` for system identity, tech stack, and interface format selection.
3. If present, load latest relevant `triage/*-impact.md` for affected files, planned files, and task focus.
4. Emit explicit `[MISSING — run stage XX first]` markers for missing upstream stage outputs; do not skip sections.
5. Build `SPEC.md` sections:
   - §G: purpose/goal
   - §C: constraints, NFRs, compliance, tech locks
   - §I: external surfaces, contracts, generated spec pointers
   - §R: research/decision findings
   - §V: testable invariants
   - §T: implementation tasks, including code map pointers where available
   - §B: empty bug table
6. Generate interface specs based on contracts and tech stack:
   - HTTP → `openapi.yaml`
   - gRPC → `{slug}.proto`
   - Go/TypeScript/Java/Kotlin → `{slug}-interfaces.*`
7. Generate `{slug}-extraction-map.md`; every §C and §V entry must trace to source excerpt.
8. Apply Bridge Gate G7 before saving.
9. Present SPEC/interface summary before writing outputs.

## Audit Focus

- no architecture information from `01–04` lost
- every §C and §V entry traced in extraction map
- generated interface specs match contracts
- code map and triage impact reflected in §T when available
- all TODO/missing items documented
- no unresolved `{{PLACEHOLDER}}`

## Outputs

See `shared/output-catalog.md`:
- `SPEC.md`
- `openapi.yaml`
- `{slug}.proto`
- `{slug}-interfaces.*`
- `{slug}-extraction-map.md`
