# BUBAT

Architecture documentation workspace. Document any software system through four levels of zoom using the [C4 model](https://c4model.com), then export a ready-to-use [cavekit](https://github.com/JuliusBrussee/cavekit) `SPEC.md` plus interface specs (OpenAPI, proto3, Go/TS/Java interfaces) for implementation.

Inspired by / built on ideas from [Interpreted Context Methodology](https://github.com/RinDig/Interpreted-Context-Methdology).

---

## Pipeline

```
raw/ → setup → 01-discovery → 01b-flow → 01c-bounded-context → 01d-data-model
                                                                      ↓
                                          05-document ← 04-component ← 03-container ← 02-context
                                               ↓ (optional)                ↓
                                           stakeholder            06-spec (bridge)
                                             review                    ↓
                                                        SPEC.md + openapi.yaml + .proto + interfaces.*
                                                                    ↓
                                                           07-spec-validation
                                                                    ↓
                                                           08-test-scaffold
                                                                    ↓
                                                               cavekit /ck:build
```

| Stage                 | Output                                                                                                                                          |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `01-discovery`        | System goals, NFRs, tech constraints, ADR log                                                                                                   |
| `01b-flow`            | Business flows, user journeys, key scenarios                                                                                                    |
| `01c-bounded-context` | Bounded context map, ubiquitous language, context relationships                                                                                 |
| `01d-data-model`      | Entity inventory, ER model, storage hints                                                                                                       |
| `02-context`          | C4 Level 1 — system context diagram                                                                                                             |
| `03-container`        | C4 Level 2 — container diagram, interface contracts, sequences                                                                                  |
| `04-component`        | C4 Level 3 — component diagrams per container + component code map                                                                              |
| `05-document`         | Final architecture document (assembled, audience-ready) — **optional**, for stakeholder review only                                             |
| `06-spec`             | `SPEC.md` bridge → cavekit spec + `openapi.yaml` + `.proto` + language interfaces — reads stages 01–04 directly, does not require `05-document` |
| `07-spec-validation`  | Validate Stage 06 outputs for completeness, testability, and consistency                                                                        |
| `08-test-scaffold`    | BDD/unit/integration/e2e test scenarios derived from validated spec                                                                             |

---

## Install

**Standalone workspace** (open the created directory in Claude Code):

```bash
npx create-bubat my-arch
```

**Embed in existing project** (patches paths, adds `@import` hint for project `CLAUDE.md`):

```bash
npx create-bubat --dir .bubat
```

Then add the printed line to your project `CLAUDE.md`:

```
@.bubat/CLAUDE.md
```

Embed mode note:
- workspace files live under `.bubat/`
- raw files go in `.bubat/raw/`
- triggers may be run from project root after skill update, or from `.bubat/` directly

**Update an existing workspace** (preserves user data, updates framework files):

```bash
npx create-bubat --update my-arch
npx create-bubat --update --dir .bubat
```

**Install/update from a pinned release/tag** (not branch `main`):

```bash
# npm published version
npx create-bubat@1.0.0 my-arch
npx create-bubat@1.0.0 --update my-arch

# GitHub release/tag
npx github:mgalela/bubat#v1.0.0 my-arch
npx github:mgalela/bubat#v1.0.0 --dir .bubat
npx github:mgalela/bubat#v1.0.0 --update my-arch
npx github:mgalela/bubat#v1.0.0 --update --dir .bubat
```

The script copies templates from the package version/tag that `npx` resolved, so pinned tag installs do not depend on branch `main`.

Preserved on update: `shared/system-meta.md`, `raw/MANIFEST.md`, `raw/SOURCES.md`, `stages/*/output/*`.
New stages added automatically.

---

## Quickstart

**New system from scratch:**

```
setup
```

**Have existing docs (PRD, ADRs, diagrams, API specs)?**

Standalone workspace:

```
1. Drop files into raw/ or register external docs with `raw add <path>`
2. raw route
3. setup
```

Embedded workspace (`--dir .bubat`):

```
1. Drop files into .bubat/raw/ or register external docs with `raw add <path>`
2. Run raw route from project root or cd .bubat first
3. setup
```

**Run pipeline stage by stage:**

```
stages/01-discovery/CONTEXT.md   → discovery
stages/01b-flow/CONTEXT.md       → flow
stages/01c-bounded-context/...   → bounded context
stages/01d-data-model/...        → data model
stages/02-context/...            → context diagram
stages/03-container/...          → container diagram
stages/04-component/...          → component diagrams
stages/05-document/...           → architecture doc
stages/06-spec/...               → cavekit SPEC.md
stages/07-spec-validation/...    → spec validation report
stages/08-test-scaffold/...      → test scaffold
```

**Export to cavekit:**

```
bridge
→ copy stages/06-spec/output/SPEC.md to project root
→ copy openapi.yaml / .proto / interfaces.* to project as needed
→ /ck:review → /ck:build
```

---

## Triggers

| Keyword             | Action                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `setup`             | Onboarding — collect system info, populate `shared/system-meta.md`                             |
| `stage <id>`        | Run a stage using shared stage registry — e.g. `stage 04`                                      |
| `raw add <path>`    | Register external file/dir as raw source before routing — e.g. `raw add docs/`                 |
| `raw route`         | Scan workspace `raw/` plus registered external sources, assign stage(s), write `raw/MANIFEST.md` |
| `status`            | Show pipeline completion across all stages                                                     |
| `bridge`            | Run stage 06-spec — convert all outputs into `SPEC.md` + interface specs                       |
| `diagram <stage>`   | Re-render diagrams for a stage without re-running the full stage                               |
| `update <stage(s)>` | Re-run stages after system changes — e.g. `update 03 04 05`                                    |
| `triage <idea>`     | Map feature/change request to impacted architecture stages, code map rows, and cavekit handoff |
| `sync graphify`     | Feed completed stage outputs back into the project graphify graph                              |

---

## Folder Structure

```
BUBAT/
├── CLAUDE.md                     agent instructions
├── CONTEXT.md                    task routing
├── README.md                     this file
├── raw/                          drop existing materials here
│   ├── README.md                 what to drop and how routing works
│   ├── SOURCES.md                optional external source registry for `raw add`
│   └── MANIFEST.md               generated by `raw route`
├── triage/                       feature/change impact reports
├── setup/
│   └── questionnaire.md          system onboarding
├── skills/                       Claude Code skills (auto-installed by create-bubat)
│   ├── bubat-stage/              generic stage runner
│   ├── bubat-raw-add/            external raw source registration skill
│   ├── bubat-raw-route/          raw route skill
│   ├── bubat-status/             status skill
│   ├── bubat-diagram/            diagram skill
│   ├── bubat-update/             update skill
│   ├── bubat-triage/             triage skill
│   ├── bubat-bridge/             cavekit bridge skill
│   └── bubat-graphify-sync/      graphify sync skill
├── shared/
│   ├── system-meta.md            system name, purpose, tech stack, interface formats
│   ├── c4-notation.md            C4 element rules and naming conventions
│   ├── stage-runbook.md          common stage execution protocol
│   ├── stage-index.md            stage registry, inputs, outputs, load boundaries
│   ├── output-catalog.md         artifact ownership and consumers
│   ├── stage-gates.md            cross-stage quality gates and rerun policy
│   └── architecture-source-of-truth.md  truth hierarchy, feature workflow, drift rules
└── stages/
    ├── 01-discovery/             goals, NFRs, tech decisions
    ├── 01b-flow/                 business flows, scenarios
    ├── 01c-bounded-context/      domain boundaries, context map
    ├── 01d-data-model/           entity model, storage hints
    ├── 02-context/               C4 Level 1 diagram
    ├── 03-container/             C4 Level 2 diagram + contracts
    ├── 04-component/             C4 Level 3 diagrams + component code map
    ├── 05-document/              final architecture doc
    ├── 06-spec/                  cavekit SPEC.md bridge + interface spec generation
    ├── 07-spec-validation/       spec completeness, testability, and consistency checks
    └── 08-test-scaffold/         BDD/unit/integration/e2e test scenario generation
```

Each stage has:

- `CONTEXT.md` — agent instructions, inputs, process, audit checks
- `references/` — guides, templates, format rules
- `output/` — generated artifacts

---

## Quality Gates

Cross-stage gate rules live in `shared/stage-gates.md`.

| Gate                              | Purpose                                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Workspace gate                    | setup placeholders cleared; `raw/MANIFEST.md` exists                                                     |
| Input gate                        | upstream outputs exist before downstream starts                                                          |
| Stage audit gate                  | current stage `Audit` table passes before save                                                           |
| Traceability gate                 | extracted decisions/flows/contracts/invariants cite sources                                              |
| Diagram gate                      | diagram code uses configured format; names match upstream labels                                         |
| ADR gate                          | no duplicate tech decisions on rerun; changed decisions append superseding ADR                           |
| Bridge gate                       | `SPEC.md` constraints/invariants trace to extraction map; interface spec TODOs documented                |
| Architecture source-of-truth gate | Architecture-significant changes have triage impact artifact; bridge before code; `update 04` after code |

---

## Raw Materials

Drop existing system documentation into workspace `raw/` before running `setup`, or register external source paths with `raw add <path>`.
- standalone: `raw/`
- embedded: `.bubat/raw/`
- external source examples: `docs/`, `openapi.yaml`, `../legacy-arch/`

Claude routes each file to correct stage automatically.
Requirements (BRD, PRD, problem statement), System docs (README, architecture doc, ADR log), API specs (OpenAPI/Swagger YAML, GraphQL schema, Postman collection), Process docs, Data docs (ERD, data dictionary, schema descriptions), Constraints (platform mandates, compliance requirements)

---

## Implementation Reference

Stages `01` through `04` are intended to be main reference for application implementation:

| Layer                   | Role                                                                   |
| ----------------------- | ---------------------------------------------------------------------- |
| `01–04` outputs         | business intent, domain boundaries, data model, containers, components |
| `06-spec` outputs       | Cavekit-ready implementation plan                                      |
| Codebase                | Runtime implementation                                                 |
| `04-component` code map | Trace index from component to file path/symbol/line span               |
| `triage/*-impact.md`    | Change intent and impact analysis                                      |

Feature/change workflow:

```text
triage <feature request>
→ writes triage/<date>-<feature>-impact.md
→ update affected stages 01–04
→ bridge
→ cavekit updates/adds code
→ update 04   # refresh code map
→ bridge      # refresh SPEC task pointers if needed
```

Architecture-significant code work should start with `triage`. After code changes, refresh Stage 04 code map so future triage can tell cavekit which files to update or add.

See `shared/architecture-source-of-truth.md` for governance and drift rules.

---

## Cavekit Integration

Stage `06-spec` bridges BUBAT architecture outputs into two categories of artifacts:

**1. Cavekit SPEC.md** — zero information loss, caveman-encoded. Every NFR, contract, domain invariant, and tech decision compressed into the spec.

| BUBAT Artifact                                      | SPEC.md Section  |
| --------------------------------------------------- | ---------------- |
| Discovery goals + purpose                           | `§G` goal        |
| NFRs, tech locks, compliance                        | `§C` constraints |
| Interface contracts, APIs, events                   | `§I` interfaces  |
| Tech decisions research findings                    | `§R` research    |
| BC rules, data constraints, scenario postconditions | `§V` invariants  |
| Container inventory (dependency-ordered)            | `§T` tasks       |

**2. Interface specs** — generated from container contracts and component diagrams.

Stage `04-component` also emits implementation trace artifact:

- `{slug}-component-code-map.md` — component → file path + symbol + line span
- source mode: `discovery` for existing code, `generated` after codegen/update

| Output file              | Generated when                     |
| ------------------------ | ---------------------------------- |
| `openapi.yaml`           | any HTTP/HTTPS contract exists     |
| `{slug}.proto`           | any gRPC contract exists           |
| `{slug}-interfaces.go`   | Go in tech stack                   |
| `{slug}-interfaces.ts`   | TypeScript / Node.js in tech stack |
| `{slug}-interfaces.java` | Java / Kotlin in tech stack        |

Format selection is auto-detected from tech stack and contract protocols, or set explicitly via `Interface formats` in `setup`.

After `bridge`:

1. Copy `stages/06-spec/output/SPEC.md` to project root
2. Copy interface specs (`openapi.yaml`, `.proto`, `interfaces.*`) to project as needed
3. Run `/ck:review` — adversarial spec review
4. Run `/ck:build` — implement

Architecture changes → `update <stages>` → `bridge` → `/ck:check` → `/ck:build`

---

## Graphify Integration

BUBAT integrates with [graphify](https://github.com/JuliusBrussee/graphify) in two directions:

**Discovery pre-fill** — if `graphify-out/` exists at `project_path`, Stage 01 auto-detects it and loads `GRAPH_REPORT.md` + `graph.json` as a pre-fill reference before user interview. Components, dependencies, and naming already extracted from code feed directly into discovery report — no duplicate work.

**Component implementation trace** — Stage 04 can inspect existing code under `project_path` and map each component to concrete files and line spans. If code does not exist yet, same artifact can be refreshed later after generation via `update 04`.

**Sync back** — after stages are complete, `sync graphify` feeds BUBAT outputs back into the project graph:

```
sync graphify
→ copies stages/*/output/*.md to <project_path>/docs/architecture/bubat/
→ runs graphify --update (re-indexes only new/changed files)
```

What graphify gains from BUBAT outputs:

| BUBAT output                    | What graphify extracts                                                 |
| ------------------------------- | ---------------------------------------------------------------------- |
| Discovery report                | System purpose, user roles, external dependencies as named nodes       |
| Business flows                  | Flow names and step sequences as hyperedges                            |
| BC map + context relationships  | Domain boundaries and integration patterns as community-spanning edges |
| Data model                      | Entity names and relationships with domain labels                      |
| Architecture diagrams (Mermaid) | Container/component relationships as inferred edges                    |
| Tech decisions log              | ADR rationale as `rationale_for` edges linking decisions to components |

Run after completing stages 01–04 minimum, or after any significant `update <stage>`.

---

## Skills

Triggers are implemented as installable Claude Code skills. `create-bubat` installs them automatically to `~/.claude/skills/` on install and `--update`.

| Skill                 | Trigger             |
| --------------------- | ------------------- |
| `bubat-stage`         | `stage <id>`        |
| `bubat-raw-add`       | `raw add <path>`    |
| `bubat-raw-route`     | `raw route`         |
| `bubat-status`        | `status`            |
| `bubat-diagram`       | `diagram <stage>`   |
| `bubat-update`        | `update <stage(s)>` |
| `bubat-triage`        | `triage <idea>`     |
| `bubat-bridge`        | `bridge`            |
| `bubat-graphify-sync` | `sync graphify`     |

Skills are standalone — they can be updated independently of the workspace via `npx create-bubat --update`.
