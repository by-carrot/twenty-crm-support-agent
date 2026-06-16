# Project Handoff Brief: CRM Support Specialist

## Context for Claude Code

This is a new project, starting from scratch. The design and architecture decisions below were worked out in a separate planning conversation and should be treated as settled decisions, not open questions, unless something concrete discovered during implementation gives a real reason to revisit them.

The person you are working with (John) is comfortable with analytics Python (pandas, scipy, statsmodels) but new to application development, deployment, and production engineering. He is on Windows and learns by building rather than by reading documentation in isolation. Walk through terminal commands one at a time and explain what each one does before running it. He is also rusty on Python generally, so do not assume familiarity with newer syntax or libraries without a brief explanation.

A previous project, "experiment-auditor," is live at github.com/by-carrot/experiment-auditor and follows specific GitHub conventions that should be followed here too: Conventional Commits format (feat:, fix:, test:, docs:, refactor:, chore:), pushing in logical stages rather than one large dump, a README structured as a decision log (problem, architecture and design decisions with alternatives considered, how to run, tests, project structure, evaluation results), and 5 to 8 topic tags on the repo.

---

## Project Summary

This project builds a RAG based support specialist chatbot for end users of Twenty, an open source CRM (https://github.com/twentyhq/twenty, docs at docs.twenty.com). The chatbot answers user questions about how to operate and configure the CRM (e.g. "where is this field," "how do I set this up," "what's the right format for this") by retrieving relevant sections from Twenty's documentation and generating a grounded answer. The goal is for users to get a correct answer in under a minute instead of filing a support ticket and waiting.

When the system cannot confidently answer from documentation, it escalates to a human with a structured handoff package, distinguishing between two escalation types (defined below).

## Architecture Decisions (Settled)

**Retrieval over keyword search:** Chosen because users often do not know the product's terminology for the feature they're looking for. Semantic retrieval can match a user's own phrasing to documentation that uses different words for the same concept. (Real example found during research: a Twenty community member searched for "formula" related terms but didn't think to search "computed," missing a relevant discussion that used that term.)

**Escalation taxonomy (two types):**
- **Type 1, Documentation Gap:** No relevant documentation was retrieved for the question. Likely the product works fine but the docs don't cover this. Lower urgency, useful signal for documentation maintainers.
- **Type 2, Documentation Mismatch:** Relevant documentation was retrieved and addresses the question, but the user's described behavior doesn't match what the docs say should happen. Possible bug signal. Higher urgency, useful for a technical/support engineering queue.
These are kept separate because they're owned by different people and the distinction costs little to compute (it falls out of comparing retrieved docs against the user's described behavior).

**Evaluation metric (the key differentiator):** The industry standard metric for AI support agents (Intercom Fin, Zendesk AI agents) is "resolution rate," generally defined as the percentage of conversations that end without escalation to a human. Both major vendors have had to retrofit additional verification specifically because this metric lets through cases where the user gave up rather than got helped (Zendesk added an LLM verification step; Intercom evolved from "resolutions" to "outcomes"). This project builds that verification in from the start as the *primary* metric: for each non-escalated conversation, a separate judgment pass asks "given the user's question and the system's answer, would a reasonable person be able to complete the task they described using only this answer?" This is explicitly a proxy for real user behavior, and that limitation should be stated plainly, not glossed over.

## Knowledge Base Scope

Source: Twenty CRM documentation (docs.twenty.com), specifically the User Guide sections on Data Model (objects, fields, table views, relation fields, data model FAQ, and the how-to pages for creating custom objects/fields/relations) and Workflows. This is a self-contained subset that maps directly onto "how do I configure / where is this / what's the right format" questions.

Cost note: building the embedding index should use a local, open source embedding model (no per-token API cost regardless of corpus size). Only the answer-generation step at query time should call the Claude API, similar in scale to experiment-auditor's eval set costs.

## First Session Goals

1. Create a new GitHub repository, suggested name `twenty-crm-support-agent`, following the naming and topic tag conventions from experiment-auditor.
2. Set up the Python project structure: virtual environment, `.gitignore` (same pattern as experiment-auditor: `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.DS_Store`, `*.egg-info/`, `dist/`, `.pytest_cache/`).
3. Bring this brief into the repo as the seed for the architecture/decision log section of the README.
4. Set up a local, open source embedding model and verify it can turn a piece of text into an embedding vector, with no API calls. This is new territory (the retrieval half of RAG, as opposed to the classification/generation work in experiment-auditor) and should be explained step by step.
5. Pull a small sample of actual Twenty documentation pages (Data Model section to start) into the project as raw files, as a first look at the real content the system will work with.

Do not jump ahead to the full ingestion pipeline, retrieval confidence thresholds, or evaluation set design in this first session. Those are the next decisions after the foundation above is working, and should be made by looking at the real documentation content once it's actually in the project, not decided in the abstract.
