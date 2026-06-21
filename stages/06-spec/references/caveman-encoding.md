# Caveman Encoding Rules

Apply to prose in `SPEC.md` only. Do not apply to OpenAPI, proto, or language interface files.

| Rule | Before | After |
|------|--------|-------|
| Drop articles | the system must validate | system ! validate |
| Drop filler | basically just sends | sends |
| Fragments OK | This requires authentication | ! auth |
| Short symbols | leads to | `→` |
| Must | must | `!` |
| Forbidden | never / must not | `⊥` |
| For all | for all | `∀` |
| At most | at most | `≤` |
| At least | at least | `≥` |

Use pipe tables over prose lists. Keep technical terms, proper nouns, versions, URLs, field names, status codes.
