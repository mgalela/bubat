# BDD Feature Template

Gherkin structure for Stage 08 BDD feature file output.
One Feature block per key scenario. Steps use domain language only — no container/component/tech names.

## Structure

```gherkin
Feature: {{scenario name from 01b-flow scenarios.md}}
  As a {{user role}}
  I want to {{primary action from scenario}}
  So that {{business outcome / value}}

  Background:
    Given {{shared precondition 1 across all scenarios in this feature}}
    And {{shared precondition 2}}

  Scenario: {{happy path name}}
    Given {{specific precondition for this path}}
    When {{actor performs action}}
    Then {{observable outcome 1}}
    And {{observable outcome 2}}

  Scenario: {{failure path name}}
    Given {{precondition leading to failure}}
    When {{actor performs action}}
    Then {{observable failure outcome}}
    And {{system recovery or error message observable to actor}}

  Scenario Outline: {{parameterized scenario name}} (use when same flow applies to multiple input sets)
    Given {{precondition with <param>}}
    When {{action with <param>}}
    Then {{outcome with <expected>}}

    Examples:
      | param | expected |
      | {{value1}} | {{outcome1}} |
      | {{value2}} | {{outcome2}} |
```

## Naming Rules

| Element | Rule |
|---------|------|
| Feature name | = key scenario name from `scenarios.md`. No abbreviation. |
| Scenario name | Describes the path, not the test ("User completes checkout" not "Test checkout") |
| Given | State, not action. Past tense or present state. "a user is logged in" not "a user logs in" |
| When | Single actor action. One When per scenario. |
| Then | Observable system output. From actor's perspective only. |
| And / But | Extends previous Given/When/Then. Never starts a scenario block. |

## Domain Language Rules

- Use ubiquitous language terms from `01c-bounded-context` output.
- Use user role names from `01-discovery` output.
- No container names (e.g., "API Gateway", "Order Service").
- No component names (e.g., "OrderRepository", "PaymentGateway").
- No tech terms (e.g., "HTTP 200", "PostgreSQL row", "Kafka topic").

**Allowed:** "the order is confirmed", "the user receives a receipt", "the payment is rejected"
**Not allowed:** "the OrderService returns 200", "a row is inserted into orders table"

## §V Coverage within BDD

When a §V invariant maps to BDD, append a Scenario that directly tests it:

```gherkin
  # §V.{{N}} — {{invariant source}}
  Scenario: {{invariant as scenario name}}
    Given {{precondition that makes invariant testable}}
    When {{action that triggers invariant check}}
    Then {{the invariant condition is satisfied / violated and handled}}
```

Include `# §V.N` comment above the Scenario to maintain traceability to coverage matrix.

## File Layout

Output is one `.md` file containing all Feature blocks, separated by horizontal rule.

```markdown
# {{SYSTEM_SLUG}}-bdd-features.md

## Feature: {{Scenario Name 1}}

```gherkin
Feature: {{Scenario Name 1}}
  ...
```

---

## Feature: {{Scenario Name 2}}

```gherkin
Feature: {{Scenario Name 2}}
  ...
```
```

Each Feature section has its own `##` heading to allow direct navigation.
```
