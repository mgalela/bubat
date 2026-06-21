# §T Task Generation Rules

Generate implementation tasks from architecture artifacts and optional triage impact.

## Sources

| Source | Task Use |
|--------|----------|
| container inventory | one task cluster per container |
| component diagrams/scope | subtasks per selected component |
| contracts | API/event/RPC implementation tasks |
| data model | schema/entity/repository tasks |
| sequences | orchestration and behavior tasks |
| code map | implementation pointer `file:path#line-range` |
| triage impact | prioritize affected components/files and new-file tasks |

## Rules

1. Use dependency order from container diagram.
2. Expand Level 3 containers into component subtasks.
3. Where code map exists, attach implementation pointer.
4. Where no code exists, mark planned/new file.
5. Keep task status `[ ]` unless evidence says complete.
6. Add tasks for generated OpenAPI/proto/interfaces when contracts require them.
7. Preserve traceability in extraction map.
