# twenty-crm-support-agent

A RAG-based support chatbot for [Twenty CRM](https://github.com/twentyhq/twenty). Users ask "how do I" and "where is" questions; the system retrieves relevant documentation and generates a grounded answer, or escalates to a human with a structured handoff.

---

## Problem

Twenty CRM users filing support tickets for questions that are answerable from documentation — the answer exists, but users can't find it quickly. Goal: correct answer in under a minute, without a human in the loop.

---

## Architecture Decisions

### Semantic retrieval (not keyword search)
Users often don't know the product's terminology for what they're looking for. Semantic retrieval matches the user's phrasing to docs that use different words for the same concept.

### Two escalation types
- **Type 1 — Documentation Gap:** No relevant docs retrieved. The product likely works fine but isn't documented. Lower urgency; signal for docs maintainers.
- **Type 2 — Documentation Mismatch:** Docs retrieved and address the question, but contradict the user's described behavior. Possible bug signal. Higher urgency; routes to a technical/support engineering queue.

Keeping these separate costs little (it falls out of comparing retrieved docs against the user's described behavior) and they're owned by different people.

### Evaluation metric
Industry standard is "resolution rate" (conversations that don't escalate), but this lets through cases where the user gave up. This project uses an LLM judgment pass as its primary metric: *"Given the user's question and the system's answer, would a reasonable person be able to complete the task using only this answer?"* This is a proxy for real user behavior — that limitation is stated plainly, not glossed over.

### Embeddings: local model, no API cost
The embedding index uses a local open-source model (no per-token cost regardless of corpus size). Only answer-generation calls the Claude API.

---

## Knowledge Base Scope

Twenty CRM documentation (docs.twenty.com), User Guide — Data Model and Workflows sections.

---

## How to Run

_To be filled in once the pipeline is built._

---

## Project Structure

_To be filled in once the structure stabilizes._

---

## Evaluation Results

_To be filled in._
