# Stage 05: Architecture Document

Assemble all C4 levels into one coherent architecture document for the target audience.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Context diagram | `../02-context/output/{{SYSTEM_SLUG}}-context.md` | Full file | Level 1 diagram and narrative |
| Container diagram | `../03-container/output/{{SYSTEM_SLUG}}-containers.md` | Full file | Level 2 diagram, narrative, inventory |
| Interface contracts | `../03-container/output/{{SYSTEM_SLUG}}-contracts.md` | Full file | Inter-container contracts for contracts section |
| Container sequences | `../03-container/output/{{SYSTEM_SLUG}}-sequences-l2.md` | Full file | Container-level sequence diagrams per scenario |
| Component diagrams | `../04-component/output/{{SYSTEM_SLUG}}-components.md` | Full file | Level 3 diagrams and narratives |
| Component scope | `../04-component/output/{{SYSTEM_SLUG}}-component-scope.md` | Full file | Which containers got Level 3 and why |
| Component sequences | `../04-component/output/{{SYSTEM_SLUG}}-sequences-l3.md` | Full file | Component-level sequence diagrams per scenario |
| Business flows | `../01b-flow/output/{{SYSTEM_SLUG}}-flows.md` | Full file | Business process flowcharts for user flows section |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | Scenario table for traceability |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | All accumulated decisions across all stages |
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | "Non-Functional Requirements" section | NFR content for NFR section |
| System identity | `../../shared/system-meta.md` | Full file | Title, audience, purpose |
| Doc template | `references/doc-template.md` | Full file | Document structure and writing rules |

## Process

1. Read all stage outputs and `shared/system-meta.md`.
2. Identify the audience from `system-meta.md` and calibrate explanation depth accordingly.
3. Draft the document title page and introduction section.
4. Assemble Non-Functional Requirements section from discovery NFR table.
5. Assemble User Flows section: include flowchart diagrams and one-paragraph narrative per flow from `{slug}-flows.md`.
6. Assemble Level 1 section: context diagram + narrative + user and external system table.
7. Assemble Level 2 section: container diagram + narrative + container inventory table.
8. Assemble Key Scenario Sequences section: include container-level sequence diagrams from `{slug}-sequences-l2.md`, one per scenario.
9. Assemble Interface Contracts section from the contracts artifact.
10. Assemble Level 3 sections (one per component diagram, if any). Include pattern declaration per container. Embed component-level sequence diagrams from `{slug}-sequences-l3.md` for each container.
11. Write the "Tech Stack Rationale" section from technology choices in the tech decisions log.
12. Write the "Key Architectural Decisions" section: draw from the full tech decisions log, select 5-10 most significant decisions with rationale and tradeoffs.
13. Write the "Open Questions" section from any unresolved items in the discovery report.
14. Pause at checkpoint -- review structure before finalization.
15. Run audit checks.
16. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 13 | Outline of all sections with word counts | Add, remove, or reorder sections; flag any missing context |

## Audit

| Check | Pass Condition |
|-------|---------------|
| All structural diagrams present | At least Levels 1 and 2 included; Level 3 if component diagrams were produced |
| User flows present | At least one business flow per user role from Stage 01b |
| Sequence diagrams present | One container-level sequence per scenario; component-level where containers have Level 3 |
| NFR section present | Non-Functional Requirements section has at least availability, scale, and security rows |
| Contracts section present | At least one contract entry per inter-container relationship in Level 2 diagram |
| Tech stack rationale present | Every technology in system-meta.md has a stated reason in the Tech Stack Rationale section |
| Audience-appropriate | Technical depth matches audience defined in system-meta.md |
| No orphaned diagrams | Every diagram has an explanatory narrative immediately following it |
| Decisions documented | At least 5 architectural decisions with rationale and tradeoffs drawn from tech-decisions log |
| No placeholders remain | No {{PLACEHOLDER}} strings in the final document |
| Document is scannable | Section headings form a readable outline on their own |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Architecture document | `output/{{SYSTEM_SLUG}}-architecture.md` | Single Markdown file, complete and self-contained |
