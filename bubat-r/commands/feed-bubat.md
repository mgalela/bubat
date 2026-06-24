# bubat-r feed bubat

Prepare reconstruction outputs as BUBAT inputs.

## Intent

```text
bubat-r feed bubat [target-path]
```

## Protocol

1. Verify `reconstruction/11-reference-design.md` exists.
2. Verify `reconstruction/02-coverage-ledger.md` exists.
3. Verify `reconstruction/12-drift-ambiguity-report.md` exists.
4. Register reconstruction folder as raw source for BUBAT.
5. Route artifacts to BUBAT stages.

## Mapping

| BUBAT-R Artifact | BUBAT Stage |
|---|---|
| evidence catalog | 01-discovery |
| behavior spine | 01b-flow |
| ownership map | 01c / 01d |
| domain map | 01c |
| runtime map | 02 / 03 |
| contract map | 03 |
| component map | 04 |
| code trace map | 04 |
| reference design | 01–04 seed |
| drift report | gates/update notes |
