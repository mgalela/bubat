# Interface Generation Rules

Rules for deciding which interface spec formats to generate at Stage 06.
Read `system-meta.md` first, then apply these rules.

## Format Decision Table

| Condition | Generate |
|-----------|---------|
| Any contract has `Protocol: HTTPS` or `Protocol: HTTP` | `output/openapi.yaml` |
| Any contract has `Protocol: gRPC` | `output/{slug}.proto` |
| Tech stack contains Go / Golang | Go interfaces in `output/{slug}-interfaces.go` |
| Tech stack contains TypeScript / Node.js | TypeScript interfaces in `output/{slug}-interfaces.ts` |
| Tech stack contains Java / Kotlin | Java interfaces in `output/{slug}-interfaces.java` |
| `{{INTERFACE_FORMATS}}` explicitly set in system-meta | Override all above — generate only listed formats |

Multiple formats may apply. Generate all that match.

## Source Mapping

| Interface Type | Primary Source | Secondary Source |
|---------------|----------------|-----------------|
| OpenAPI paths | `03-container/output/{slug}-contracts.md` (HTTP rows) | `04-component/output/{slug}-sequences-l3.md` (request/response shape) |
| proto services | `03-container/output/{slug}-contracts.md` (gRPC rows) | `04-component/output/{slug}-components.md` (component names for service names) |
| Language interfaces | `04-component/output/{slug}-components.md` (component types) | `04-component/output/{slug}-sequences-l3.md` (method interactions) |

## Extraction Rules per Source

### From contracts.md → OpenAPI

For each row where `Protocol` = HTTPS/HTTP:
- `Endpoint / Topic` → path + method
- `Key Request Fields` → requestBody schema properties
- `Key Response Fields` → response schema properties
- `Auth` → security scheme reference
- `Error Handling` (HTTP codes) → responses object entries
- `SLA / Timeout` → x-sla extension field

### From contracts.md → proto

For each row where `Protocol` = gRPC:
- `[Consumer] → [Producer]` → service name = Producer name (CamelCase)
- `Endpoint / Topic` → rpc method name
- `Key Request Fields` → request message fields
- `Key Response Fields` → response message fields
- `Error Handling` → use `google.rpc.Status` if error detail needed
- `Format: Protobuf` → confirm; if `Format: JSON` over gRPC, note it

### From components.md + sequences-l3.md → Language Interfaces

For each component in a selected container:
- Component type tag determines interface type:

| C4 Type Tag | Interface Kind |
|-------------|---------------|
| `[Repository]` | Data access interface — CRUD + query methods |
| `[Service]` | Business logic interface — use-case methods |
| `[Gateway]` | External call interface — wraps third-party contract |
| `[Controller]` | Usually not interfaced (entry point); skip unless hexagonal pattern |
| `[Handler]` | Command/query handler interface |
| `[Consumer]` | Message consumer interface |

- Method names: derive from sequence diagram interactions. "calls OrderService.createOrder()" → `CreateOrder(ctx, req) (res, error)`
- If sequences-l3 is missing for a container: generate skeleton methods from component name + type only, mark as `// TODO: derive from sequences`

## Completeness Check

Before saving generated artifacts:
1. Every HTTP contract row has ≥1 OpenAPI path entry.
2. Every gRPC contract row has ≥1 proto rpc entry.
3. Every component in a Level 3 diagram has ≥1 interface declaration (if language target applies).
4. No contract row is silently skipped — if data is insufficient, add `# TODO: insufficient data — [field name] missing` comment in output.
