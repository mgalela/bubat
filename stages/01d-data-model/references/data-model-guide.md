# Domain Data Model Guide

Rules for extracting a conceptual entity model from bounded context aggregates at Stage 01d.

## From Aggregate to Entity

An aggregate from Stage 01c becomes a cluster of entities in the data model.

Steps:
1. The aggregate root becomes the primary entity. Its identity is the aggregate identity.
2. Objects that belong exclusively to the aggregate and cannot exist without it become child entities.
3. Objects with no independent lifecycle and no identity of their own become value objects.

Example:
- Aggregate: Order
  - Root entity: Order (has its own ID, full lifecycle — created, confirmed, shipped, cancelled)
  - Child entity: LineItem (exists only within an Order; no meaning outside the aggregate)
  - Value object: Money (amount + currency; no ID; immutable; replaced, never mutated)

## Identifying Attributes

Extract attributes from three sources:
1. **Ubiquitous language definitions** — fields implied by the term definitions in Stage 01c
2. **Domain events** — data implied by the event (e.g., `OrderPlaced` implies `Order.placedAt`, `Order.status`)
3. **Key scenarios** — data required to execute a scenario (e.g., "calculate total" needs `LineItem.unitPrice` and `LineItem.quantity`)

Attribute format:
- **name**: camelCase domain term (not a column name)
- **type**: String, Integer, Decimal, Boolean, UUID, DateTime, Enum, or a named value object
- **constraint**: required / optional / unique / positive / max-length / immutable

## Cardinality Rules

| Symbol | Meaning |
|--------|---------|
| `\|\|--\|\|` | exactly one to exactly one |
| `\|\|--o{` | exactly one to zero or more |
| `}o--o{` | zero or more to zero or more |

M:N relationships are valid at the conceptual level. Do not resolve them to junction tables here —
that is a schema design decision, deferred to implementation.

## Entities vs Value Objects

| Property | Entity | Value Object |
|---|---|---|
| Has identity | Yes — UUID or domain key | No |
| Can exist alone | Yes | No — always embedded in an entity |
| Mutable | Usually yes | No — replace, never mutate |
| Equality | By identity | By value (all fields equal) |
| Examples | Order, Customer, Product | Money, Address, DateRange, PhoneNumber |

## Cross-BC Data Rules

Data does not move freely across BC boundaries. When a scenario requires data from two BCs:
- One BC is **upstream** (owns and produces the data)
- The other BC receives a **projection** (a subset, possibly reshaped)
- The projection is not the same entity as the source — name it differently

Example:
- **Identity BC** owns: `User { userId, email, hashedPassword, roles }`
- **Order Management BC** uses: `CustomerRef { customerId, displayName }` — a projection, not the full User

Projections are owned by the consuming BC. The upstream BC publishes what it chooses to share.
The ACL flag in the context map signals that a translation layer is needed at the boundary.

## Storage Hint Selection

Choose based on aggregate structure and access patterns:

| Storage Type | Use When |
|---|---|
| **Relational** | Entities have strong relationships; transactions span multiple entities; ad-hoc structured queries needed |
| **Document** | Aggregate is stored and retrieved as a whole; schema varies across instances |
| **Key-Value** | Lookup by a single identifier; high throughput; flat or nested structure with no joins |
| **Graph** | Complex many-to-many traversals are the primary access pattern |
| **Time-Series** | Entities represent timestamped measurements appended sequentially; range queries by time |

Storage hints are recommendations, not final decisions. The container stage (Stage 03) confirms the technology.
