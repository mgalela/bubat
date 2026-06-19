# Graphify Output Guide for BUBAT Discovery

How to read and map graphify output artifacts into BUBAT discovery inputs.

---

## What Graphify Produces

After running `graphify <project_path>`, the `graphify-out/` directory contains:

| File | Content | BUBAT use |
|------|---------|-----------|
| `GRAPH_REPORT.md` | Human-readable audit: god nodes, surprising connections, suggested questions, community labels | Primary read — extract facts directly |
| `graph.json` | NetworkX node-link graph (nodes, links, community membership) | Secondary — query when GRAPH_REPORT.md lacks detail |
| `graph.html` | Interactive visualization | Reference only — do not parse |

---

## Reading GRAPH_REPORT.md

GRAPH_REPORT.md has these sections. Extract from each:

### God Nodes
High-centrality nodes — things everything else depends on.

- Map to: **key components** in 01-discovery, **container candidates** in Stage 03.
- Flag each god node label for human validation: is it a technical artifact (e.g., `utils.py`) or a real domain concept?

### Community Labels
Named clusters detected by community detection (e.g., "Auth Flow", "Payment Pipeline").

- Map to: **bounded context candidates** for Stage 01c.
- Treat each community label as a provisional BC name. Human must confirm domain alignment.
- Cross-community edges in Surprising Connections = integration points between BCs.

### Surprising Connections
Edges between nodes in different communities that graphify flagged as unexpected.

- Map to: **integration points** and **shared kernel candidates** for Stage 01c context map.
- Also check: does the surprising connection suggest a missing BC boundary?

### Suggested Questions
Questions graphify generated from the graph structure.

- Map to: **discovery gaps** — add to the list of topics to cover with the user.
- Prioritize questions that cross community boundaries.

---

## Reading graph.json

graph.json uses NetworkX node-link format. Key fields:

```json
{
  "nodes": [
    {
      "id": "auth_validatetoken",
      "label": "ValidateToken",
      "file_type": "code|document|paper|image",
      "source_file": "src/auth/session.py"
    }
  ],
  "links": [
    {
      "source": "auth_validatetoken",
      "target": "db_userrepository",
      "relation": "calls|implements|references|shares_data_with|rationale_for|semantically_similar_to",
      "confidence": "EXTRACTED|INFERRED|AMBIGUOUS",
      "confidence_score": 0.9
    }
  ]
}
```

**Confidence levels:**
- `EXTRACTED` (score 1.0) — relationship explicitly in source code. Trust as fact.
- `INFERRED` (score 0.6–0.9) — reasonable inference. Use as candidate, validate.
- `AMBIGUOUS` (score 0.1–0.3) — uncertain. Flag for human, do not assume.

---

## Mapping Rules: Graphify → BUBAT Stages

### Stage 01-discovery

| Graphify artifact | Extract | Note |
|---|---|---|
| God nodes | System's core components, tech stack anchors | Cross-check against system-meta.md tech stack |
| `rationale_for` edges | ADR candidates — why a decision was made | Seed tech-decisions log; confirm with user |
| Community count | Rough system complexity signal | High count = likely complex domain |
| `file_type: document` nodes | Existing documentation presence | Source for raw/ if not already there |

### Stage 01c — Bounded Context

| Graphify artifact | Extract | Note |
|---|---|---|
| Community labels | BC name candidates | Rename to ubiquitous language; technical names = red flag |
| Cross-community edges | Context relationships (conformist, anti-corruption, shared kernel) | Surprising connections = likely integration point |
| Community cohesion scores (in GRAPH_REPORT.md) | BC boundary confidence | Low cohesion = BC boundary may need splitting |

### Stage 01d — Data Model

| Graphify artifact | Extract | Note |
|---|---|---|
| `code` nodes with noun labels | Entity candidates | Filter: verbs and utility classes are not entities |
| `shares_data_with` edges | Entity relationships | Trust EXTRACTED; validate INFERRED |
| `semantically_similar_to` edges | Potential entity merge candidates | Same concept, different names = normalization opportunity |

### Stage 03 — Container

| Graphify artifact | Extract | Note |
|---|---|---|
| God nodes | Container candidates (high-centrality = likely a container) | One god node ≈ one container; validate with user |
| Community-level structure | Container grouping | Each community may correspond to one deployable unit |

### Stage 04 — Component

| Graphify artifact | Extract | Note |
|---|---|---|
| Non-god `code` nodes within a community | Component candidates | Filter out utilities and helpers by label |
| `calls|implements` edges within community | Component relationships | Use for component diagram arrows |

---

## Naming Translation Rules

Graphify node labels come from code identifiers. BUBAT uses domain ubiquitous language.

Before using any label as a domain concept:

1. Strip technical suffixes: `Repository`, `Service`, `Handler`, `Controller`, `Manager`, `Util`, `Helper` — these are patterns, not domain concepts. The prefix is the concept.
   - `OrderRepository` → `Order`
   - `PaymentService` → `Payment`

2. Flag abbreviations and acronyms for human expansion:
   - `TxnMgr`, `AuthSvc`, `UserCtrl` → ask the user what these mean.

3. Separate infrastructure from domain:
   - Infrastructure: `Database`, `Cache`, `Queue`, `Logger`, `Config`, `Router` — these are containers, not domain concepts.
   - Domain: nouns that non-technical stakeholders would recognize.

---

## What to Ignore

Do not carry these into BUBAT artifacts:

- Internal utility nodes: `logger`, `config`, `constants`, `utils`, `helpers`
- Test-only nodes: any node from `test/`, `spec/`, `__tests__/`
- Build and tooling nodes: `webpack`, `babel`, `eslint`, CI configuration files
- Edges with `confidence: AMBIGUOUS` and `confidence_score < 0.3` — too uncertain
- Nodes with `file_type: image` unless they contain architecture diagrams

---

## Staleness Check

Before using graphify output, ask the user:

> "Graphify output found at `<project_path>/graphify-out/`. When was this last generated? If the codebase has changed significantly since then, re-run `graphify <project_path> --update` for accurate results."

If the user confirms it's recent (or doesn't know), proceed and note it as provisional.
