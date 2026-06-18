# Stage 01c: Bounded Context Map

Identify domain language boundaries within the system and map relationships between bounded contexts
before structural design begins. Output feeds both the context diagram (Stage 02) and container
partitioning (Stage 03).

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Business flows | `../01b-flow/output/{{SYSTEM_SLUG}}-flows.md` | Full file | Primary source of domain language and domain events per functional area |
| Key scenarios | `../01b-flow/output/{{SYSTEM_SLUG}}-scenarios.md` | Full file | Scenarios reveal language shifts across actor boundaries |
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | "Users", "External Systems", "High-Level Structure" sections | External systems become external BCs; user roles anchor language |
| System identity | `../../shared/system-meta.md` | Full file | System name and diagram format |

## Stage Gate

Before running this stage, apply relevant checks from `../../shared/stage-gates.md`: input gate before work starts; stage audit, placeholder, and traceability gates before saving outputs.

## Process

1. Read all flows and scenarios. Extract every domain noun and verb that appears.
2. Group nouns and verbs by functional area: cluster terms that co-occur in the same flows.
3. Identify language shifts: find terms that appear in multiple areas with different meanings.
   These shifts mark candidate BC boundaries.
4. Name each candidate BC using domain language only -- no technology names.
5. For each BC: list its ubiquitous language (key terms), owned aggregates, and primary domain events.
6. Treat each external system from discovery as an external BC.
7. Pause at checkpoint 1 -- confirm BC list before mapping relationships.
8. For each BC pair (and each BC-to-external-BC pair) with a relationship in the flows: assign a
   context map relationship type (see `references/context-map-format.md`).
9. Flag relationships that require an Anti-Corruption Layer (ACL).
10. Pause at checkpoint 2 -- confirm context map before rendering diagram.
11. Render the BC map diagram.
12. Write a short narrative (one paragraph) explaining the BC breakdown and key relationship types.
13. Run audit checks.
14. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 6 | Table: BC name, ubiquitous language (top 5 terms), owned aggregates, primary domain events | Confirm, merge, or split BCs before relationships are mapped |
| Step 9 | Context map table: BC pair, relationship type, direction, ACL required | Confirm or correct relationship types before diagram is rendered |

## Audit

| Check | Pass Condition |
|-------|---------------|
| No technology names in BC definitions | BC names and ubiquitous language contain only domain terms |
| Every BC has owned aggregates | At least one aggregate listed per BC |
| Every external system mapped | Each external system from discovery appears as an external BC in the context map |
| Every flow covered | Each flow from 01b-flow traces to at least one BC |
| Every relationship has a type | No BC-to-BC relationship left without a context map type |
| ACL decisions explicit | Every upstream→downstream relationship states whether ACL is required and why |
| BC count reasonable | Between 2 and 8 BCs for most systems; more than 8 signals over-partitioning |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Bounded context inventory | `output/{{SYSTEM_SLUG}}-bounded-contexts.md` | BC table + ubiquitous language per BC + BC map diagram |
| Context map | `output/{{SYSTEM_SLUG}}-context-map.md` | Relationship table per BC pair + ACL decision notes |
