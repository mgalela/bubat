---
name: bubat-diagram
description: Re-render diagrams for a specific BUBAT stage without re-running the full stage. Use when user types "diagram <stage>" in a BUBAT workspace.
---

# BUBAT Diagram Re-render

Given the target stage argument:

1. Read the target stage's `CONTEXT.md` to identify which output file contains the diagram.
2. Read the existing output artifact.
3. Re-render only the diagram block(s) using the format in `shared/system-meta.md`.
4. Replace the diagram block(s) in the artifact. Preserve all narrative, tables, and other content.
5. Confirm: "Diagram re-rendered for Stage XX. No other content changed."
