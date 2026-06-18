# Module Interface Patterns

Language-specific interface declarations per C4 component type.
Derive method signatures from `sequences-l3.md` interactions.
If sequences missing: generate skeleton from component name + type, mark `// TODO`.

---

## Go

### Repository Interface

```go
// {{EntityName}}Repository — [Repository] component
// Derives from: sequences showing DB read/write interactions
type {{EntityName}}Repository interface {
    Create(ctx context.Context, entity *{{EntityName}}) (*{{EntityName}}, error)
    GetByID(ctx context.Context, id string) (*{{EntityName}}, error)
    Update(ctx context.Context, entity *{{EntityName}}) (*{{EntityName}}, error)
    Delete(ctx context.Context, id string) error
    List(ctx context.Context, filter {{EntityName}}Filter) ([]*{{EntityName}}, error)
}

type {{EntityName}}Filter struct {
    // Derive fields from query patterns in sequences-l3
    Limit  int
    Offset int
}
```

### Service Interface

```go
// {{ContextName}}Service — [Service] component
// Derives from: sequences showing use-case orchestration
type {{ContextName}}Service interface {
    // Method names: derive from sequence diagram message labels
    // e.g., "OrderService.PlaceOrder(req)" → PlaceOrder
    Create{{EntityName}}(ctx context.Context, req *Create{{EntityName}}Req) (*{{EntityName}}, error)
    Get{{EntityName}}(ctx context.Context, id string) (*{{EntityName}}, error)
    Update{{EntityName}}(ctx context.Context, id string, req *Update{{EntityName}}Req) (*{{EntityName}}, error)
    Delete{{EntityName}}(ctx context.Context, id string) error
}

type Create{{EntityName}}Req struct {
    // Derive from Key Request Fields in contracts / sequence inputs
}

type Update{{EntityName}}Req struct {
    // Derive from Key Request Fields in contracts / sequence inputs
}
```

### Gateway Interface

```go
// {{ExternalSystem}}Gateway — [Gateway] component
// Wraps external contract from contracts.md
// Method signatures mirror the external API, translated to domain types
type {{ExternalSystem}}Gateway interface {
    // Derive method from Endpoint field in contract
    // Input/output types: domain types (not external API types — ACL boundary here)
    Send{{Action}}(ctx context.Context, req *{{Action}}Req) (*{{Action}}Res, error)
}

type {{Action}}Req struct {
    // Domain-side fields (not wire format)
}

type {{Action}}Res struct {
    // Domain-side fields
}
```

### Command/Query Handler (CQRS)

```go
// {{CommandName}}Handler — [Handler] component
type {{CommandName}}Handler interface {
    Handle(ctx context.Context, cmd {{CommandName}}) error
}

type {{CommandName}} struct {
    // Command fields — derive from sequence input
}

// {{QueryName}}Handler — [Handler] component
type {{QueryName}}Handler interface {
    Handle(ctx context.Context, query {{QueryName}}) (*{{QueryName}}Result, error)
}
```

### Message Consumer Interface

```go
// {{TopicName}}Consumer — [Consumer] component
// Derives from: events/topics in contracts.md
type {{TopicName}}Consumer interface {
    Consume(ctx context.Context, msg *{{MessageType}}) error
}

type {{MessageType}} struct {
    // Derive from Key Fields in contracts events section
    EventID   string
    OccuredAt time.Time
    Payload   json.RawMessage
}
```

---

## TypeScript

### Repository Interface

```typescript
// {{EntityName}}Repository — [Repository] component
export interface {{EntityName}}Repository {
  create(entity: Create{{EntityName}}Input): Promise<{{EntityName}}>;
  findById(id: string): Promise<{{EntityName}} | null>;
  update(id: string, entity: Update{{EntityName}}Input): Promise<{{EntityName}}>;
  delete(id: string): Promise<void>;
  findMany(filter: {{EntityName}}Filter): Promise<{{EntityName}}[]>;
}

export interface {{EntityName}}Filter {
  // Derive from query patterns in sequences-l3
  limit?: number;
  offset?: number;
}
```

### Service Interface

```typescript
// {{ContextName}}Service — [Service] component
export interface {{ContextName}}Service {
  create(input: Create{{EntityName}}Input): Promise<{{EntityName}}>;
  getById(id: string): Promise<{{EntityName}}>;
  update(id: string, input: Update{{EntityName}}Input): Promise<{{EntityName}}>;
  remove(id: string): Promise<void>;
}

export interface Create{{EntityName}}Input {
  // Derive from Key Request Fields
}

export interface Update{{EntityName}}Input {
  // Derive from Key Request Fields
}
```

### Gateway Interface

```typescript
// {{ExternalSystem}}Gateway — [Gateway] component
export interface {{ExternalSystem}}Gateway {
  send{{Action}}(request: {{Action}}Request): Promise<{{Action}}Response>;
}

export interface {{Action}}Request {
  // Domain-side fields
}

export interface {{Action}}Response {
  // Domain-side fields
}
```

### Event Consumer Interface

```typescript
// {{TopicName}}Consumer — [Consumer] component
export interface {{TopicName}}Consumer {
  consume(message: {{MessageType}}): Promise<void>;
}

export interface {{MessageType}} {
  eventId: string;
  occurredAt: Date;
  payload: Record<string, unknown>;
}
```

---

## Java

### Repository Interface

```java
// {{EntityName}}Repository — [Repository] component
public interface {{EntityName}}Repository {
    {{EntityName}} save({{EntityName}} entity);
    Optional<{{EntityName}}> findById(String id);
    {{EntityName}} update(String id, {{EntityName}} entity);
    void deleteById(String id);
    List<{{EntityName}}> findAll({{EntityName}}Filter filter);
}
```

### Service Interface

```java
// {{ContextName}}Service — [Service] component
public interface {{ContextName}}Service {
    {{EntityName}} create(Create{{EntityName}}Request request);
    {{EntityName}} getById(String id);
    {{EntityName}} update(String id, Update{{EntityName}}Request request);
    void delete(String id);
}
```

### Gateway Interface

```java
// {{ExternalSystem}}Gateway — [Gateway] component
public interface {{ExternalSystem}}Gateway {
    {{Action}}Response send{{Action}}({{Action}}Request request);
}
```

---

## Naming Conventions

| C4 Label | Go type name | TS name | Java name |
|----------|-------------|---------|-----------|
| `Order Repository` | `OrderRepository` | `OrderRepository` | `OrderRepository` |
| `Payment Gateway Adapter` | `PaymentGateway` (drop "Adapter") | `PaymentGateway` | `PaymentGateway` |
| `Order Service` | `OrderService` | `OrderService` | `OrderService` |
| `Notification Consumer` | `NotificationConsumer` | `NotificationConsumer` | `NotificationConsumer` |

Strip tech suffixes from C4 labels (e.g. "[Node.js]", "[PostgreSQL]") before deriving interface names.
