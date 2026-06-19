---
name: bubat-status
description: Show BUBAT pipeline completion status for all stages. Use when user types "status" in a BUBAT workspace.
---

# BUBAT Status

Scan `stages/*/output/` folders. COMPLETE if files exist beyond `.gitkeep`, PENDING otherwise.

Display pipeline in this exact format:

```
Pipeline Status: BUBAT

  [01-discovery] --> [01b-flow] --> [01c-bounded-context] --> [01d-data-model] --> [02-context] --> [03-container] --> [04-component] --> [05-document] --> [06-spec]
      STATUS            STATUS               STATUS                  STATUS              STATUS           STATUS              STATUS             STATUS            STATUS
```

Replace each `STATUS` with `COMPLETE` or `PENDING`.
