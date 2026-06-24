# Domain Map

Project: `[PROJECT]`  
Date: `[YYYY-MM-DD]`

## Reconstruction Basis

Inputs:
- `03-main-spine.md`
- `05-behavior-spine.md`
- `06-ownership-map.md`
- `02-coverage-ledger.md`

## Candidate Contexts

| Context | Responsibility | Owned Data | Commands | Events | Confidence | Evidence |
|---|---|---|---|---|---|---|
| `[context]` | `[responsibility]` | `[entities]` | `[commands]` | `[events]` | Inferred | `EV-...` |

## Context Relationships

| Upstream | Downstream | Relation | Mechanism | Evidence | Notes |
|---|---|---|---|---|---|
| `[context]` | `[context]` | customer/supplier/peer | API/event/shared DB | `path:line` | |

## Decision-Making Zones

| Zone | Decisions Made | Evidence | Related Data |
|---|---|---|---|
| `[zone]` | `[decisions]` | `path:line` | `[entities]` |

## Read / Projection Zones

| Zone | Reads From | Purpose | Evidence |
|---|---|---|---|
| `[zone]` | `[source]` | `[purpose]` | `path:line` |

## Ambiguous Boundaries

| Boundary | Ambiguity | Evidence | Required Validation |
|---|---|---|---|
| `[boundary]` | `[ambiguity]` | `EV-...` | `[validation]` |
