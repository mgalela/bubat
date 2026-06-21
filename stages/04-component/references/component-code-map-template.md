# Component Code Map Template

Use this artifact in Stage 04 output as:
`output/{{SYSTEM_SLUG}}-component-code-map.md`

## Purpose

Map each Stage 04 component to concrete implementation location in codebase.
Supports 2 source modes:
- `discovery` — existing project code inspected under `project_path`
- `generated` — code generated after design; Stage 04 re-run/update refreshes map

If implementation not found yet, keep row and mark:
- `File Path` = `[MISSING — implementation not yet generated]`
- `Line Span` = `[MISSING]`
- `Source Mode` = `generated`
- `Confidence` = `planned`

## Required Columns

| Container | Component | Type | File Path | Symbol | Line Span | Source Mode | Confidence | Notes |
|-----------|-----------|------|-----------|--------|-----------|-------------|------------|-------|
| [Container Name] | [Component Name] | [Controller/Service/Repository/Gateway/Worker/etc.] | `src/...` | `ClassName` / `functionName` / `module` | `L10-L84` | discovery / generated | high / medium / low / planned | [Why mapped here, ambiguity, alt files, TODO] |

## Rules

1. One row per component implementation location.
   - If component spans multiple files, use multiple rows.
2. `Component` name must match Stage 04 diagram label exactly.
3. `Type` should match component tag from Level 3 diagram.
4. `File Path` should be repo-relative when possible.
5. `Line Span` should be exact when resolvable.
   - If exact span not resolvable, use best-known range or `[MISSING]` and explain in `Notes`.
6. `Symbol` may be class, function, exported object, module name, or package path.
7. `Confidence` values:
   - `high` = exact file + exact symbol verified
   - `medium` = file verified, symbol/span inferred
   - `low` = likely mapping, needs confirmation
   - `planned` = implementation not present yet
8. Keep missing rows. Do not delete component because code missing.
9. If generated code later changes file locations, refresh rows on Stage 04 update.

## Example

| Container | Component | Type | File Path | Symbol | Line Span | Source Mode | Confidence | Notes |
|-----------|-----------|------|-----------|--------|-----------|-------------|------------|-------|
| Orders API | Order Controller | Controller | `apps/orders-api/src/controllers/order.controller.ts` | `OrderController` | `L12-L88` | discovery | high | Handles HTTP order endpoints |
| Orders API | Order Service | Service | `apps/orders-api/src/services/order.service.ts` | `OrderService` | `L8-L142` | discovery | high | Core orchestration |
| Orders API | Payment Gateway | Gateway | `apps/orders-api/src/integrations/payment.gateway.ts` | `PaymentGateway` | `L5-L77` | discovery | medium | Span inferred from exported class + helper fn below |
| Orders API | Fraud Policy | Service | `[MISSING — implementation not yet generated]` | `[MISSING]` | `[MISSING]` | generated | planned | Planned in design; refresh after codegen |
