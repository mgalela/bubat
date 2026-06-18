# C4 Level 1 Rules

## What Belongs at Level 1

- The software system being documented (one box, black box)
- Human users who interact directly with the system (Person elements)
- External software systems that send or receive data to/from the system

## What Does NOT Belong at Level 1

- Containers (databases, APIs, services) inside the system
- Internal components or modules
- Technology details (programming language, framework, database type)
- Network infrastructure (load balancers, CDN, VPCs)
- Third-party libraries or SDKs -- only external systems that the system calls or is called by

## Common Mistakes

**Too much detail.** Showing "PostgreSQL database" or "Redis cache" at Level 1 breaks the abstraction.
The system is a black box at this level. What it does inside is invisible.

**Missing users.** Every human role that interacts with the system must appear. If a system has no
human users (a pure backend service), that is worth noting but the diagram still shows who or what
calls it.

**Floating external systems.** Every external system shown must have at least one relationship arrow.
If an external system appears but has no drawn relationship, either add the relationship or remove the element.

**Bidirectional clutter.** If two systems truly exchange data in both directions, draw two arrows
(one each way) with distinct labels. Do not use a single bidirectional arrow with "integrates with" as the label.

## Narrative Section

After the diagram, write one paragraph (3-5 sentences) that:
1. Names the system and its primary job
2. Identifies the main user types and their relationship to the system
3. Names the key external dependencies and why the system depends on them

The narrative is for readers who find diagrams hard to parse. It must be fully redundant with the diagram
-- no new information, just prose translation.

## Relationship Label Rules

Labels answer the question: "What happens across this arrow?"
- Use active verbs: "submits", "retrieves", "authenticates via", "sends notification to"
- Include technology in brackets when it matters: "queries [GraphQL]", "streams events [Kafka]"
- Keep labels under 8 words
