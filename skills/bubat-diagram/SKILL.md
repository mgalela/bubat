---
name: bubat-diagram
description: Re-render diagrams for a specific BUBAT stage without re-running the full stage. Use when user types "diagram <stage>" in a BUBAT workspace.
---

# BUBAT Diagram Re-render

Resolve `WORKSPACE_ROOT` first:
- use `.` if `shared/stage-index.md` exists in current directory
- else use `.bubat` if `.bubat/shared/stage-index.md` exists
- else stop and ask user to confirm BUBAT workspace root

Given the target stage argument:

1. Read the target stage's `${WORKSPACE_ROOT}/stages/<stage-id>/CONTEXT.md` to identify which output file contains the diagram.
2. Read the existing output artifact.
3. Re-render only the diagram block(s) using the format in `${WORKSPACE_ROOT}/shared/system-meta.md`.
4. Replace the diagram block(s) in the artifact. Preserve all narrative, tables, and other content.
5. Confirm: "Diagram re-rendered for Stage XX. No other content changed."
