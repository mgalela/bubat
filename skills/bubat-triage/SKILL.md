---
name: bubat-triage
description: Map feature/change request to affected BUBAT stages, architecture artifacts, code map rows, and cavekit handoff. Use when user types "triage <idea>" in a BUBAT workspace.
---

# BUBAT Triage

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Given the idea description from the user:

1. Load source-of-truth rules from `${WORKSPACE_ROOT}/shared/architecture-source-of-truth.md`.
2. Load architecture artifacts if present:
   - `${WORKSPACE_ROOT}/stages/01-discovery/output/*.md`
   - `${WORKSPACE_ROOT}/stages/01b-flow/output/*.md`
   - `${WORKSPACE_ROOT}/stages/01c-bounded-context/output/*.md`
   - `${WORKSPACE_ROOT}/stages/01d-data-model/output/*.md`
   - `${WORKSPACE_ROOT}/stages/02-context/output/*.md`
   - `${WORKSPACE_ROOT}/stages/03-container/output/*.md`
   - `${WORKSPACE_ROOT}/stages/04-component/output/*.md`
   - especially `${WORKSPACE_ROOT}/stages/04-component/output/*-component-code-map.md`
3. Classify request into one **change class** using Change Class table below.
4. Map it to one or more **entry stages** using Signal Table below. An idea may have multiple entry stages if it spans topics.
5. Determine **cascade stages**: all stages downstream of earliest affected stage in pipeline order.
6. Check each cascade stage: if stage output artifact does not reference concepts touched by request, mark it **likely unaffected** and exclude it from minimum update set.
7. Build impact map:
   - affected user flows and scenarios
   - affected bounded contexts and domain terms
   - affected entities/aggregates
   - affected containers
   - affected contracts
   - affected components
   - affected code map rows (`file path`, `symbol`, `line span`, confidence)
   - likely new files if no existing code map row fits
8. Determine cavekit handoff:
   - SPEC sections likely changed (`§G`, `§C`, `§I`, `§R`, `§V`, `§T`)
   - existing files to update from code map
   - new files likely needed
   - interface specs to regenerate
   - tests to scaffold/update
9. Write triage artifact from `change-impact-template.md` to:
   `${WORKSPACE_ROOT}/triage/{{YYYYMMDD}}-{{feature-slug}}-impact.md`
10. Present the triage report:

```
Triage: "<idea description>"

  Change class     →  <class>
  Entry stage(s)   →  <stage-id>: <reason>
  Cascade stages   →  <stage-id>: AFFECTED / likely unaffected
  Impacted code    →  <file path#lines or [new file needed]>
  Cavekit handoff  →  SPEC sections + files/contracts/tests
  Impact artifact  →  ${WORKSPACE_ROOT}/triage/<date>-<feature>-impact.md

  Minimum update:  update <stage-ids in pipeline order>
  Then:            bridge
  After code:      update 04 && bridge
  Proceed? [y/n]
```

11. If user confirms (`y`), invoke skill `bubat-update` with minimum update set automatically.
12. If user declines (`n`), leave stage artifacts unchanged but keep triage impact artifact unless user asks to delete it.

## Change Class Table

| Change class | Signals | Typical entry stage | Cavekit/code-map implication |
|--------------|---------|---------------------|------------------------------|
| `business-feature` | New user-visible capability, new path in workflow | `01b-flow` | New/changed scenarios; likely §V/§T changes |
| `domain-change` | New domain concept, rule, bounded context, term | `01c-bounded-context` | Domain invariants and component responsibilities shift |
| `data-change` | New/changed entity, aggregate, field, relation, storage | `01d-data-model` | Update schema/data tasks and related components |
| `contract-change` | New/changed API, event, RPC, external integration | `03-container` | Regenerate OpenAPI/proto/interfaces; update contract code |
| `component-change` | Internal module/responsibility/interaction change | `04-component` | Update component diagram, sequences, code map |
| `infra-change` | Deployment unit, database, broker, cache, runtime platform | `03-container` | Update container tasks and infra code pointers |
| `bugfix-local` | Behavior fix with no architecture responsibility change | `04-component` or none | Use code map to locate file; refresh only if path/symbol changes |
| `refactor-local` | Move/rename/split code without behavior/domain change | `04-component` | Refresh code map; bridge only if §T pointers changed |

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
01-discovery → 01b-flow → 01c-bounded-context → 01d-data-model → 02-context → 03-container → 04-component → 05-document → 06-spec → 07-spec-validation → 08-test-scaffold
```

Cascade always includes `06-spec` when any stage 01–04-component is affected because cavekit consumes Stage 06 output. `05-document` is optional for stakeholder docs but should be marked affected when architecture narrative changes.

## Source-of-Truth Rule

Architecture-significant feature requests must update BUBAT stages before cavekit/code implementation. After implementation, run `update 04` to refresh `${WORKSPACE_ROOT}/stages/04-component/output/*-component-code-map.md`; then run `bridge` again if SPEC task pointers changed.
