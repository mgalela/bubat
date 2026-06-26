# Contract Map

Project: `[PROJECT]`  
Date: `[YYYY-MM-DD]`

## Contract Inventory

| Contract | Type | Producer | Consumer | Schema/Source | Versioning | Break Risk | Evidence |
|---|---|---|---|---|---|---|---|
| `[contract]` | REST/GraphQL/RPC/event/webhook/DB/file/auth/config | `[producer]` | `[consumer]` | `path:line` | Unknown | High/Medium/Low | `path:line` |

## API / RPC Contracts

| Endpoint/Method | Runtime Unit | Request | Response | Auth | Evidence | Status |
|---|---|---|---|---|---|---|
| `[method path]` | `[unit]` | `[schema]` | `[schema]` | `[auth]` | `path:line` | Unknown |

## Event / Message Contracts

| Event/Topic | Producer | Consumers | Payload Evidence | Delivery Semantics | Status |
|---|---|---|---|---|---|
| `[event]` | `[producer]` | `[consumers]` | `path:line` | Unknown | Unknown |

## Shared DB / File Contracts

| Shared Surface | Writers | Readers | Coupling Risk | Evidence |
|---|---|---|---|---|
| `[table/file]` | `[writers]` | `[readers]` | High/Medium/Low | `path:line` |

## Auth / Config Contracts

| Contract | Used By | Meaning | Evidence | Risk |
|---|---|---|---|---|
| `[claim/env/flag]` | `[consumer]` | `[meaning]` | `path:line` | `[risk]` |
