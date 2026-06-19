# Component Patterns

Common internal structures for containers. Use as starting points, not rigid templates.

## Step 0: Cross-Check Stage 01 Pattern Signals

Before declaring a pattern for any container, read the "Pattern Signals" section of `{slug}-discovery.md`. Map signals to patterns:

| Stage 01 Signal | Recommended Pattern |
|---|---|
| Heavy business logic, domain complexity | Hexagonal — protects domain from infrastructure |
| Read/write ratio >10:1 or distinct latency SLAs | CQRS |
| Long-running jobs, queue-based processing | Pipeline Worker |
| Standard CRUD, simple business rules | Layered |
| Large SPA organized by domain area | Feature Modules |
| Swappable external integrations or compliance isolation | Hexagonal |

If no Pattern Signals exist from Stage 01, default to **Layered** and record it as a default in the component-scope artifact, not an ADR.

## ADR Triggers at Stage 04

Write an ADR when:
- A non-default pattern is chosen (anything other than Layered for a standard API, or Feature Modules for a standard SPA)
- CQRS is introduced — read/write model split is a team-wide commitment affecting data strategy
- Hexagonal is chosen — implies explicit port/adapter discipline across the codebase
- Pattern choices are inconsistent across containers — explain why different containers use different patterns

Do NOT write an ADR for:
- Layered on a standard CRUD container (expected default — note in component-scope artifact only)
- Feature Modules on a standard SPA (expected default)

---

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

---

## GoF Design Patterns

GoF patterns operate **below** C4 Level 3 — they describe class-level collaboration, not component structure. At Stage 04, identify GoF patterns that are architecturally significant: ones that affect component boundaries, team conventions, or testability. Document them in the component narrative and tech decisions log, not in the C4 diagram itself.

Reference: https://refactoring.guru/design-patterns/catalog

### Mapping: Component Pattern → Relevant GoF Patterns

| Component Pattern | GoF Patterns Commonly Used | Where They Appear |
|---|---|---|
| **Layered** | Facade (Service over domain), Repository (data access), Strategy (swappable rules), Decorator (cross-cutting: logging, caching), Template Method (base service steps) | Service and Repository layers |
| **Hexagonal** | Adapter (each outbound adapter), Strategy (multiple adapters per port), Factory / Abstract Factory (adapter instantiation), Proxy (caching/logging at port boundary) | Outbound adapters and port implementations |
| **CQRS** | Command (write operations as objects), Mediator (command bus dispatch), Observer (write→read model propagation), Builder (complex command/query construction) | Command handlers, event propagation |
| **Pipeline Worker** | Chain of Responsibility (processing steps as linked handlers), Template Method (base job class with override points), Strategy (swappable processors), Decorator (retry/logging per step) | Validator, Processor, Notifier steps |
| **Feature Modules (SPA)** | Observer / Reactive (state propagation via RxJS, Signals), Facade (module's public API surface), Mediator (cross-module comms via shared bus), Factory (dynamic component creation) | Module boundaries, shared services |

### Signal-Based GoF Selection

| If you need this... | Use this GoF pattern |
|---|---|
| Swappable algorithm or business rule variant | **Strategy** |
| Decoupled event or state propagation | **Observer** |
| Complex object construction with many optional parts | **Builder** |
| Wrap legacy system or external API behind a clean interface | **Adapter** |
| Simplify a complex subsystem to a single entry point | **Facade** |
| Add cross-cutting behaviour (logging, caching, retry) without subclassing | **Decorator** |
| Control creation of objects whose type varies at runtime | **Factory Method** / **Abstract Factory** |
| Step-by-step pipeline where each step can pass or stop | **Chain of Responsibility** |
| Encapsulate an operation as a first-class object | **Command** |
| Decouple many senders from many receivers through a hub | **Mediator** |

### GoF ADR Triggers

Write an ADR when:
- **Strategy** is chosen for core business rule dispatch — systemic, affects how team extends behaviour
- **Observer** / event mechanism is introduced — affects data consistency reasoning across components
- **Mediator** is used as a command bus — architectural commitment, not just an implementation detail
- **Singleton** is used deliberately — almost always a smell; if intentional, document why
- **Abstract Factory** is used to manage adapter variants in Hexagonal — documents the adapter contract

Do NOT write an ADR for:
- Repository pattern in Layered (expected)
- Facade over a service layer (expected)
- Observer in a standard reactive SPA (expected)
- Template Method in a base class (implementation detail)
