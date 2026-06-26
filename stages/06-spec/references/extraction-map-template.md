# Extraction Map Template

```markdown
# {{SYSTEM_SLUG}}-extraction-map.md

| SPEC Entry | Source Artifact | Source Section | Verbatim Excerpt (truncated) |
|------------|----------------|----------------|------------------------------|
| §G | system-meta.md | purpose | "{{excerpt}}" |
| §C.1 | {slug}-discovery.md | NFR / Availability | "{{excerpt}}" |
| §V.3 | {slug}-bounded-contexts.md | aggregate rule | "{{excerpt}}" |
| §I/openapi | {slug}-contracts.md | HTTP contract rows | "→ openapi.yaml paths" |
| §I/proto | {slug}-contracts.md | gRPC contract rows | "→ {slug}.proto services" |
| §I/interfaces | {slug}-components.md + sequences-l3 | component type tags | "→ {slug}-interfaces.{ext}" |
| §T/code-map | {slug}-component-code-map.md | affected component rows | "→ file:path#line-range" |
| §T/change-impact | triage/*-impact.md | Cavekit Handoff | "→ affected files + planned new files" |
```

Every §V and §C entry must have a row. §I and §T trace rows are strongly encouraged; required when generated from code map or triage impact.
