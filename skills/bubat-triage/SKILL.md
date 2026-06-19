---
name: bubat-triage
description: Identify which BUBAT stage(s) a new idea belongs to and which downstream stages are affected. Use when user types "triage <idea>" in a BUBAT workspace.
---

# BUBAT Triage

Given the idea description from the user:

1. Map it to one or more **entry stages** using the signal table below. An idea may have multiple entry stages if it spans topics.
2. Determine **cascade stages**: all stages downstream of the highest entry stage in the pipeline order.
3. Check each cascade stage: if a stage's output artifact does not reference concepts touched by the idea, mark it as **likely unaffected** and exclude it from the minimum update set.
4. Present the triage report:

```
Triage: "<idea description>"

  Entry stage(s)   →  <stage-id>: <reason>
  Cascade stages   →  <stage-id>: AFFECTED / likely unaffected
  Safe (upstream)  →  <stage-ids>

  Minimum update:  update <stage-ids in pipeline order>
  Proceed? [y/n]
```

5. If user confirms (`y`), invoke skill `bubat-update` with the minimum update set automatically.
6. If user declines (`n`), leave all artifacts unchanged.

## Signal Table

| Idea signals                                                                              | Entry stage           |
| ----------------------------------------------------------------------------------------- | --------------------- |
| New/changed stakeholder, user role, actor, system goal, NFR, high-level requirement      | `01-discovery`        |
| New/changed business process, user journey, workflow, use case, scenario                 | `01b-flow`            |
| New/changed domain concept, bounded context, ubiquitous language term, context boundary  | `01c-bounded-context` |
| New/changed entity, aggregate, attribute, data relationship, storage type                | `01d-data-model`      |
| New/changed external system integration, system-level actor or dependency                | `02-context`          |
| New/changed service, database, message broker, deployment unit, infrastructure component | `03-container`        |
| New/changed API, internal module, component interaction, code-level design               | `04-component`        |

## Pipeline Order

```
01-discovery → 01b-flow → 01c-bounded-context → 01d-data-model → 02-context → 03-container → 04-component → 05-document → 06-spec
```

Cascade always includes `05-document` and `06-spec` when any stage 01–04-component is affected, because those stages aggregate all upstream content.
