# BUBAT Context

BUBAT documents architecture through C4 stages, then bridges to cavekit `SPEC.md`.

Workspace root rule:
- standalone install: workspace root = current directory
- embedded install (`--dir .bubat`): workspace root = `.bubat/`
- skills should resolve workspace root before reading `shared/`, `stages/`, `raw/`, `triage/`, `setup/`

## Use These Registries

| Need | File |
|------|------|
| Stage inputs/process protocol | `shared/stage-runbook.md` |
| Stage routing + load boundaries | `shared/stage-index.md` |
| Output artifact ownership | `shared/output-catalog.md` |
| Quality gates | `shared/stage-gates.md` |
| Feature/change workflow | `shared/architecture-source-of-truth.md` |

## Main Triggers

| Task | Trigger / Skill |
|------|-----------------|
| Run stage | `stage <id>` → `skills/bubat-stage/SKILL.md` |
| Add external raw source | `raw add <path>` → `skills/bubat-raw-add/SKILL.md` |
| Route raw files | `raw route` → `skills/bubat-raw-route/SKILL.md` |
| Show status | `status` → `skills/bubat-status/SKILL.md` |
| Re-render diagram | `diagram <stage>` → `skills/bubat-diagram/SKILL.md` |
| Update after change | `update <stage(s)>` → `skills/bubat-update/SKILL.md` + `@commands/cl/research_codebase.md` on existing repos |
| Triage feature/change | `triage <idea>` → `skills/bubat-triage/SKILL.md` |
| Generate cavekit spec | `bridge` → `skills/bubat-bridge/SKILL.md` |
| Sync architecture docs to graphify | `sync graphify` → `skills/bubat-graphify-sync/SKILL.md` |

## Existing Project Precision

If workspace attached to existing project, use `@commands/cl/research_codebase.md` during each stage for focused codebase exploration before drafting outputs.

Raw path note:
- standalone: `raw/`
- embedded: `.bubat/raw/`
- optional external sources: register with `raw add <path>`

## Source-of-Truth Loop

```text
triage <feature/change>
→ update affected stages
→ bridge
→ cavekit/code changes
→ update 04
→ bridge if task pointers changed
```

Stages `01–04` are design truth. Stage `04` code map links components to implementation files. Stage `06` is cavekit handoff.
