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
5. Append a note to `{slug}-tech-decisions.md` marking which stages were updated and why (ask the user for the reason).
6. After all stages complete, invoke skill `bubat-status` to confirm.
