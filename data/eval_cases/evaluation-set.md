# Twenty CRM Support Specialist: Evaluation Set

## Status and Construction Note

**This is a first draft evaluation set generated from documentation review, not from observed user confusion.**

The questions below were written after reading Twenty's User Guide documentation covering data model, objects, fields, views, and workflows. They were not derived from watching real users interact with the product. This is an acknowledged limitation: questions written by someone who has read the documentation will tend to use closer-to-correct terminology and will be less likely to expose discoverability failures than questions written by genuinely confused first-time users.

A planned revision step involves using the Twenty demo (app.twenty.com, credentials noah@demo.dev / Applecar2025) to surface real confusion points and add evaluation cases grounded in actual friction. Until that revision is done, the evaluation set should be treated as covering correctness and basic retrieval, but not as a strong test of the discoverability failure mode specifically.

---

## Evaluation Case Format

Each case includes:
- **ID**: unique identifier
- **User query**: phrased as a user would type it, not as a documentation heading
- **Expected outcome**: ANSWER (should respond from docs), ESCALATE-T1 (no relevant docs), or ESCALATE-T2 (docs exist but behavior mismatch suspected)
- **Relevant documentation**: which page(s) should be retrieved
- **What a good answer looks like**: the key information a correct response should contain
- **Discoverability gap**: whether the user's phrasing differs meaningfully from the documentation's terminology (YES/NO, with explanation)
- **Notes**: anything worth watching for during evaluation

---

## Data Model Cases

### DM-01
**User query:** "What's the difference between an object and a record in Twenty? I keep seeing both words."

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/data-model/overview

**What a good answer looks like:** Objects are the categories of data (like People or Companies), records are the individual entries within those categories (like a specific person named John Smith). The analogy to spreadsheets is useful: objects are like the sheet itself, records are like individual rows.

**Discoverability gap:** NO. The user is using the product's own terms, just asking what they mean.

**Notes:** This is a baseline correctness test. If the system cannot answer this from the overview page, something is fundamentally wrong with retrieval.

---

### DM-02
**User query:** "I want to track projects in my CRM, should I make a new section or add more columns to what I already have?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/data-model/overview

**What a good answer looks like:** If Projects have their own properties, lifecycle, and relationships to other things, they should be a custom object. If Projects are just a category of something that already exists, a field (like a select field for type) is enough. The documentation's heuristic is: if it has its own lifecycle, properties, or connections to multiple other objects, it deserves its own object.

**Discoverability gap:** YES. The user says "new section" and "columns" where the documentation says "object" and "fields." This is a direct test of whether semantic retrieval can bridge colloquial spreadsheet language to CRM data model terminology.

**Notes:** This is one of the most important discoverability test cases. A keyword search for "section" or "columns" would likely return nothing useful.

---

### DM-03
**User query:** "Can I add a field that automatically calculates a value from other fields, like a formula?"

**Expected outcome:** ESCALATE-T1 (with a note)

**Relevant documentation:** user-guide/data-model/overview (partially)

**What a good answer looks like:** The documentation does not currently describe a native formula field type. The workaround documented is using workflows to calculate and update field values automatically. The system should say it could not find documentation for a formula field feature, note the workflow workaround if retrieved, and escalate.

**Discoverability gap:** NO. "Formula" is the term the community uses and the docs reference.

**Notes:** This is the formula fields case we identified during research. The documentation previously stated this feature was coming in Q1 2026. As of June 2026 it has not shipped. This tests whether the system escalates correctly when the feature does not exist as documented rather than hallucinating a confident answer about a feature that is not there. This case may need to be updated if formula fields ship.

---

### DM-04
**User query:** "I don't see the Data Model option anywhere in my settings, how do I find it?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/data-model/overview

**What a good answer looks like:** Data Model is in Settings in the left sidebar. If it is not visible, it is likely a permissions issue. Only administrators can access the data model by default. The user should contact their workspace admin.

**Discoverability gap:** NO. The user is describing a UI navigation problem and the documentation has a direct note about this.

**Notes:** This is a straightforward navigation case. Also tests whether the system surfaces the permissions caveat, which is easy to miss but important for a user who is stuck.

---

### DM-05
**User query:** "I want contacts and leads to be separate things in my CRM but I'm not sure if I should create two objects or just use one with some kind of label."

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/data-model/overview

**What a good answer looks like:** The documentation explicitly addresses this. The recommendation is to use one People object with a field like "Person Type" containing values like "Prospect" and "Partner" (or "Lead" and "Contact"), then create different views to filter. Creating separate objects for categories of the same thing is discouraged. Email and calendar sync only works with the standard People object, which is another reason not to split it.

**Discoverability gap:** YES. The user says "label" where the documentation says "select field." The user says "contacts and leads" where the documentation says "Person Type field with values." This tests whether retrieval can bridge from the user's intent to the documentation's specific recommendation.

**Notes:** The email and calendar sync constraint is a meaningful detail a correct answer should include, since it affects the decision.

---

## Views Cases

### VW-01
**User query:** "How do I save a view so only I can see it and not my whole team?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/crm-essentials/view-management

**What a good answer looks like:** When creating or editing a view, set its visibility to "Unlisted." Unlisted views appear only in your own "My unlisted views" section and are hidden from other team members' view lists. Note that anyone with a direct link can still access them.

**Discoverability gap:** YES. The user says "only I can see it" where the documentation uses the term "Unlisted." A keyword search for "private view" or "personal view" might not surface this clearly.

**Notes:** The caveat that unlisted views are still accessible via direct link is important and easy to miss. A good answer should include it.

---

### VW-02
**User query:** "I accidentally changed the filters on a shared view. How do I undo that without messing up what my team saved?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/crm-essentials/view-management

**What a good answer looks like:** When you modify sorting or filtering on an existing view, a "Save as new view" button appears. This lets you create a new view based on your customizations without overwriting the original. The user can use this to preserve the shared view.

**Discoverability gap:** NO. But this is a realistic confusion scenario: users will not know this button appears automatically and may not look for it.

**Notes:** This tests whether the system can answer an implicit question (how do I not break the shared view) that is not phrased as a direct lookup question.

---

### VW-03
**User query:** "Can I group my list by a field, like group all opportunities by stage?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/crm-essentials/view-management

**What a good answer looks like:** Yes, but there is a specific sequence. You must first select the List layout and then add a Group By. You cannot create a List Group By directly. For stage-based grouping of opportunities specifically, a Kanban view is the more natural choice since each column represents a stage.

**Discoverability gap:** YES. The user says "group my list" where the documentation uses "List Group By." The Kanban suggestion is also a non-obvious redirect that a good answer should include.

**Notes:** The sequence dependency (List layout first, then Group By) is a real friction point that is easy to get wrong.

---

## Workflows Cases

### WF-01
**User query:** "How do I set up an automatic reminder when a deal hasn't been updated in a while?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/workflows/getting-started-workflows, user-guide/workflows/capabilities/workflow-actions

**What a good answer looks like:** This requires a workflow with a scheduled or record-based trigger watching for stale updates on the Opportunities object. The workflow would check the last updated date, and if the condition is met, trigger a notification or task creation. The documentation lists "stale opportunity alerts" as an explicit internal automation example.

**Discoverability gap:** YES. The user says "automatic reminder" and "hasn't been updated in a while" where the documentation says "workflow" and "stale opportunity alerts." This is a strong discoverability test.

**Notes:** The documentation mentions this as an example but may not walk through the full setup steps. Watch for whether the system gives a confident complete answer or honestly notes the limitation.

---

### WF-02
**User query:** "My workflow isn't showing up in my sidebar, where did it go?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/workflows/capabilities/workflow-features

**What a good answer looks like:** If the Workflows section is not visible, it is a permissions issue. The user should contact their workspace administrator to grant access to workflows.

**Discoverability gap:** NO. The documentation has a direct note about this.

**Notes:** Parallel to DM-04 (Data Model not visible). Tests whether the system handles the recurring pattern of "I can't see this feature" with the permissions answer.

---

### WF-03
**User query:** "I want to connect Twenty to our webform so new leads automatically get added. Is that possible?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/workflows/getting-started-workflows

**What a good answer looks like:** Yes. Workflows support a webhook trigger that fires when a GET or POST request is received from an external service. A webform can be configured to send a POST request to Twenty's webhook endpoint, which triggers a workflow that creates a new record. The documentation explicitly lists webform submissions as an integration example.

**Discoverability gap:** YES. The user says "connect to our webform" where the documentation says "webhook trigger" and "POST request." This tests whether retrieval bridges from the business intent to the technical mechanism.

**Notes:** The answer requires connecting two pieces of the documentation: the webhook trigger and the create record action. This is a mild chunking test.

---

### WF-04
**User query:** "I set up a workflow but when I click activate nothing happens and it never runs."

**Expected outcome:** ESCALATE-T2 (possible mismatch)

**Relevant documentation:** user-guide/workflows/capabilities/workflow-features

**What a good answer looks like:** The documentation says clicking Activate publishes the draft as a new version and makes it eligible to run when triggered, but does not immediately execute it. So if the user is expecting it to run immediately, that is a documentation explanation case, not a bug. However, if the user has a trigger configured and the workflow still never fires after the triggering event occurs, that is not explained by the documentation and should escalate.

**Discoverability gap:** NO.

**Notes:** This is the most nuanced case in the set. The correct response depends on what the user means by "never runs." The system needs to distinguish between "I expected it to run immediately on activation" (answerable from docs) and "it is triggered but nothing happens" (possible mismatch, should escalate). This is a good test of whether the system can ask a targeted clarifying question in a future version, or whether in V1 it defaults to escalation when ambiguous.

---

### WF-05
**User query:** "Can I make a workflow run on a schedule, like every Monday morning?"

**Expected outcome:** ANSWER

**Relevant documentation:** user-guide/workflows/capabilities/workflow-actions

**What a good answer looks like:** Yes. Twenty workflows support a scheduled trigger type and also include a Delay action that pauses execution for a specified duration or until a specific date and time. A recurring Monday morning workflow would use a scheduled trigger configured for weekly recurrence.

**Discoverability gap:** NO. But this tests whether the system can synthesize across the trigger and the delay action, which may live in different parts of the retrieved content.

**Notes:** Watch for whether the answer confuses the Delay action (pauses within a running workflow) with a scheduled trigger (starts the workflow on a schedule). These are related but distinct.

---

## Summary Table

| ID    | Domain     | Expected outcome | Discoverability gap | Primary test |
|-------|------------|-----------------|---------------------|--------------|
| DM-01 | Data model | ANSWER          | NO                  | Baseline correctness |
| DM-02 | Data model | ANSWER          | YES                 | Colloquial to CRM terminology |
| DM-03 | Data model | ESCALATE-T1     | NO                  | Missing feature, no hallucination |
| DM-04 | Data model | ANSWER          | NO                  | Navigation and permissions |
| DM-05 | Data model | ANSWER          | YES                 | User intent to documented recommendation |
| VW-01 | Views      | ANSWER          | YES                 | "Private" to "Unlisted" terminology |
| VW-02 | Views      | ANSWER          | NO                  | Implicit question phrasing |
| VW-03 | Views      | ANSWER          | YES                 | "Group my list" to List Group By |
| WF-01 | Workflows  | ANSWER          | YES                 | Business intent to workflow mechanism |
| WF-02 | Workflows  | ANSWER          | NO                  | Permissions pattern |
| WF-03 | Workflows  | ANSWER          | YES                 | Webform intent to webhook mechanism |
| WF-04 | Workflows  | ESCALATE-T2     | NO                  | Ambiguous mismatch, clarification needed |
| WF-05 | Workflows  | ANSWER          | NO                  | Cross-chunk synthesis |

**Total cases:** 13
**Expected ANSWER:** 11
**Expected ESCALATE-T1:** 1
**Expected ESCALATE-T2:** 1
**Cases with discoverability gap:** 6 of 13

---

## Planned Revision

Before treating this evaluation set as final, the following cases should be added from direct product use:
- At least 3 questions that arose from genuine confusion during a session with the Twenty demo
- At least 1 additional Type 2 mismatch case if one is found during product use
- Revision of any question whose phrasing feels too close to documentation language after real use reveals how users actually phrase things
