# Stage 02: Context Diagram

Build the C4 Level 1 System Context diagram showing the system, its users, and external dependencies.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Discovery report | `../01-discovery/output/{{SYSTEM_SLUG}}-discovery.md` | Full file | Source of all elements |
| Bounded context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-bounded-contexts.md` | Full file | Confirms which external systems are upstream/downstream BCs |
| Context map | `../01c-bounded-context/output/{{SYSTEM_SLUG}}-context-map.md` | Full file | Informs relationship labels with context map type where relevant |
| Tech decisions log | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Full file | Carry forward decisions and append new ones |
| C4 notation rules | `../../shared/c4-notation.md` | "Element Definitions" and "Diagram Rules" sections | Element types and relationships |
| System identity | `../../shared/system-meta.md` | Full file | System name and diagram format preference |
| Level 1 rules | `references/level1-rules.md` | Full file | What belongs and does not belong at Level 1 |

## Process

1. Read the discovery report to extract: system name, all user roles, all external systems.
2. Read the context map to identify which external systems are upstream BCs requiring ACL.
3. Classify each element: Person, Internal Software System, or External Software System.
4. Draft the element list with labels and one-sentence descriptions.
5. Define relationships: who does what with whom, and in what direction.
   - For external systems identified as upstream BCs with ACL in the context map, annotate the
     relationship label with "[ACL]" to signal the translation boundary.
6. Pause at checkpoint -- confirm elements and relationships before drawing.
7. Render the diagram in the format from `shared/system-meta.md`.
8. Write a short narrative (one paragraph) explaining the diagram.
9. Run audit checks.
10. Append any architectural decisions made during this stage to the tech decisions log (e.g., boundary calls, element classification choices, external system inclusion/exclusion rationale).
11. Save to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 4 | List of all elements with type tags and all relationships | Add, remove, or reclassify before diagram is rendered |

## Audit

| Check | Pass Condition |
|-------|---------------|
| System boundary clear | The internal system is clearly distinguished from external systems |
| Every Person has a goal | Each user element has a one-sentence description of their purpose |
| Every external system has a direction | Each external system has at least one directed relationship |
| No containers visible | No technology-level detail (databases, APIs) appears in this diagram |
| Diagram has title and key | Title states the system name; key explains shape meanings |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Context diagram | `output/{{SYSTEM_SLUG}}-context.md` | Diagram code + narrative description |
| Tech decisions log (append) | `../01-discovery/output/{{SYSTEM_SLUG}}-tech-decisions.md` | Append new entries; do not overwrite existing |
