# raw/

Drop existing materials here before running any stage. Run `raw route` -- Claude scans each file, decides which stage(s) it's most relevant to, and writes `MANIFEST.md`.

## What belongs here

| Type              | Examples                                                   |
| ----------------- | ---------------------------------------------------------- |
| Requirements docs | BRD, PRD, product brief, problem statement                 |
| System docs       | README, architecture doc, Confluence export, ADR log       |
| API specs         | OpenAPI/Swagger YAML, GraphQL schema, Postman collection   |
| Diagrams          | draw.io export, Miro screenshot, Lucidchart image          |
| App captures      | Screenshots, screen recordings, UI walkthroughs            |
| Process docs      | Business flow diagrams, swimlane charts, BPMN exports      |
| Data docs         | ERD, data dictionary, data flow diagrams                   |
| Constraints       | Tech radar, platform mandates, compliance requirements doc |

## Any format accepted

`.md`, `.txt`, `.pdf`, `.docx`, `.yaml`, `.json`, `.png`, `.jpg`, `.html` -- Claude reads what it can parse and notes what it cannot.

## Workflow

1. Drop files here
2. Trigger: `raw route`
3. Claude scans each file, determines relevant stage(s), writes `MANIFEST.md`
4. Each stage reads only the files routed to it via `MANIFEST.md`
