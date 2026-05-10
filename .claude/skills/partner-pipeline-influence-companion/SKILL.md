---
name: partner-pipeline-influence-companion
description: Use when a partner user wants to scan accessible vendor pipeline / shared accounts to identify deals where they have unique influence (existing customer relationship, vertical fit, geographic proximity, prior similar wins) — then surface those deals as candidates to register, share context on, or request to be placed on. Trigger phrases include "where can I add value", "which vendor deals fit me", "find deals I should be on", "my partner-influence opportunities", "register the deals I can influence".
---

# Pipeline Partner-Influence Companion (Partner)

**Audience**: Partner user — **claude.ai Introw Connect Staging** MCP.
**Use case**: 08 — Deal Registration (partner-side companion to `vendor-pipeline-partner-influence-scout`).

## Why this matters
Partners typically only register deals they sourced themselves — but a meaningful chunk of vendor-direct or co-sell-eligible pipeline is on accounts where the partner already has earned influence: existing customer relationships, vertical specialization, geographic proximity, prior similar wins. Surfacing those opportunities to the partner self-service multiplies the partner-led-revenue lift (~35%, Computer Market Research) without requiring a vendor-side PDM to spot every opportunity manually.

## Process

### Step 1 — Resolve the portal
If the user has access to multiple partner portals, call `Introw_Connect_Staging:partners` first and confirm which `roomId` to use.

### Step 2 — Pull what the partner can see
Strictly scoped to the partner's accessible data:
- `Introw_Connect_Staging:search_crm_objects` — vendor accounts/deals visible to this partner (per their portal permissions).
- `Introw_Connect_Staging:search_partner_engagement` — their own engagement / asset views.
- `Introw_Connect_Staging:search_form_submissions` — their existing registrations.
- `Introw_Connect_Staging:get_goals` — partner's own goals (pacing context).
- `Introw_Connect_Staging:get_tier_information` — tier eligibility for any product/segment.

### Step 3 — Identify partner-influence candidates
For each accessible vendor account/deal, score the partner's natural fit:
- **Existing customer** — partner already serves this customer in another capacity.
- **Vertical specialization** — partner's vertical focus matches the customer's industry.
- **Geographic proximity** — partner's region matches the customer's region.
- **Prior similar wins** — partner has closed similar deals (vertical × deal size × product).
- **Tech-stack match** — partner builds integrations the deal would benefit from.
- **Service attach** — deal would benefit from implementation services the partner offers.

Score each candidate. Surface the top N with the strongest case.

### Step 4 — Frame the value to the partner
For each candidate, articulate:
- **Why you fit** (the strongest one or two signals).
- **What registering / placing yourself on this would unlock** (deal-protection 10–15 pts margin, MDF eligibility, pre-sales support, tier progression).
- **What the partner would need to do** (intro call, share customer reference, attend joint pitch).

### Step 5 — Take the action the partner chooses
- **Register the deal**: hand off to the `partner-register-deal` flow, pre-filled with the captured fields.
- **Submit a "place me on this" request**: use `Introw_Connect_Staging:share_lead_or_register_deal` with the appropriate form type and a comment explaining the influence rationale.
- **Add context to the deal**: `Introw_Connect_Staging:add_comment` to share what the partner knows about the customer (existing relationships, prior conversations, vertical-specific risks).
- **Add a follow-up task**: `Introw_Connect_Staging:add_task` for the partner to track outreach.

## Output format
- **Top-N candidate list** with: account, deal-context-as-visible, why-you-fit, suggested action.
- **Action confirmations** for any submission / comment / task created.
- **Suggested follow-ups** — e.g., when to check back on response.

## Guardrails & PRM best practice
- **Strictly scoped to partner's permissions.** This skill never surfaces vendor-direct or other-partner data the portal doesn't expose to this partner. If the data isn't visible in the partner's portal scope, it doesn't appear here.
- **Influence claim must be evidenced.** Every "why you fit" needs a concrete signal (existing relationship, prior win, vertical match) — speculative claims undermine the partner's standing with the vendor.
- **Don't over-register.** If a partner registers everything they "could" influence, the vendor's review queue clogs and trust degrades. Prioritize aggressively — top 3–5 candidates, not 50.
- **Conflict awareness.** If the account is already covered by another partner per visible portal data, don't surface it as a registration candidate — surface as a co-sell or referral opportunity instead, or skip.
- **Echo before submit.** For any registration/share, echo the captured fields back for confirmation before calling the write tool.
- **Capture context in the comment.** When the partner has unique knowledge about the customer (decision-maker dynamics, prior product use, regional considerations), capture via `add_comment` — that context is the partner's strongest contribution.
- **Goal-aware suggestions.** Prefer candidates that move the partner toward their `get_goals` targets — pacing matters.
- **Don't promise vendor outcomes.** This skill submits requests; vendor review and conflict logic determine acceptance. Frame next steps as "submitted, in review per SLA," not approval.
- **Cross-skill handoff.** Confirmed registrations → `partner-register-deal` flow. Coaching needs after placement → `partner-coach-my-deal`.
