# BUBAT

Document software architecture through four levels of zoom using C4 model, then bridge outputs into cavekit `SPEC.md`.

## Task Routing

| Task Type | Go To | Description |
|-----------|-------|-------------|
| Gather system info | `stages/01-discovery/CONTEXT.md` | Interview stakeholders and parse existing docs |
| Capture business flows | `stages/01b-flow/CONTEXT.md` | Map user journeys and select key scenarios for sequence diagrams |
| Map bounded contexts | `stages/01c-bounded-context/CONTEXT.md` | Identify domain language boundaries and context relationships before structural design |
| Design domain data model | `stages/01d-data-model/CONTEXT.md` | Convert BC aggregates into entity-relationship model; assign storage hints |
| Build context diagram | `stages/02-context/CONTEXT.md` | C4 Level 1 -- system boundary and external actors |
| Build container diagram | `stages/03-container/CONTEXT.md` | C4 Level 2 -- major deployable units |
| Build component diagrams | `stages/04-component/CONTEXT.md` | C4 Level 3 -- internals of each container |
| Assemble final document | `stages/05-document/CONTEXT.md` | Combine all levels into one architecture doc |
| Generate cavekit spec | `stages/06-spec/CONTEXT.md` | Convert BUBAT outputs into `SPEC.md` |

## Triggers

| Keyword | Action |
|---------|--------|
| `setup` | Run onboarding, populate `shared/system-meta.md` |
| `raw route` | Route `raw/` files into stage manifest |
| `status` | Show completion for all stages |
| `bridge` | Run Stage 06 and generate cavekit `SPEC.md` |
| `diagram <stage>` | Re-render diagram blocks only |
| `update <stage(s)>` | Re-run stages and downstream dependencies |

## Shared Resources

| Resource | Location | Contains |
|----------|----------|----------|
| System identity | `shared/system-meta.md` | System name, purpose, tech stack, team context |
| C4 notation rules | `shared/c4-notation.md` | Element definitions, naming conventions, diagram rules |
| Stage gates | `shared/stage-gates.md` | Cross-stage quality gates and rerun policy |
| Raw manifest | `raw/MANIFEST.md` | File-to-stage routing table |
| Business flows | `stages/01b-flow/output/` | User journey flowcharts and key scenario definitions |
| Domain data model | `stages/01d-data-model/output/` | Entity inventory, cross-BC dependencies, storage hints |
