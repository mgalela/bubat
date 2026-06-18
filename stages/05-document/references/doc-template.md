# Architecture Document Template

Structure and writing rules for the final assembled document.

## Document Structure

```
# [System Name] Architecture

> One-sentence description of the system.
> Audience: [who this is for]. Last updated: [date].

---

## 1. System Overview

[2-3 paragraph introduction covering: what the system does, who uses it,
and the key architectural approach. Written for the target audience.]

---

## 2. Non-Functional Requirements

| Attribute | Requirement | Notes |
|-----------|-------------|-------|
| Availability | ... | ... |
| Latency | ... | ... |
| Scale | ... | ... |
| Security | ... | ... |
| Compliance | ... | ... |
| DR / RTO / RPO | ... | ... |

[Source: discovery report NFR section. Mark unknown attributes as "Not yet defined".]

---

## 3. User Flows & Business Processes

[One subsection per user role. Each subsection contains a flowchart and one-paragraph narrative.
Source: Stage 01b flows artifact. Stay business-level -- no container or technology names here.]

### 3.1 [User Role Name]

[Flowchart diagram]

[One-paragraph narrative: what the user is trying to accomplish, what happens on the happy path,
and what the main failure cases are.]

[Repeat 3.2, 3.3, etc. for each user role.]

---

## 4. System Context (C4 Level 1)

[Level 1 diagram]

### Users

| Role | Description | Primary Goal |
|------|-------------|--------------|

### External Dependencies

| System | Direction | What is Exchanged |
|--------|-----------|-------------------|

[1-paragraph narrative from Stage 02 output]

---

## 5. Containers (C4 Level 2)

[Level 2 diagram]

### Container Inventory

| Container | Technology | Responsibility |
|-----------|-----------|----------------|

[1-paragraph narrative from Stage 03 output]

---

## 6. Key Scenario Sequences

[One subsection per scenario from Stage 01b scenarios artifact.
Shows how containers collaborate at runtime to fulfil each scenario.
Source: Stage 03 sequences-l2 artifact.]

### Scenario: [Scenario Name] (SC-XX)

**Actors:** [Container names involved]
**Trigger:** [What starts this flow]

[Container-level sequence diagram]

[One sentence: what this diagram shows and any notable interaction patterns.]

[Repeat for each scenario.]

---

## 7. Interface Contracts

[One entry per inter-container relationship. Sourced from Stage 03 contracts artifact.]

### [Consumer] → [Producer]

| Field | Value |
|-------|-------|
| Protocol | ... |
| Format | ... |
| Direction | Synchronous / Asynchronous |
| Endpoint / Topic | ... |
| Key Request Fields | ... |
| Key Response Fields | ... |
| Error Handling | ... |
| Auth | ... |

[Repeat for each contract.]

---

## 8. Components (C4 Level 3)

[Repeat per container that has a component diagram]

### 8.1 [Container Name]

**Pattern:** [Layered / CQRS / Hexagonal / Feature Modules / Pipeline Worker / other]
**Why:** [One sentence rationale from Stage 04 component-scope artifact]

[Level 3 diagram]

[1-paragraph narrative from Stage 04 output]

#### Sequence Detail: [Scenario Name] inside [Container Name]

[Component-level sequence diagram from Stage 04 sequences-l3 artifact.
One block per scenario that passes through this container.
Shows which components handle which steps of the scenario.]

[Repeat sequence detail blocks for each relevant scenario.]

---

## 9. Tech Stack Rationale

| Technology | Role | Why Chosen | Tradeoff / Ruled Out |
|------------|------|------------|----------------------|

[Source: tech-decisions log. One row per technology in system-meta.md tech stack.]

---

## 10. Key Architectural Decisions

[5-10 decisions drawn from tech-decisions log. Prioritise non-obvious choices.]

### Decision: [Short name]
**Why:** [Rationale in 1-2 sentences]
**Tradeoff:** [What was given up or what was explicitly not done]

---

## 11. Open Questions

[Unresolved items from discovery and subsequent stages, each as a bullet with owner if known]

---

## Appendix: Diagram Legend

[Key explaining shape meanings for all diagrams in this document]
```

---

## Writing Rules

**Audience calibration:**
- Engineering team: include technology names, protocol details, data flow specifics
- New engineers onboarding: add one sentence of "why" for each major choice
- External stakeholders: replace technology names with function descriptions; remove protocol detail; omit Interface Contracts section or summarise in prose

**User Flows:**
- Diagrams must stay business-level -- no container names, no technology, no API paths
- Each flow narrative answers: what is the user trying to do, what happens on success, what are the main failure cases
- For external stakeholders audience: this section may be the most important -- give it prominence

**Sequence Diagrams (container and component level):**
- Container-level: actors are containers from Level 2 diagram -- names must match exactly
- Component-level: actors are components from Level 3 diagram -- names must match exactly
- Each sequence diagram must have a title referencing the scenario ID (e.g., "SC-01: Customer Places Order")
- For external stakeholders audience: omit component-level sequences; keep only container-level

**Narrative paragraphs:**
- Must be redundant with the diagram above -- no new information
- Written in present tense: "The API server receives requests from..."
- No marketing language: "robust", "scalable", "enterprise-grade" are banned

**Non-Functional Requirements:**
- State concrete values where known: "p99 < 200ms" not "low latency"
- Mark unknowns explicitly as "Not yet defined" -- do not omit rows
- Link to SLAs or compliance docs if they exist externally

**Interface Contracts:**
- Include only container-boundary contracts -- not internal method signatures
- If a contract is partial or provisional, mark fields as "TBD" and add to Open Questions
- For external system contracts (third-party APIs), link to the provider's docs rather than duplicating

**Tech Stack Rationale:**
- One row per technology -- do not group "frontend stack" into one row
- "Why Chosen" must be a reason, not a description: "team expertise + ACID needed" not "it's a relational database"
- "Tradeoff / Ruled Out" names what was considered and rejected, or what is sacrificed

**Key Architectural Decisions:**
- Focus on non-obvious choices: if a reader would assume the choice, skip it
- Include choices about what was NOT done: "We chose not to use microservices because..."
- Each decision under 100 words total
- Draw from the full tech-decisions log; do not invent decisions not captured there

**Open Questions:**
- Phrase as questions, not statements: "Should the cache be per-region or global?" not "Cache region TBD"
- Include owner if known: "(Owner: platform team)"
- Remove items that were resolved during the documentation process
