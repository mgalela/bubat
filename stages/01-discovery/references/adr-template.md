# ADR Template

Format for every entry in `{slug}-tech-decisions.md`. One ADR per decision. **Append only — never edit a past entry.**

---

## Numbering

Flat sequential across all stages: `ADR-001`, `ADR-002`, …  
Stage of origin is recorded in the **Stage** field, not the number.

---

## File Header

Seed the file with this header when it is first created (Stage 01):

```markdown
# Architecture Decision Log: [System Name]

> Append-only. One ADR per decision. Do not edit past entries.
> To supersede a decision, write a new ADR and set the old entry's Status to `Superseded by ADR-NNN`.
```

---

## Entry Format

```markdown
---

# ADR-NNN: [Short imperative title — state what was decided, not what was considered]

**Date:** YYYY-MM-DD
**Stage:** NN-[stage-name]  <!-- e.g. 01-discovery, 03-container -->
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN

## Context

<!--
What forces, constraints, or requirements led to this decision?
Cover: business drivers, technical constraints, team skills, timeline pressure, compliance needs.
2–4 sentences. No solution discussion here — only why a decision was needed.
-->

## Decision

<!--
What was decided? Write as an active statement: "We will use X."
Include the primary reason: "We will use X because Y."
One short paragraph.
-->

## Alternatives Considered

| Option | Reason Rejected |
|--------|----------------|
|        |                |

## Consequences

**Positive:**
-

**Negative / Trade-offs:**
-

**Risks:**
-

---
```

---

## Field Rules

| Field | Rule |
|-------|------|
| **Title** | Imperative, ≤10 words. "Use PostgreSQL for primary storage." Not "Database selection." |
| **Date** | ISO 8601: `YYYY-MM-DD`. Use the date the decision was made, not when it was written. |
| **Stage** | The BUBAT stage where this decision surfaced. Technology choices from discovery → `01-discovery`. |
| **Status** | Start `Proposed` if not yet confirmed by a human. Set to `Accepted` when confirmed. |
| **Context** | Forces only — no solution. A reader should understand *why* without reading the decision. |
| **Decision** | One clear statement. Avoid "we decided to consider" — decide or escalate. |
| **Alternatives** | At least one row. "No alternatives considered" is a smell — record what was implicitly ruled out. |
| **Consequences** | Honest. Negative consequences are expected; hiding them undermines the log's value.               |

---

## Statuses

| Status                  | Meaning                                                           |
| ----------------------- | ----------------------------------------------------------------- |
| `Proposed`              | Decision drafted, not yet confirmed by a human stakeholder        |
| `Accepted`              | Confirmed and in effect                                           |
| `Deprecated`            | No longer relevant; system moved on but decision was not replaced |
| `Superseded by ADR-NNN` | Replaced by a later decision — link the new ADR number            |

---

## Rerun / Duplicate Policy

Before appending new ADR during `update` or rerun:

1. Search existing log for same **Stage** + ADR title/decision.
2. If unchanged, do not append duplicate ADR.
3. If changed, append next ADR number and set previous decision status to `Superseded by ADR-NNN` only if user explicitly allows editing historical status; otherwise mention `Supersedes: ADR-NNN` in new ADR Context.
4. Never create multiple active ADRs for same stage + same decision topic.

---

## Seeding at Stage 01

When populating the tech decisions log from discovery, create one ADR per technology choice captured in the Technology Choices section of the discovery report. Minimum fields to populate:

- **Context:** why this technology was chosen / what problem it solves
- **Decision:** the specific technology and version (if known)
- **Alternatives:** what was explicitly ruled out, or "None stated — record if known"
- **Consequences:** known trade-offs (e.g., operational burden, learning curve, licensing)
