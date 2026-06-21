---
name: bubat-update
description: Re-run one or more BUBAT stages after system changes. Use when user types "update <stage(s)>" in a BUBAT workspace, e.g. "update 03" or "update 03 04 05".
---

# BUBAT Update

Given the stage numbers specified:

1. Parse which stage numbers were specified (e.g. `update 03 04 05`).
2. Warn: downstream stages will be re-run — confirm before proceeding.
3. Re-run each specified stage in order, starting from the lowest number.
4. Each re-run stage reads its inputs fresh (including any upstream outputs that were re-run in the same pass).
5. Special rule for `update 04`:
   - Refresh component diagrams, component sequences, component scope, and `output/{slug}-component-code-map.md`.
   - If `project_path` contains existing code, rebuild code map in `discovery` mode from actual files.
   - If code was newly generated after prior design, rebuild same map in `generated` mode from generated files.
   - Keep rows for planned components whose implementation still does not exist: mark `[MISSING — implementation not yet generated]` rather than dropping them.
6. Append a note to `{slug}-tech-decisions.md` marking which stages were updated and why (ask the user for the reason).
7. After all stages complete, invoke skill `bubat-status` to confirm.
