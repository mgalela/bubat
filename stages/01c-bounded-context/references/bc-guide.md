# Bounded Context Identification Guide

Questions and rules for identifying bounded contexts from business flows at Stage 01c.

## What is a Bounded Context

A bounded context is a section of the domain where a specific model applies and a ubiquitous language
is consistent. Inside one BC, every term has exactly one meaning. The same word in a different BC may
mean something entirely different -- that divergence is what marks the boundary.

Examples:
- "Account" in Banking means a financial account with a balance. "Account" in IAM means login credentials.
  Two BCs.
- "Order" in Checkout means a cart being purchased. "Order" in Fulfillment means a package to ship.
  Two BCs, even if the data overlaps.

## Step 1: Extract Domain Language from Flows

For each flow in `{slug}-flows.md`:
- List every domain noun (things): Customer, Order, Invoice, Product, Shipment, Policy, Claim, ...
- List every domain verb (actions): place, approve, dispatch, cancel, settle, renew, ...
- Note which actor (user role or external system) performs each action.

## Step 2: Cluster by Language Coherence

Group nouns and verbs that co-occur consistently across flows. A cluster where the same terms appear
together and mean the same thing is a BC candidate.

Questions to ask:
- Do these terms always appear together in the same flows?
- When a term appears in a different cluster, does it mean the same thing?
- Could a domain expert from cluster A and a domain expert from cluster B disagree on the definition
  of a shared term?

If yes to the last question: that term sits on a BC boundary.

## Step 3: Name the Bounded Context

Rules for BC names:
- Use domain language, not technology: "Order Management" not "Order Service"
- Name from the perspective of what happens there: "Identity & Access" not "Login Module"
- Avoid generic names: "Core", "Common", "Shared", "Utils" are not BC names
- One or two words is ideal; three is acceptable

## Step 4: Define Ubiquitous Language per BC

For each BC, list 5-10 terms with one-line definitions as used *within that BC only*.

```markdown
**Order Management BC**
- Order: a confirmed purchase intent from a customer, containing line items and a total
- Line Item: one product SKU with quantity and unit price within an Order
- Fulfillment Request: an instruction sent to the warehouse to pack and ship an Order
```

## Step 5: Identify Owned Aggregates

An aggregate is a cluster of domain objects that change together and are always consistent together.
It has one root entity that controls access.

For each BC, ask:
- What is the main "thing" this BC manages throughout its lifecycle?
- What other objects always exist in relation to it and cannot stand alone?

Example: Order is an aggregate root. LineItem cannot exist without Order. They change together.

## Step 6: Identify Primary Domain Events

Domain events are things that happened in the domain that other BCs care about.
They flow outward from a BC via the context map.

Questions to ask per BC:
- What does this BC announce when something significant happens?
- What do other BCs need to know about?

Format: past tense, domain language. "OrderPlaced", "PaymentSettled", "ShipmentDispatched".

## Recognising Over-Partitioning

Signs that BCs are too fine-grained:
- A BC has only one aggregate
- A BC never produces domain events
- Two BCs always change together and share the same ubiquitous language
- The team boundary maps multiple small BCs to the same team

Merge candidates before mapping relationships.

## External Systems as External BCs

Every external system from discovery is treated as an external BC for context mapping purposes.
It has its own model, its own language, and its own ownership.
The relationship type (ACL, Conformist, etc.) applies to the integration point.
