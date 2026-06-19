# Discovery Guide

Questions that shape the system discovery. Cover every topic. Record answers verbatim first, then structure.

## System Boundary

- What does this system do? (the core job, in one sentence)
- What does it NOT do? (where it stops and another system begins)
- What would break if this system went down?

## Users and Actors

- Who uses this system directly? (list all human roles)
- For each user: what is their primary goal when using the system?
- Are there batch jobs, scheduled tasks, or automated processes that act on the system?

## External Systems

- What systems does this one send data TO? (name + what is sent)
- What systems does this one receive data FROM? (name + what is received)
- Which of these are inside your organization, and which are third-party services?
- Are there any external systems where the relationship is bidirectional?

## Internal Structure (preview for Stage 02-03)

- At the highest level, what are the major parts of this system? (e.g., web app, API, database, worker)
- Which parts are separately deployed? (own server, own container, own process)
- Which parts share a deployment unit?
- Are there functional areas owned by different teams or squads?
- Are there any domain terms that mean different things in different areas of the system?
  (e.g., "Customer" in sales vs. "Customer" in support -- same word, different meaning)
- Which areas of the system change most frequently? Which are most stable?

## Existing Artifacts

- Is there a README, architecture doc, or ADR that describes the system?
- Are there existing diagrams (draw.io, Lucidchart, Confluence, Miro)?
- Is there an API spec (OpenAPI, Swagger, GraphQL schema)?

## Non-Functional Requirements

- What are the expected load or scale targets? (concurrent users, requests/sec, data volume)
- Are there latency or response time requirements? (e.g., p99 < 200ms)
- What are the availability and uptime requirements? (e.g., 99.9% SLA)
- Are there data retention or compliance requirements? (e.g., GDPR, SOC2, PCI-DSS)
- Are there security requirements? (authentication method, encryption at rest/in transit, network isolation)
- Are there disaster recovery requirements? (RTO, RPO)
- Are there geographic or data residency constraints? (region pinning, data sovereignty)

## Technology Choices

- What is the primary tech stack and why was it chosen? (language, framework, database, cloud provider)
- Were any technologies explicitly ruled out? Why?
- Are there technology constraints imposed by the organisation or platform team?
- What implementation patterns are planned or in use? (e.g., event-driven, CQRS, microservices, monolith)
- Are there existing shared services or platforms that this system must integrate with?

## Pattern Signal Capture

After answering NFRs and Technology Choices, extract constraint signals for architectural style (Stage 03) and component pattern (Stage 04) decisions. Record these in the discovery output under a "Pattern Signals" section.

| Constraint Signal | Source Question | Stage 03 Implication | Stage 04 Implication |
|---|---|---|---|
| High scale (>1 000 RPS) or independent scaling needed | Scale targets | Separate services over monolith | — |
| Multiple teams / squads own different areas | Internal structure | Team boundaries → service boundaries | — |
| Different release cadences per area | Which areas change most? | Separate deployable units per high-change area | — |
| Strong consistency / ACID across BCs | Data volume + compliance | Shared DB or modular monolith over microservices | — |
| Single team, early stage, simple domain | Team size + core job | Modular monolith; split later | Layered (default) |
| Read/write ratio >10:1 or distinct latency SLAs | NFR latency + scale | — | CQRS candidate |
| Long-running tasks flagged | Existing structure | Async worker container | Pipeline Worker |
| Swappable external integrations or compliance isolation | External systems + security | — | Hexagonal |
| Heavy business logic concentrated in one BC | BC complexity from Stage 01c | — | Layered or Hexagonal |

If a signal is absent or unknown, record "Not determined" — do not guess. Gaps here are open questions to resolve before Stage 03.

---

## Output Format

Structure the discovery artifact as:

```markdown
# Discovery: [System Name]

## System Boundary
[One paragraph on what the system is and is not]

## Users
| Role | Description | Primary Goal |
|------|-------------|--------------|
| ... | ... | ... |

## External Systems
| System | Direction | What is Exchanged |
|--------|-----------|-------------------|
| ... | Sends to | ... |
| ... | Receives from | ... |

## Non-Functional Requirements
| Attribute | Requirement | Notes |
|-----------|-------------|-------|
| Availability | ... | ... |
| Latency | ... | ... |
| Scale | ... | ... |
| Security | ... | ... |
| Compliance | ... | ... |
| DR / RTO / RPO | ... | ... |

## Technology Choices
| Technology | Role | Why Chosen | Constraints / Ruled Out |
|------------|------|------------|------------------------|
| ... | ... | ... | ... |

## Pattern Signals
| Signal | Source | Stage 03 Implication | Stage 04 Implication |
|--------|--------|----------------------|----------------------|
| ... | ... | ... | ... |

## High-Level Structure (preview)
[Bullet list of major parts identified -- not yet formal containers]

## Open Questions
[Anything ambiguous or unresolved that needs follow-up]
```
