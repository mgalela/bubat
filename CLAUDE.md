# C4ICM

Architecture documentation workspace using the C4 model, built on ICM conventions.
One system through four levels of zoom: context, containers, components, and assembled document.

## Folder Map

```
C4ICM/
├── CLAUDE.md                           (you are here)
├── CONTEXT.md                          (task routing)
├── setup/
│   └── questionnaire.md               (system onboarding -- run once)
├── shared/
│   ├── system-meta.md                 (system name, purpose, tech stack -- populated at setup)
│   └── c4-notation.md                 (C4 element rules and naming conventions)
└── stages/
    ├── 01-discovery/                  (gather system info from stakeholders and docs)
    ├── 02-context/                    (C4 Level 1 -- system context diagram)
    ├── 03-container/                  (C4 Level 2 -- container diagram)
    ├── 04-component/                  (C4 Level 3 -- component diagrams per container)
    └── 05-document/                   (assemble final architecture document)
```

## Triggers

| Keyword | Action |
|---------|--------|
| `setup` | Run onboarding -- collects system info and populates shared/system-meta.md |
| `status` | Show pipeline completion for all five stages |
| `diagram <stage>` | Re-render diagrams for a specific stage without re-running the full stage |
| `update <stage(s)>` | Re-run one or more stages after system changes -- e.g. `update 03` or `update 03 04 05` |

### How `status` works

Scan `stages/*/output/` folders. COMPLETE if files exist beyond .gitkeep, PENDING otherwise.

```
Pipeline Status: C4ICM

  [01-discovery] --> [01b-flow] --> [02-context] --> [03-container] --> [04-component] --> [05-document]
      STATUS            STATUS          STATUS           STATUS              STATUS             STATUS
```

### How `diagram` works

1. Read the target stage's CONTEXT.md to identify which output file contains the diagram.
2. Read the existing output artifact.
3. Re-render only the diagram block(s) using the format in `shared/system-meta.md`.
4. Replace the diagram block(s) in the artifact. Preserve all narrative, tables, and other content.
5. Confirm: "Diagram re-rendered for Stage XX. No other content changed."

### How `update` works

1. Parse which stage numbers were specified (e.g. `update 03 04 05`).
2. Warn: downstream stages will be re-run -- confirm before proceeding.
3. Re-run each specified stage in order, starting from the lowest number.
4. Each re-run stage reads its inputs fresh (including any upstream outputs that were re-run in the same pass).
5. Append a note to `{slug}-tech-decisions.md` marking which stages were updated and why (ask the user for the reason).
6. After all stages complete, run `status` to confirm.

## Routing

| Task | Go To |
|------|-------|
| Gather system information | `stages/01-discovery/CONTEXT.md` |
| Capture business flows and scenarios | `stages/01b-flow/CONTEXT.md` |
| Build C4 Level 1 diagram | `stages/02-context/CONTEXT.md` |
| Build C4 Level 2 diagram | `stages/03-container/CONTEXT.md` |
| Build C4 Level 3 diagrams | `stages/04-component/CONTEXT.md` |
| Assemble architecture doc | `stages/05-document/CONTEXT.md` |
| Re-render a diagram only | Use `diagram <stage>` trigger |
| Re-run after system changes | Use `update <stage(s)>` trigger |

## What to Load

| Task | Load These | Do NOT Load |
|------|-----------|-------------|
| Discovery | `shared/system-meta.md`, `stages/01-discovery/references/discovery-guide.md` | `stages/01b-flow/` through `stages/05-document/` |
| Business flows | `stages/01-discovery/output/`, `shared/system-meta.md`, `stages/01b-flow/references/` | `stages/02-context/` through `stages/05-document/` |
| Context diagram | `stages/01-discovery/output/`, `shared/c4-notation.md`, `stages/02-context/references/` | `stages/03-container/` through `stages/05-document/` |
| Container diagram | `stages/02-context/output/`, `stages/01b-flow/output/`, `shared/c4-notation.md`, `stages/03-container/references/` | `stages/04-component/`, `stages/05-document/` |
| Component diagrams | `stages/03-container/output/`, `shared/c4-notation.md`, `stages/04-component/references/` | `stages/05-document/` |
| Final document | `stages/01b-flow/output/`, `stages/02-context/output/`, `stages/03-container/output/`, `stages/04-component/output/`, `stages/05-document/references/` | `stages/01-discovery/` |
