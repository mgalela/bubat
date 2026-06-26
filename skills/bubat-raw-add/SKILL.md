---
name: bubat-raw-add
description: Register external raw source paths so `raw route` can scan files outside workspace raw/ folder. Use when user types `raw add <path>` in BUBAT workspace.
---

# BUBAT Raw Add

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Resolve user path argument `<path>` in this order:
1. path as typed from current directory
2. `${WORKSPACE_ROOT}/<path>`
3. if `WORKSPACE_ROOT` = `.bubat`, also try sibling project-root path `<path>` outside workspace
4. if none exist, stop and ask user to confirm path

Rules:
- accept file or directory
- keep path relative when possible
- do not copy files into `raw/`; register source path only
- if path already registered in `${WORKSPACE_ROOT}/raw/SOURCES.md`, report `already registered`

Write or update `${WORKSPACE_ROOT}/raw/SOURCES.md` using this format:

```markdown
# raw/SOURCES.md

<!-- Optional external sources for `raw route`. Edit manually if needed. -->

| Path | Type | Recursive | Notes |
| ---- | ---- | --------- | ----- |
| docs/ | dir | yes | Existing project docs |
| openapi.yaml | file | no | Root API contract |
```

Defaults:
- directory => `Recursive = yes`
- file => `Recursive = no`
- `Notes` short user intent if provided, else inferred from path name

After save, report:
- registered path
- source file/dir type
- next step: `raw route`
