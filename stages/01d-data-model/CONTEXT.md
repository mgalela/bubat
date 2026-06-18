# Stage 01d: Domain Data Model

Convert bounded context aggregates into a concrete entity-relationship model at the conceptual/logical level.
Output feeds container partitioning (Stage 03) and repository design (Stage 04).

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Bounded context inventory | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-bounded-contexts.md` | Full file | Aggregates and ubiquitous language are the source of entities |
| Context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-context-map.md` | Full file | Cross-BC relationships reveal cross-entity dependencies and shared data |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | Scenarios validate that the model can support all required operations |
| System identity | `../../shared/system-meta.md` | Full file | System name, slug, and diagram format |
| Entity guide | `references/data-model-guide.md` | Full file | Rules for extracting entities from aggregates |
| Entity format | `references/entity-format.md` | Full file | Format for attribute tables and ERD diagrams |

## Process

1. Read the BC inventory. For each BC, list its aggregates.
2. For each aggregate: identify its root entity, child entities, and value objects.
3. For each entity: list its key attributes (name, type, constraint). Distinguish identifiers, required fields, and optional fields.
4. For each value object: list its fields and note it has no independent identity.
5. Map relationships within each BC: entity-to-entity, with cardinality (1:1, 1:N, M:N) and direction.
6. Pause at checkpoint 1 -- confirm entity list, attributes, and intra-BC relationships before cross-BC mapping.
7. Read the context map. For each BC-to-BC relationship: identify what data crosses the boundary and in which direction.
8. Flag shared or replicated entities: entities that appear in multiple BCs with different shapes (projections).
9. Identify cross-cutting value objects: types used across BCs (e.g., Money, Address, DateRange).
10. Pause at checkpoint 2 -- confirm cross-BC data dependencies and shared types.
11. Validate against scenarios: for each key scenario, trace the data reads and writes. Flag any data that cannot be stored or retrieved with the current entity model.
12. Assign a storage hint to each aggregate: Relational, Document, Key-Value, Graph, or Time-Series.
13. Pause at checkpoint 3 -- confirm storage hints before rendering diagrams.
14. Render one ERD per BC using Mermaid `erDiagram`.
15. Write a short narrative per BC (one paragraph) explaining the entity structure and key design decisions.
16. Run audit checks.
17. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 5 | Table per BC: aggregate root, child entities, value objects, key attributes with types and constraints | Confirm, rename, split, or merge entities before cross-BC work begins |
| Step 10 | Cross-BC dependency table: data that crosses each boundary, direction, projection shape, shared value objects | Confirm cross-BC design before scenario validation |
| Step 12 | Storage hint table: aggregate, storage type, rationale, candidate technology | Confirm or override storage hints before diagrams are rendered |

## Audit

| Check | Pass Condition |
|-------|---------------|
| Every BC has entities | Each BC from Stage 01c maps to at least one entity |
| Every aggregate has a root | Aggregate root entity named and marked for each aggregate |
| All attributes have types | No attribute left without a type (String, Integer, DateTime, Boolean, UUID, Decimal, Enum, etc.) |
| All relationships have cardinality | Every entity-to-entity relationship has 1:1, 1:N, or M:N label |
| Scenarios satisfied | Every key scenario from 01b-flow can be traced through the entity model without missing data |
| No SQL syntax | Entity definitions use domain language and conceptual types, not DDL or column definitions |
| Cross-BC data explicit | Any data that crosses a BC boundary is named in the cross-BC dependency table |
| Projections named differently | Cross-BC projections have distinct names from their source entities |
| Storage hints assigned | Every aggregate has a storage hint with rationale |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Domain entity inventory | `output/{{SYSTEM_SLUG}}-domain-entities.md` | Attribute tables per aggregate + ERD diagrams per BC |
| Cross-BC data dependencies | `output/{{SYSTEM_SLUG}}-data-dependencies.md` | Cross-BC dependency table + shared value object list |
| Storage hints | `output/{{SYSTEM_SLUG}}-storage-hints.md` | Table: aggregate, storage type, rationale, candidate technology |
