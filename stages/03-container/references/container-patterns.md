# Container Patterns

Common topologies to recognize and reference when building Level 2 diagrams.

## Pattern: Classic Web Three-Tier

```
User -> Single Page App [React] -> API Server [Node.js] -> Database [PostgreSQL]
```

Use when: a browser-based app with a REST or GraphQL API and a relational database.
Variants: add a cache (Redis) between API and database for read-heavy workloads.

## Pattern: Mobile + API

```
Mobile App [iOS/Android] -> API Server [Java Spring] -> Database [MySQL]
                                                     -> Object Store [S3]
```

Use when: mobile clients as the primary interface. Object store common for media.

## Pattern: Async Worker

```
API Server -> Message Queue [RabbitMQ] -> Background Worker [Python]
                                                    -> Database
                                                    -> Email Service [External]
```

Use when: long-running tasks (email sending, report generation, image processing) are offloaded.

## Pattern: Event-Driven Microservices

```
API Gateway -> Service A -> Event Bus [Kafka] -> Service B
                                              -> Service C
Each service has its own database (Database per Service pattern).
```

Use when: independently deployable services with loose coupling via events.

## Pattern: BFF (Backend for Frontend)

```
Web App -> Web BFF [Node.js] -> Downstream Services
Mobile App -> Mobile BFF [Go] -> Downstream Services
```

Use when: different client types need different API shapes from the same underlying services.

## Pattern: Static Site + Serverless

```
User -> CDN [CloudFront] -> Static Site [Next.js]
User -> CDN -> API Functions [Lambda] -> Database [DynamoDB]
```

Use when: serverless or JAMstack architecture where there is no always-on server process.

---

## Checklist When Choosing Topology

- Is there a real-time communication requirement? Consider WebSocket container.
- Is there a scheduled job? It is a container (cron or worker).
- Is there a third-party auth provider? It appears as an external system, not a container.
- Is there a shared cache? It is a container between the API and database.
- Is there a search index? It is a container (Elasticsearch, Algolia, etc.).
