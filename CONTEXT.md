# BUBAT

Document software architecture through four levels of zoom using the C4 model.

## Task Routing

| Task Type                | Go To                                   | Description                                                                            |
| ------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------- |
| Gather system info       | `stages/01-discovery/CONTEXT.md`        | Interview stakeholders and parse existing docs                                         |
| Capture business flows   | `stages/01b-flow/CONTEXT.md`            | Map user journeys and select key scenarios for sequence diagrams                       |
| Map bounded contexts     | `stages/01c-bounded-context/CONTEXT.md` | Identify domain language boundaries and context relationships before structural design |
| Design domain data model | `stages/01d-data-model/CONTEXT.md`      | Convert BC aggregates into entity-relationship model; assign storage hints             |
| Build context diagram    | `stages/02-context/CONTEXT.md`          | C4 Level 1 -- system boundary and external actors                                      |
| Build container diagram  | `stages/03-container/CONTEXT.md`        | C4 Level 2 -- major deployable units                                                   |
| Build component diagrams | `stages/04-component/CONTEXT.md`        | C4 Level 3 -- internals of each container                                              |
| Assemble final document  | `stages/05-document/CONTEXT.md`         | Combine all levels into one architecture doc                                           |

## Shared Resources

| Resource          | Location                        | Contains                                               |
| ----------------- | ------------------------------- | ------------------------------------------------------ |
| System identity   | `shared/system-meta.md`         | System name, purpose, tech stack, team context         |
| C4 notation rules | `shared/c4-notation.md`         | Element definitions, naming conventions, diagram rules |
| Business flows    | `stages/01b-flow/output/`       | User journey flowcharts and key scenario definitions   |
| Domain data model | `stages/01d-data-model/output/` | Entity inventory, cross-BC dependencies, storage hints |
