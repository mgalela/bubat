# Stage 01b: User Flows & Business Processes

Capture and document business-level processes and key system scenarios before structural design begins.
These flows inform structural decisions in Stages 03-04 and become the source for sequence diagrams.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | "Users", "External Systems", "System Boundary" sections | Source of actors and system boundary |
| System identity | `../../shared/system-meta.md` | Full file | System name and diagram format |

## Stage Gate

Before running this stage, apply relevant checks from `../../shared/stage-gates.md`: input gate before work starts; stage audit, placeholder, and traceability gates before saving outputs.

## Process

1. Read the discovery report to identify all user roles, external systems, and the system boundary.
2. For each user role, identify their primary use cases (2-5 per role).
3. For each use case, map the business process step-by-step using swimlane or flowchart notation.
   - Stay at business level: no technology names, no container or component references.
   - Capture happy path and at least one failure or exception path per flow.
4. Pause at checkpoint 1 -- confirm use case list before drawing flows.
5. Select 3-7 key scenarios that warrant sequence diagrams in Stages 03-04.
   - Prioritise: highest-traffic paths, most complex flows, failure-critical paths, paths that cross multiple actors.
6. For each selected scenario: document trigger, actors, ordered steps, and failure cases.
7. Pause at checkpoint 2 -- confirm scenario list and detail before saving.
8. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 2 | Use case list per user role | Add, remove, or rename before flows are drawn |
| Step 5 | Selected scenario list with justification | Confirm or adjust which scenarios get sequence diagrams |

## Audit

| Check | Pass Condition |
|-------|---------------|
| All user roles covered | At least one flow per user role from discovery |
| Business-level only | No technology, container, or component names appear in flow diagrams |
| Failure paths captured | Each flow has at least one failure or exception path |
| Scenarios are distinct | No two scenarios cover the same path through the system |
| Scenario count | Between 3 and 7 scenarios selected |
| Scenarios traceable | Each scenario references user role(s) and flow(s) it was derived from |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Business flows | `output/{{SYSTEM_SLUG}}-flows.md` | Swimlane/flowchart diagrams + one-paragraph narrative per flow |
| Key scenarios | `output/{{SYSTEM_SLUG}}-scenarios.md` | Scenario table + detail block per scenario |
