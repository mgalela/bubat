# C4 Level 3 Rules

## What is a Component

A component is a logical grouping of code within a single container. It is a named, addressable unit
that has a clear responsibility. Examples per container type:

**API Server:**
- Controller -- receives HTTP requests, validates input, delegates to services
- Service -- orchestrates business logic, calls repositories and external gateways
- Repository -- abstracts data access, translates between domain objects and DB queries
- Gateway -- wraps calls to external systems (payment provider, email service)
- Middleware -- cross-cutting concerns (auth, logging, rate limiting)

**Single Page App:**
- Page / View -- top-level routed screen component
- Feature Component -- self-contained UI feature (cart, product listing)
- API Client -- typed wrapper around backend API calls
- Store / State Module -- client-side state slice (Redux slice, Zustand store, Pinia module)

**Background Worker:**
- Job Handler -- handles one type of job message
- Scheduler -- determines when jobs run
- Notifier -- sends outcomes to other systems

## Scope Rule

A Level 3 diagram shows ONLY the internals of ONE container. The boundary of the diagram is that container.
Other containers and external systems can appear as external boxes that components interact with,
but their internals remain hidden.

## When Level 3 is Worth Building

Build Level 3 for containers that are:
- The most complex (most business logic, most relationships)
- Most frequently changed (high churn = high value for documentation)
- Least understood by the team (onboarding pain points)
- At the center of bugs or incidents

Skip Level 3 for containers that are:
- Simple passthrough proxies
- Standard data stores with no custom logic
- Small, well-understood utilities

## Component Naming

Use noun phrases that describe role, not implementation:
- "Order Service" not "OrderManager"
- "User Repository" not "UserDatabaseHelper"
- "Payment Gateway" not "StripeIntegration"

Type tags guide the reader on the pattern:
- [Controller], [Service], [Repository], [Gateway], [Middleware], [Facade], [Handler], [Factory]

## Relationship Depth at Level 3

Relationships between components should be specific. Avoid "uses":
- "delegates validation to" not "uses"
- "queries orders from" not "reads"
- "publishes event via" not "sends"
- "authenticates request via" not "calls"
