# BUBAT Setup

Ask all questions in one pass. Collect all answers before making any changes.
After the user answers, populate `shared/system-meta.md` with their responses.
Then confirm: "Setup complete. Run `status` to check where you are in the pipeline."

---

## Questions

1. What is the name of the software system you want to document?
   - Default: "My System"
   - Derived: system slug = lowercase-with-hyphens version of the name

2. Describe the system in one sentence. What problem does it solve and for whom?
   - Example: "An online retail platform that lets customers browse and purchase products."

3. Who are the primary users of this system? List up to 3 user types with a one-sentence description each. (Preview -- Stage 01 will explore in full depth.)
   - Example: "Customer -- a person who browses and buys products. Admin -- internal staff who manage inventory."
   - Default: Not yet known

4. What external systems does this system interact with? List name and relationship (sends/receives/both). (Preview -- Stage 01 will explore in full depth.)
   - Example: "Payment Gateway (sends payment requests), Email Service (sends notifications), CRM (both)"
   - Default: None known yet

5. What is the primary technology stack? (Languages, frameworks, databases, cloud provider)
   - Example: "Node.js, React, PostgreSQL, AWS"
   - Default: Not yet defined

6. What diagram format do you prefer for output?
   - Options: Mermaid (default, renders in GitHub/GitLab/Notion), Structurizr DSL (official C4 tool), PlantUML C4
   - Default: Mermaid

7. Who is the intended audience for this architecture document?
   - Options: Internal engineering team, new engineers onboarding, external stakeholders, all of the above
   - Default: Internal engineering team

---

## After Collecting Answers

Populate `shared/system-meta.md` by replacing all {{PLACEHOLDERS}} with the user's answers.
Do not ask clarifying questions mid-setup. If an answer is vague, record it as-is and note it is provisional.
