# Stage 01: Discovery

Gather structured information about the system by interviewing the user and parsing existing materials.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| System identity | `../../shared/system-meta.md` | Full file | Baseline from setup |
| Discovery guide | `references/discovery-guide.md` | Full file | Questions to ask and what to capture |
| ADR template | `references/adr-template.md` | Full file | Format for every entry in the tech decisions log |
| Raw materials | `../../raw/` | Files routed to this stage | Pre-existing docs parsed during `raw route` -- only read rows in `raw/MANIFEST.md` where `Stages` contains `01-discovery` |
| Graphify output (conditional) | `<project_path>/graphify-out/` | `GRAPH_REPORT.md` + `graph.json` | Auto-detected if graphify was run on the project -- see Step 0 and `references/graphify-guide.md` |

## Stage Gate

Before running this stage, apply relevant checks from `../../shared/stage-gates.md`: input gate before work starts; stage audit, placeholder, and traceability gates before saving outputs.

## Process

### Step 0 — Graphify detection (run before anything else)

Read `project_path` from `../../shared/system-meta.md`. If set and not "Not provided":

1. Check for `<project_path>/graphify-out/GRAPH_REPORT.md` and `<project_path>/graphify-out/graph.json`.
2. If both exist: load them as reference material. Read `references/graphify-guide.md` for interpretation rules. Log: `"Graphify output detected at <project_path>/graphify-out/ — used as discovery reference."`
3. If missing: skip silently. Do not prompt the user to run graphify.

Graphify pre-fills are treated the same as raw material pre-fills — every extracted fact must carry `Source: graphify-out/GRAPH_REPORT.md` or `Source: graphify-out/graph.json`.

### Steps 1–9

1. Read `shared/system-meta.md` to confirm what was captured during setup.
2. Read `references/discovery-guide.md` to load the full question set.
3. Check `../../raw/MANIFEST.md` for rows where `Stages` contains `01-discovery`. If any exist, parse them and extract answers that map to discovery topics. Note the source file for every pre-filled answer.
4. If graphify output or raw materials were parsed, present a summary of pre-filled topics and remaining gaps -- confirm with the user before proceeding.
5. Ask the user only about topics not already covered -- one topic at a time, not all at once.
6. Pause after each topic to confirm the captured information before moving on.
7. Compile all gathered information into a structured discovery artifact. For answers sourced from graphify or raw materials, include a `Source` note referencing the file.
8. Compile NFR and Technology Choices into the tech decisions log -- seed it with tech stack rationale and any constraints captured during discovery. Use the format in `references/adr-template.md` for every entry; seed the file with the header defined there.
9. Save both artifacts to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 0 | Whether graphify output was found; what it pre-fills and what it flags as ambiguous | Confirm detection, override misreads, or note graphify output is stale |
| Step 4 | Summary of what graphify + raw materials pre-filled and what gaps remain | Confirm pre-fills, correct misreads, or flag additional raw docs |
| Step 6 | Summary of each conversationally discovered topic | Correct, add, or flag gaps before the artifact is written |

## Audit

| Check | Pass Condition |
|-------|---------------|
| System boundary defined | Clear inside-vs-outside line for the system |
| All users identified | At least one person element with role and description |
| External dependencies listed | Every external system named with relationship direction |
| No ambiguous elements | Each element is clearly Person, System, or external dependency |
| NFR captured | At least availability, scale, and security attributes have a stated requirement or explicit "not yet defined" |
| Tech stack rationale | Every technology in system-meta.md has a Why entry in tech-decisions log |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Discovery report | `output/{{SYSTEM_SLUG}}-discovery.md` | Structured markdown with sections per topic |
| Tech decisions log | `output/{{SYSTEM_SLUG}}-tech-decisions.md` | ADR log using format from `references/adr-template.md` -- appended by each subsequent stage |
