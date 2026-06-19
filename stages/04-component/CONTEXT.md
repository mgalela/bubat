# Stage 04: Component Diagrams

Build C4 Level 3 Component diagrams for each container selected for deep-dive.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Container diagram | `../03-container/output/{{SYSTEM_SLUG}}-containers.md` | Full file | Container inventory and relationships to inherit |
| Interface contracts | `../03-container/output/{{SYSTEM_SLUG}}-contracts.md` | Full file | Contracts that internal components must honour |
| Container sequences | `../03-container/output/{{SYSTEM_SLUG}}-sequences-l2.md` | Full file | Which scenarios touch which containers -- determines where L3 sequences are needed |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | Carry forward decisions and append new ones |
| C4 notation rules | `../../shared/c4-notation.md` | "Element Definitions" and "Diagram Rules" sections | Component element rules |
| Level 3 rules | `references/level3-rules.md` | Full file | What belongs and does not belong at Level 3 |
| Component patterns | `references/component-patterns.md` | Full file | Common component structures to reference |

## Stage Gate

Before running this stage, apply relevant checks from `../../shared/stage-gates.md`: input gate before work starts; stage audit, placeholder, and traceability gates before saving outputs.

## Process

1. Read the container diagram output to identify all containers.
2. Ask the user: which containers warrant a Level 3 diagram? (Not all containers need one -- focus on complex ones.) Record the decision and rationale.
3. For each selected container: declare the implementation pattern (Layered / CQRS / Hexagonal / Feature Modules / Pipeline Worker / other) and state why. Cross-check Stage 01 Pattern Signals using `references/component-patterns.md` Step 0 before deciding.
4. For each selected container: identify its components, their responsibilities, and their relationships.
4b. For each selected container: identify architecturally significant GoF patterns using `references/component-patterns.md` GoF section. Record which GoF patterns apply to which components. Note them in the narrative — do not add them to the C4 diagram.
5. If the user has existing code or API docs, parse them to extract component candidates.
6. Pause at checkpoint per container -- confirm pattern choice, components, and GoF patterns before drawing.
7. Render one Level 3 diagram per selected container.
8. Write a one-paragraph narrative per diagram. Include: implementation pattern chosen, rationale, and GoF patterns applied to key components.
9. Run audit checks for each diagram.
10. Append pattern decisions and container scope decisions to the tech decisions log. Include ADRs for GoF patterns that meet the trigger criteria in `references/component-patterns.md`.
11. For each scenario in the container sequences (L2) that involves a selected container: render a component-level sequence diagram showing how components inside that container handle their part of the scenario. Use component names exactly as labelled in the Level 3 diagram.
12. Save all diagrams, scope artifact, and component sequences to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 2 | Table: container name, Level 3 yes/no, reason | Confirm scope before any component work begins |
| Step 3 (per container) | Pattern choice + one-sentence rationale, cross-checked against Stage 01 Pattern Signals | Confirm or change pattern before component identification |
| Step 4 (per container) | Component list: name, type, one-sentence responsibility | Confirm, rename, split, or merge before diagram is drawn |
| Step 4b (per container) | GoF patterns table: component, GoF pattern, reason | Confirm or drop GoF calls before narrative is written |
| Step 11 | Draft component-level sequence diagrams per scenario | Confirm accuracy before saving |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Components are inside one container | Each diagram stays within a single container boundary |
| Component types labelled | Each component has a type tag: [Controller], [Service], [Repository], [Gateway], etc. |
| No cross-container components | Components do not reference internals of other containers -- only their interfaces |
| Relationships use component-level verbs | "calls", "delegates to", "queries via" rather than "uses" |
| External systems shown where connected | If a component calls an external system, that external system appears |
| Diagram has title | Title states "Component Diagram: [Container Name]" |
| Pattern declared | Each selected container has an explicit pattern entry in component-scope artifact |
| GoF patterns noted in narrative | Each diagram narrative mentions GoF patterns applied to key components (or explicitly states none were identified) |
| GoF ADRs written where triggered | ADRs written for GoF patterns that meet trigger criteria in `references/component-patterns.md` |
| Component sequences cover relevant scenarios | Every scenario that touches a selected container has a component-level sequence diagram |
| Component sequence actors match diagram labels | Component names in sequences match exactly the labels in the Level 3 diagram |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Component diagrams | `output/{{SYSTEM_SLUG}}-components.md` | One diagram + narrative per selected container, all in one file |
| Component scope | `output/{{SYSTEM_SLUG}}-component-scope.md` | Table: container, Level 3 yes/no, pattern, rationale |
| Component sequences | `output/{{SYSTEM_SLUG}}-sequences-l3.md` | Component-level sequence diagrams per scenario per selected container |
| Tech decisions log (append) | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Append new entries; do not overwrite existing |
