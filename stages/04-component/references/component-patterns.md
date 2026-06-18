# Component Patterns

Common internal structures for containers. Use as starting points, not rigid templates.

## Pattern: Layered API (Controller / Service / Repository)

```
HTTP Request
  -> [Controller] -- validates input, calls service
  -> [Service] -- business logic, calls repository and gateways
  -> [Repository] -- data access, maps domain <-> DB
  -> Database [PostgreSQL] (external to this component layer)
  -> [Gateway] -- wraps external API calls
  -> External System (external to this container)
```

When to use: standard CRUD APIs, REST services. Most common pattern.

## Pattern: CQRS (Command / Query Separation)

```
Write path: [Command Handler] -> [Domain Model] -> [Event Store]
Read path:  [Query Handler] -> [Read Model / Projection] -> [Read DB]
```

When to use: systems where read and write workloads have very different shapes or scale requirements.

## Pattern: Feature Modules (SPA)

```
Router
  -> [Auth Module]    -- login, session, token refresh
  -> [Product Module] -- listing, search, detail view
  -> [Cart Module]    -- add/remove items, calculate totals
  -> [Order Module]   -- checkout, confirmation, history
Each module: [Page Component] -> [Feature Component(s)] -> [API Client]
```

When to use: large SPAs organized by domain feature rather than layer.

## Pattern: Pipeline Worker

```
[Job Consumer] -- pulls from queue
  -> [Validator] -- checks job payload
  -> [Processor] -- core transformation or action
  -> [Notifier] -- emits result events or sends notification
  -> [Dead Letter Handler] -- handles failed jobs after retries
```

When to use: background workers, data processing pipelines, scheduled jobs.

## Pattern: Hexagonal (Ports and Adapters)

```
[Domain Core] -- pure business logic, no dependencies
  <- [Inbound Adapter: HTTP Controller]
  <- [Inbound Adapter: Message Consumer]
  -> [Outbound Port: Repository Interface]
       -> [Outbound Adapter: PostgreSQL Repository]
  -> [Outbound Port: Notification Port]
       -> [Outbound Adapter: Email Gateway]
```

When to use: when domain logic must be testable in isolation, or when adapters need to be swappable.

---

## Choosing a Pattern

Ask:
- Is there heavy business logic? -> Layered or Hexagonal
- Is there distinct read vs. write traffic? -> CQRS
- Is this a large SPA? -> Feature Modules
- Is this a worker processing jobs? -> Pipeline Worker
- Is there a simple CRUD need? -> Layered (simplified, no strict ports)
