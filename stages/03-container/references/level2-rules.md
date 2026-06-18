# C4 Level 2 Rules

## What is a Container

A container is a separately runnable or deployable unit. It is not a Docker container specifically --
the C4 term predates container technology. Examples:

- A web application (rendered in a browser or a mobile device)
- A server-side API or application
- A database (relational, document, graph, key-value)
- A message queue or event bus
- A background worker or cron job
- A file store or blob storage
- A mobile app or desktop app

## What is NOT a Container

- A class, module, or package inside an application -- those are components (Level 3)
- A cloud service that wraps infrastructure (load balancer, CDN) -- these are usually omitted unless they carry significant routing logic
- A third-party library linked into an application -- the application itself is the container

## System Boundary

The system boundary from Level 1 becomes the diagram boundary at Level 2. External systems still appear
but as external boxes outside the boundary. People (users) can appear at Level 2 to show which containers
they interact with directly.

## Technology Tags

Every container label must include a technology tag in brackets.
- "Single Page App [React]" not "Frontend"
- "API Server [Node.js / Express]" not "Backend"
- "User Database [PostgreSQL]" not "Database"
- "Message Queue [RabbitMQ]" not "Queue"

## Relationship Labels at Level 2

Relationships between containers should specify the protocol or technology when known.
- "reads/writes user records [SQL over TCP]"
- "publishes order events [AMQP]"
- "calls REST API [HTTPS/JSON]"
- "streams video [WebRTC]"

## Narrative Section

After the diagram, write one paragraph (4-6 sentences):
1. State the total number of containers and their broad categories (frontend, backend, data)
2. Describe the primary request flow (user -> X -> Y -> Z)
3. Name the data persistence layer and what it stores
4. Mention any async or event-driven paths if they exist

## What to Do with Complex Systems

If the system has more than 12 containers, consider:
1. Grouping related containers under a named boundary within the diagram
2. Splitting into multiple Level 2 diagrams by functional area (e.g., "Auth subsystem", "Payment subsystem")
3. Note which containers will get Level 3 treatment in Stage 04
