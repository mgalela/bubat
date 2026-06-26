# {{FEATURE_SLUG}} Change Impact

Date: {{DATE}}
Request: {{FEATURE_REQUEST}}

## Decision Summary

| Field | Value |
|-------|-------|
| Change class | business-feature / domain-change / data-change / contract-change / component-change / infra-change / bugfix-local / refactor-local |
| Entry stage(s) | {{STAGE_IDS}} |
| Minimum update | `update {{STAGE_IDS_IN_ORDER}}` |
| Bridge required | yes / no |
| Post-code refresh | `update 04` if code added/moved/changed |
| Confidence | high / medium / low |

## Impact Map

| Layer | Impacted Items | Source Artifact | Confidence | Notes |
|-------|----------------|-----------------|------------|-------|
| User flow | {{flows}} | `stages/01b-flow/output/...` | high/medium/low | |
| Scenario | {{scenarios}} | `stages/01b-flow/output/...` | high/medium/low | |
| Bounded context | {{bounded_contexts}} | `stages/01c-bounded-context/output/...` | high/medium/low | |
| Entity / aggregate | {{entities}} | `stages/01d-data-model/output/...` | high/medium/low | |
| Container | {{containers}} | `stages/03-container/output/...` | high/medium/low | |
| Contract | {{contracts}} | `stages/03-container/output/...` | high/medium/low | |
| Component | {{components}} | `stages/04-component/output/...` | high/medium/low | |
| Code map | {{file_paths_and_symbols}} | `stages/04-component/output/{{slug}}-component-code-map.md` | high/medium/low | |
| Test scaffold | {{tests}} | `stages/08-test-scaffold/output/...` | high/medium/low | |

## Stage Cascade

| Stage | Status | Reason |
|-------|--------|--------|
| 01-discovery | affected / likely unaffected / safe upstream | |
| 01b-flow | affected / likely unaffected / safe upstream | |
| 01c-bounded-context | affected / likely unaffected / safe upstream | |
| 01d-data-model | affected / likely unaffected / safe upstream | |
| 02-context | affected / likely unaffected / safe upstream | |
| 03-container | affected / likely unaffected / safe upstream | |
| 04-component | affected / likely unaffected / safe upstream | |
| 05-document | affected / likely unaffected / optional | |
| 06-spec | affected / likely unaffected | |
| 07-spec-validation | affected / likely unaffected | |
| 08-test-scaffold | affected / likely unaffected | |

## Cavekit Handoff

| Item | Value |
|------|-------|
| SPEC sections likely changed | §G / §C / §I / §R / §V / §T |
| Existing files to update | {{code_map_file_paths}} |
| New files likely needed | {{planned_files}} |
| Interface specs to regenerate | openapi.yaml / .proto / interfaces.* / none |
| Tests to scaffold/update | BDD / unit / integration / e2e / none |

## Open Questions

- {{question}}

## Recommended Commands

```bash
# architecture update
update {{STAGES}}

# bridge to cavekit
bridge

# after cavekit/code changes
update 04
bridge
```
