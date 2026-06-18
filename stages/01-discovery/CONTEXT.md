# Stage 01: Discovery

Gather structured information about the system by interviewing the user and parsing existing materials.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| System identity | `../../shared/system-meta.md` | Full file | Baseline from setup |
| Discovery guide | `references/discovery-guide.md` | Full file | Questions to ask and what to capture |

## Process

1. Read `shared/system-meta.md` to confirm what was captured during setup.
2. Read `references/discovery-guide.md` to load the full question set.
3. Ask the user discovery questions conversationally -- one topic at a time, not all at once.
4. If the user provides existing docs (PRD, README, API spec, diagrams), parse them and extract answers.
5. Pause after each topic to confirm the captured information before moving on.
6. Compile all gathered information into a structured discovery artifact.
7. Compile NFR and Technology Choices into the tech decisions log -- seed it with tech stack rationale and any constraints captured during discovery.
8. Save both artifacts to `output/`.

## Checkpoints

| After Step | Agent Presents | Human Decides |
|------------|---------------|---------------|
| Step 5 | Summary of each discovered topic | Correct, add, or flag gaps before the artifact is written |

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
| Tech decisions log | `output/{{SYSTEM_SLUG}}-tech-decisions.md` | Running ADR-style log -- appended by each subsequent stage |
