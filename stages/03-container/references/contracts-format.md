# Interface Contracts Format

Rules and format for the `{slug}-contracts.md` artifact produced at Stage 03.

## What an Interface Contract Covers

A contract defines the agreement between two containers (or a container and an external system)
across a single relationship. It answers:
- What protocol or transport is used?
- What is the data format?
- What are the key fields in the payload?
- What happens on error?

## Contract Entry Format

```markdown
## [Consumer] → [Producer]

| Field | Value |
|-------|-------|
| Protocol | HTTPS / AMQP / gRPC / WebSocket / SQL / etc. |
| Format | JSON / Protobuf / Avro / XML / binary |
| Direction | Synchronous (request/response) / Asynchronous (fire-and-forget / event) |
| Context Map Relationship | Customer-Supplier / Conformist / ACL / Shared Kernel / OHS+PL / Partnership |
| ACL Required | Yes / No -- if Yes, name the adapter container that owns the translation |
| Endpoint / Topic | `/api/orders` or `order.created` topic |
| Key Request Fields | field: type -- description |
| Key Response Fields | field: type -- description |
| Error Handling | HTTP 4xx/5xx codes, DLQ strategy, retry policy |
| Auth | Bearer token / API key / mTLS / none |
| SLA / Timeout | Expected response time or message delivery SLA |
| Notes | Any versioning, deprecation, or migration notes |
```

## Example

```markdown
## Payment Gateway Adapter → Payment Gateway [External]

| Field | Value |
|-------|-------|
| Protocol | HTTPS |
| Format | JSON |
| Direction | Synchronous (request/response) |
| Context Map Relationship | ACL |
| ACL Required | Yes -- Payment Gateway Adapter [Node.js] translates between internal Payment domain model and gateway's Charge/Transaction model |
| Endpoint | `POST https://pay.example.com/v1/charge` |
| Key Request Fields | `amount: integer` -- charge in cents; `currency: string`; `card_token: string` |
| Key Response Fields | `charge_id: string`; `status: succeeded\|failed`; `error_code: string?` |
| Error Handling | HTTP 402 = payment declined (retryable with new token); HTTP 5xx = retry with backoff |
| Auth | API key in `Authorization` header |
| SLA / Timeout | 5s timeout; 3 retries with exponential backoff |
| Notes | Use API v1; v2 in beta, not yet stable |
```

## Scope

- One entry per directed relationship in the Level 2 diagram.
- Bidirectional relationships get two entries (one each direction).
- If a contract is unknown at the time of diagramming, mark fields as `TBD` and add to Open Questions.
- Do not capture internal method signatures here -- this is container-boundary only.
