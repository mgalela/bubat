# Stage 03: Container Diagram

Build the C4 Level 2 Container diagram showing the major deployable units inside the system and how they connect.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Context diagram | `../02-context/output/{{SYSTEM_SLUG}}-context.md` | Full file | System boundary and external systems already established |
| Bounded context inventory | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-bounded-contexts.md` | Full file | BCs become the primary partitioning unit for containers |
| Context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-context-map.md` | Full file | Relationship types inform interface contracts and ACL container placement |
| Domain entity inventory | `../01d-data-model/output/{{SYSTEM_SLUG}}-domain-entities.md` | Full file | Entity structure per BC informs data store type and partitioning |
| Storage hints | `../01d-data-model/output/{{SYSTEM_SLUG}}-storage-hints.md` | Full file | Storage type recommendations drive data store container selection |
| Cross-BC data dependencies | `../01d-data-model/output/{{SYSTEM_SLUG}}-data-dependencies.md` | Full file | Cross-BC projections inform which containers need their own data stores |
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | "High-Level Structure" and "Technology Choices" sections | Preview containers and tech choices from discovery |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | Scenarios that require container-level sequence diagrams |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | Carry forward decisions and append new ones |
| C4 notation rules | `../../shared/c4-notation.md` | "Element Definitions" and "Diagram Rules" sections | Container element rules |
| Level 2 rules | `references/level2-rules.md` | Full file | What belongs and does not belong at Level 2 |
| Container patterns | `references/container-patterns.md` | Full file | Common container topologies to reference |

## Process

1. Read the context diagram output to inherit the system boundary and external systems.
2. Read the discovery high-level structure and technology choices sections for preliminary container candidates.
3. Read the bounded context inventory. Map each internal BC to a container group:
   - Minimum one service container (API or worker) + one data store per BC.
   - BCs that share no data may share a data store only when team and operational constraints require it;
     document the decision in the tech decisions log.
4. For BCs with an ACL relationship in the context map: add an explicit ACL adapter container at the
   integration boundary. Label it "[BC Name] Adapter [technology]".
5. Identify containers: present the BC-derived container list to the user for confirmation or expansion.
6. For each container: determine its technology, responsibility, and relationships.
7. Define interface contracts for each inter-container relationship: protocol, data format, key fields,
   and context map relationship type (inherited from Stage 01c).
8. Pause at checkpoint 1 -- confirm the full container list and contracts before drawing.
9. Render the Level 2 diagram in the format from `shared/system-meta.md`.
10. Write a short narrative (one paragraph) explaining the container breakdown.
11. Run audit checks.
12. Append topology and technology decisions made during this stage to the tech decisions log.
13. For each scenario in `{slug}-scenarios.md`: render a container-level sequence diagram showing how containers collaborate to fulfil the scenario. Use container names exactly as labelled in the Level 2 diagram.
14. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 4 | ACL adapter containers derived from context map, with BC and relationship type | Confirm ACL placement before container list is finalised |
| Step 5 | Table: container name, technology, one-sentence responsibility, source BC, relationships | Confirm, merge, or split containers before diagram is drawn |
| Step 7 | Interface contracts table: container pair, protocol, format, key fields, context map type | Confirm or correct contracts before diagram is drawn |
| Step 13 | Draft sequence diagrams for each scenario | Confirm accuracy before saving |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Every BC has containers | Each bounded context from Stage 01c maps to at least one service container and one data store |
| ACL containers present where required | Every BC pair with ACL=Yes in the context map has an adapter container in the diagram |
| Every container is deployable | Each element could, in principle, run in its own process or host |
| Technology tagged | Every container has a [technology] tag in its label |
| External systems inherited | Same external systems from Level 1 appear where they connect |
| No internal components shown | No service classes, functions, or modules visible -- only containers |
| Data stores are containers | Databases, caches, queues, file stores appear as distinct container elements |
| Diagram has title and key | Title states "Container Diagram: [System Name]"; key explains shapes |
| Every inter-container relationship has a contract | Each relationship in the diagram has a corresponding entry in contracts artifact |
| Sequence diagrams cover all scenarios | One sequence diagram per scenario in `{slug}-scenarios.md` |
| Sequence actors match container labels | Container names in sequence diagrams match exactly the labels in the Level 2 diagram |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Container diagram | `output/{{SYSTEM_SLUG}}-containers.md` | Diagram code + narrative + container inventory table |
| Interface contracts | `output/{{SYSTEM_SLUG}}-contracts.md` | Table per container pair: protocol, format, key fields, error handling notes |
| Container sequences | `output/{{SYSTEM_SLUG}}-sequences-l2.md` | One sequence diagram + scenario header per scenario from `{slug}-scenarios.md` |
| Tech decisions log (append) | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Append new entries; do not overwrite existing |
