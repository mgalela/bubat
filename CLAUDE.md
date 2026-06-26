# BUBAT

Architecture documentation workspace using C4 model, built on ICM conventions.
Stages `01–04` are architecture source of truth; Stage `06` bridges to cavekit.

Workspace root rule:
- standalone install: workspace root = current directory
- embedded install (`--dir .bubat`): workspace root = `.bubat/`
- resolve workspace root before reading `shared/`, `stages/`, `raw/`, `triage/`, `setup/`

## Always Use Registries

- Run protocol: `shared/stage-runbook.md`
- Stage routing/load boundaries: `shared/stage-index.md`
- Artifact ownership: `shared/output-catalog.md`
- Gates: `shared/stage-gates.md`
- Change workflow: `shared/architecture-source-of-truth.md`

## Triggers

| Keyword | Action |
|---------|--------|
| `setup` | run onboarding; populate `shared/system-meta.md` |
| `stage <id>` | invoke `skills/bubat-stage` |
| `raw add <path>` | invoke `skills/bubat-raw-add` |
| `raw route` | invoke `skills/bubat-raw-route` |
| `bubat-r feed bubat [path]` | invoke `skills/bubat-r-feed-bubat`; deterministic BUBAT-R reconstruction mapping into `raw/MANIFEST.md` |
| `status` | invoke `skills/bubat-status` |
| `where <term>` / `trace <term>` / `find artifact <term>` | invoke `skills/bubat-trace`; ultra-cheap grep-first manifest lookup, then optional summary/open |
| `refresh index` | invoke `skills/bubat-refresh-index`; rebuild `shared/artifact-manifest.ndjson`, `shared/artifact-index.json`, `shared/triage-index.json`, `shared/research-index.json` |
| `sync index <path(s)>` | invoke `skills/bubat-sync-index`; incremental index sync after artifact save/update/delete |
| `diagram <stage>` | invoke `skills/bubat-diagram` |
| `update <stage(s)>` | invoke `skills/bubat-update`; use `@commands/cl/research_codebase.md` on existing repos |
| `triage <idea>` | invoke `skills/bubat-triage`; create impact map and cavekit/code plan |
| `bridge` | invoke `skills/bubat-bridge` |
| `sync graphify` | invoke `skills/bubat-graphify-sync` |

## Existing Project Precision

If BUBAT used inside existing project, use `@commands/cl/research_codebase.md` during each stage to explore current codebase with stage-specific scope before writing artifacts.
- treat codebase research as precision aid
- do not let codebase override architecture source-of-truth rules
- keep `01–04` outputs authoritative after confirmation

## Source-of-Truth Loop

```text
triage <feature/change>
→ update affected stages
→ bridge
→ cavekit/code changes
→ update 04
→ bridge if SPEC task pointers changed
```

Rules:
- `01–04` outputs = architecture truth.
- `06-spec` output = cavekit implementation plan.
- codebase = runtime implementation.
- `04-component` code map = component → file/symbol/line trace.
- architecture-significant code work must pass G9.

## Gates

Read `shared/stage-gates.md` before stage work. Apply G0–G9 as relevant.

## Folders

```text
shared/   registries, gates, source-of-truth rules
skills/   trigger implementations
commands/ reusable command prompts, incl. codebase research
agents/   specialist research agents used by commands
stages/   stage contexts, references, outputs
raw/      source materials routed by manifest
triage/   feature/change impact reports
setup/    onboarding questionnaire
```

Raw path note:
- standalone: `raw/`
- embedded: `.bubat/raw/`
- optional external sources: register with `raw add <path>`
