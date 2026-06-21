# Stage Gates

Quality gates run between stages. A downstream stage may start only when its upstream inputs pass these checks.

## Gate Types

| Gate | When | Pass Condition | Failure Action |
|------|------|----------------|----------------|
| G0 Workspace | before any stage | `shared/system-meta.md` has no setup placeholders; `raw/MANIFEST.md` exists | run `setup` / `raw route` or create empty manifest |
| G1 Input | before stage run | every required upstream artifact exists, or missing artifact is explicitly allowed by current stage | stop and run missing upstream stage |
| G2 Stage Audit | before writing output | all checks in current stage `Audit` table pass | fix artifact before save |
| G3 Placeholder | before save | no unresolved `{{PLACEHOLDER}}` in generated outputs | replace or mark `[MISSING — reason]` |
| G4 Traceability | before downstream stage | outputs cite source stage/artifact for extracted decisions, flows, contracts, invariants | add source notes |
| G5 Diagram | before save of diagram artifacts | diagram code uses configured format and names match upstream labels exactly | re-render diagram only |
| G6 ADR | before appending tech decisions | no duplicate ADR for same stage + decision title; changed decisions supersede prior ADR | append superseding ADR, do not duplicate |
| G7 Bridge | before saving Stage 06 artifacts | all §C/§V entries trace to extraction map; missing inputs noted explicitly; all interface spec TODO items documented | fill map or mark missing |
| G8 Test Scaffold | before saving Stage 08 artifacts | Stage 07 validation report exists and contains zero Blocking findings | resolve all Blocking findings in Stage 07 report first |
| G9 Architecture Source of Truth | before architecture-significant code work and after code changes | Feature/change request has triage impact artifact; Stage 06 bridge is refreshed before code work; Stage 04 code map is refreshed after code work | run `triage <request>`, `bridge`, then post-code `update 04` |

## Required Stage Order

`setup → 01-discovery → 01b-flow → 01c-bounded-context → 01d-data-model → 02-context → 03-container → 04-component → 05-document → 06-spec → 07-spec-validation → 08-test-scaffold`

`raw route` may run before or after `setup`, but must run before any stage consumes `raw/` materials.

Stage 06 (`bridge`) may be run before Stage 05 -- it does not depend on `05-document` output. If upstream stages are incomplete, Stage 06 emits `[MISSING — run stage XX first]` markers rather than blocking entirely.

## Output Policy

| Artifact Type | Rerun Behavior |
|---------------|----------------|
| Stage output files | overwrite whole artifact after checkpoint confirmation |
| Diagram-only update | replace diagram block only; preserve narrative/tables |
| Tech decisions log | append-only; if decision changed, append new ADR with `Supersedes: ADR-NNN` |
| Raw manifest | overwrite generated table after review confirmation |
| Interface spec files (openapi.yaml, .proto, -interfaces.*) | overwrite whole file after checkpoint confirmation |

## Architecture Source-of-Truth Rule

Stages `01` through `04` are architecture source of truth. For architecture-significant changes, run `triage <request>` before implementation, update affected stages, run Stage 06 `bridge` for cavekit, then refresh Stage 04 code map after code changes. See `shared/architecture-source-of-truth.md`.

## Manifest Rule

`raw/MANIFEST.md` uses table columns `File`, `Stages`, `Notes`. A stage may read only rows where `Stages` contains its exact stage id, e.g. `01-discovery`.
