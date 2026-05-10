---
name: partner-helpdesk
description: Use when a partner user needs to ask a product, pricing, configuration, enablement, or compliance question to a specific vendor — or wants to execute a scoped self-service action (sandbox provisioning, account lookup, quote draft) — without opening the vendor's portal. Single-vendor scope per invocation. Trigger phrases include "ask vendor X about Y", "what's the price for…", "where's the battle card for…", "spin up a sandbox", "look up account…", general partner-side product Q&A.
---

# Partner Helpdesk (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP. Operates on a **single vendor portal at a time** (the partner picks or the agent confirms).
**Use case**: 06 — Enablement Support.

## When to use this skill

Use when a partner user needs to ask a product, pricing, configuration, enablement, or compliance question to a specific vendor — or wants to execute a scoped self-service action (sandbox provisioning, account lookup, quote draft) — without opening the vendor's portal. Single-vendor scope per invocation.

**Sample prompts that fire this skill:**
- "ask vendor X about Y"
- "what's the price for…"
- "where's the battle card for…"
- "spin up a sandbox"
- "look up account…"

## Why this matters
Traditional partner-vendor support runs on 15-minute-to-multi-hour first-response times — often **36 hours from question to answer** when escalations are involved. AI partner helpdesks deflect **40–60% of routine queries** (Gartner / Pylon benchmarks), with first response collapsing to **23 seconds — a 97% reduction**. For partner sellers who are mid-deal and need an answer right now, this is the difference between closing the deal and losing momentum.

This skill is the partner's in-flow helpdesk: ask anything in natural language, get the answer from the vendor's connected content base, with proper citation and a clear handoff path when the question is out of scope.

## Process

### Step 1 — Resolve the vendor portal
- If the partner has access to multiple vendor portals, call `Introw_Connect_Staging:partners` and confirm which vendor this question is about. **One vendor per invocation** — don't blend answers across vendors.
- If only one portal, proceed.

### Step 2 — Triage the query type
Classify the question:
- **Knowledge** (product, pricing, how-to, battle card, enablement, compliance) → answer from connected knowledge sources, with citation.
- **Account / deal lookup** → use `Introw_Connect_Staging:search_crm_objects` (scoped to partner's data).
- **Task / commitment** → use `Introw_Connect_Staging:search_tasks`.
- **Commission / payment status** → out of scope for this skill; suggest `partner-my-commissions` (if installed) or escalate to CAM.
- **Action request** (sandbox, quote, registration) → use the appropriate write tool **only if scoped under the vendor's capability matrix**; otherwise route for human approval.

### Step 3 — Answer or act
- For **knowledge questions**: pull from the vendor's connected knowledge base (Notion, Confluence, asset library, product docs). Cite which doc / battle card / pricing rule the answer came from. If the answer is partial or stale, say so honestly.
- For **lookups**: query Introw Connect (CRM objects, tasks, form submissions). Return the data scoped to the partner's permissions.
- For **scoped actions**:
  - In-scope auto-actions (per the vendor's capability matrix): account lookup, quote draft, sandbox request submission, deal registration via `share_lead_or_register_deal`. Echo the captured fields back for confirmation before executing any write.
  - Approval-gated actions (pricing exception, MDF release, contract change, partner-tier change): do NOT execute. Draft the request and route via `add_task` to the right CAM / approver.
- For **out-of-capability requests**: say so plainly. Don't improvise outside the matrix.

### Step 4 — Always offer a follow-up path
- "If this doesn't fully answer, I can route this to your CAM" — and if accepted, use `Introw_Connect_Staging:add_task` or `add_comment` to log the request with the vendor.
- If the answer was knowledge-based, surface where the partner can find it next time (the actual portal location).

## Output format
- **Direct answer** in the partner's preferred language, with source citation when knowledge-backed.
- **Action confirmation** (with reference ID) when an action was executed.
- **Clear handoff message** when the query is approval-gated and routed to a human.
- **Follow-up suggestion** — "want me to set a task for your CAM to follow up?"

## Guardrails & PRM best practice
- **Single-vendor scope per invocation.** This skill never aggregates answers across vendors. Each session targets one portal — confirmed at the start. Multi-vendor questions go to a different skill (or a CAM).
- **Strict data scoping.** Show only the data the partner is entitled to see in their portal. Never expose other partners' deals, vendor-internal pricing rules, or cross-customer data.
- **Capability matrix is the contract.** Anything outside the matrix is routed, not improvised. "Outside the matrix" answers should always include the alternate path (CAM, approval form, etc.).
- **Compliance.** Customer PII, pricing exceptions, and contract terms stay human-approved unless explicitly scoped under SOC 2 / ISO 27001 / GDPR controls.
- **Multilingual.** Answer in the partner's language even if source content is in English. If translation introduces ambiguity, link to the source.
- **Cite sources.** Knowledge answers always reference which battle card / doc / pricing page they came from. Opacity erodes trust faster than not knowing.
- **Honest about gaps.** If the answer isn't in the connected knowledge base, say so — don't fabricate. Surface as a content gap (feeds `vendor-support-content-gap-detector` next cycle).
- **Don't write without confirmation.** Any write action (registration, sandbox request, etc.) echoes the captured fields back for confirmation before calling the write tool.
- **Log for the loop.** Use `add_comment` on the relevant record to capture the question and resolution. Feeds the vendor's deflection audit and improves the knowledge base over time.
- **Cross-skill handoff.** Deal-related coaching question → `partner-deal-war-room`. Cert / training question → `partner-cross-vendor-cert-tracker`. Commission-status → out-of-scope, refer to commission-specific skill or finance contact.
