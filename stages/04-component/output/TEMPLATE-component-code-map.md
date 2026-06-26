# {{SYSTEM_NAME}} Component Code Map

Source: Stage 04 Component Diagrams
Purpose: map designed components to concrete implementation files.

| Container | Component | Type | File Path | Symbol | Line Span | Source Mode | Confidence | Notes |
|-----------|-----------|------|-----------|--------|-----------|-------------|------------|-------|
| [Container Name] | [Component Name] | [Controller/Service/Repository/Gateway/Worker/etc.] | `src/...` or `[MISSING — implementation not yet generated]` | `ClassName` / `functionName` / `[MISSING]` | `L10-L84` or `[MISSING]` | discovery / generated | high / medium / low / planned | [Mapping reason, ambiguity, TODO] |

## Notes

- One component may have multiple rows if implementation spans multiple files.
- `Component` names must match Stage 04 diagram labels exactly.
- Use repo-relative file paths when possible.
- If code not built yet, keep planned rows with missing markers.
- Refresh this file on `update 04` after codegen or code discovery.
