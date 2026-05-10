---
name: vendor-pipeline-partner-influence-scout
description: Use when a Channel Chief, RevOps, PDM, or AE wants to scan the vendor's CRM (or an Excel pipeline export) to identify which open deals or accounts would benefit most from partner influence — determine which specific partner should be brought in and why — then handle the registration / co-sell flagging and post a context-rich comment on the deal. Trigger phrases include "which deals need a partner", "find partner-influence opportunities", "who should we bring into deal X", "scout partner co-sell", "match partners to pipeline", "Excel pipeline + partner match".
---

# Pipeline Partner-Influence Scout (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP (+ optional Read for Excel exports if pipeline lives in spreadsheets, optional Salesforce/HubSpot MCPs).
**Use case**: 08 — Deal Registration (proactive vendor-driven side; complementary to `partner-register-deal` and `vendor-email-deal-registration-watcher`).

## Why this matters
Most channel programs are reactive on registration — they wait for partners to submit. But ~35% partner-led revenue uplift (Computer Market Research) compounds further when the vendor proactively *places* partners on deals where partner influence improves the outcome: complex implementations, vertical-specific motions, geographic proximity, services attach, existing-customer relationships. This skill scans the pipeline, identifies high-leverage partner-influence opportunities, and handles the registration mechanics — including a context-rich comment that explains *why this partner on this deal*.

The complementary partner-side skill is `partner-pipeline-influence-companion`, which lets a partner see the same view from their side.

## Inputs to gather first
- **Pipeline source**: Introw / connected CRM (`search_crm_objects`), or an Excel/CSV the user provides (then Read it).
- **Filter scope**: open deals only? specific stage range? specific products? specific regions?
- **Partner-influence definition for this vendor**: services-led? vertical-led? geography-led? existing-customer-led? Confirm if not on file.
- **Action mode**: surface only, or auto-register / flag co-sell where match is clean?

## Process

### Step 1 — Pull the pipeline
- Primary: `Introw:search_crm_objects` for open deals (filter to stages where partner influence has leverage — usually mid-funnel onward, post-discovery).
- If user provides Excel/CSV: Read the file and treat each row as a deal record; map columns to the standard schema (account, value, stage, close-date, product, owner, region, vertical).

### Step 2 — Score each deal for partner-influence leverage
Score per deal across multiple dimensions:
- **Vertical specialization** — is this a healthcare deal where a healthcare-specialist partner would close better?
- **Geographic proximity** — is the customer in a region where a local partner has presence?
- **Services / implementation complexity** — is this a deal where SI delivery would derisk close?
- **Existing-customer relationship** — does any partner already serve this customer in another product line?
- **Stalled / needs-momentum** — has the deal been in-stage > X days without a partner?
- **Tech-stack match** — does the deal involve integrations a specific partner already builds for?
- **Margin / packaging** — would partner-led pricing/packaging unlock the deal?

Output a priority score per deal: how much would partner influence improve the close probability, expected value, or close velocity?

### Step 3 — Match each high-leverage deal to a specific partner
For each prioritized deal:
- `Introw:search_partners` — filter by region, vertical, partner type, certifications relevant to the deal.
- `Introw:search_crm_objects` — partners with **prior wins on similar customers** (vertical, deal size, products) — strongest signal.
- `Introw:search_partner_engagement` — partners actively engaged this quarter (avoid putting deals on dormant partners).
- `Introw:get_tier_information` — tier requirements affecting eligibility.
- `Introw:get_goals` — partners pacing on goals where this deal would help.

For each candidate match, articulate the **why** in one sentence:
- "Partner X — has 3 recent closed-won deals in healthcare AI at similar deal sizes; located in same region as customer; certified on the relevant product."
- "Partner Y — already serves this customer in a different product line; cross-sell motion is the natural play."

### Step 4 — Conflict check
Before flagging or registering:
- Cross-check existing registrations on the account (`Introw:search_form_submissions`).
- Cross-check direct sales claim (account in named-account list?).
- Cross-check other partners with open registrations.
- If conflict — surface, don't auto-resolve. Hand off to `vendor-detect-channel-conflict`.

### Step 5 — Handle the registration / co-sell flag
For clean matches with no conflict:
- Auto-register the partner (or surface for human approval based on confirmed mode):
  - `Introw:share_lead_or_register_deal` with the partner's ID and the deal context.
- Post a context-rich comment on the deal:
  - `Introw:add_comment` on the CRM object with the **why this partner**, the prior-win evidence, the suggested co-sell motion, and the recommended next step (intro call, joint pitch, technical deep-dive).
- Notify both the AE and the partner:
  - `Introw:add_task` for the AE to make the intro.
  - `Introw:add_task` or comment for the partner to confirm engagement.

For conflicted or judgment-call matches:
- Surface to a human reviewer with full context.

### Step 6 — Track the placement
- `Introw:search_partner_engagement` and `search_crm_objects` over the next 14/30/60 days to measure whether the placement actually moved the deal.
- Capture outcome via `add_comment` so the next pipeline-scout cycle has training data.

## Output format
- **Pipeline scan summary**: deals scored, distribution by leverage tier.
- **High-leverage match table**: deal, value, stage, recommended partner, why, conflict status, action taken.
- **Confirmed actions**: registrations created, comments posted, tasks assigned.
- **Surfaced for review**: conflict, ambiguous match, or judgment-call cases with full context.
- **Tracking checkpoints**: when to measure placement effectiveness.

## Guardrails & PRM best practice
- **Why beats who.** Every match needs a one-sentence "why this partner" that traces to evidence (prior wins, vertical match, customer relationship). If you can't articulate the why, the match is wrong.
- **Channel conflict before action.** Always run the conflict check before flagging — proactive partner placement that creates conflict is worse than no placement at all.
- **Don't displace working AEs.** When a deal is healthy and progressing, a partner overlay can disrupt — match leverage to deal-state, don't impose partners on deals that don't need them.
- **Tier-aware placement.** Strategic deals to top-tier partners; transactional deals to volume-oriented partners. Mismatching destroys margin and partner energy.
- **No auto-action without confirmation on first run.** First-time use of this skill: surface, don't act. Once the user has validated the matching logic against their judgment, auto-action mode can be enabled.
- **Capture the rationale on the deal record.** The AE who picks up the deal next week needs to see why a partner was placed — don't make them archaeology the comment thread.
- **Goal-relevance.** When two partners are equally well-matched, prefer the one whose `get_goals` shows they're pacing toward a target this deal would help — placement is also an activation lever.
- **Don't poach.** If another partner already has a registration on the account, don't override — that's the conflict path, not the placement path.
- **Excel mode is provisional.** Excel pipelines lack the live attribution Introw has; Excel-based matches surface for human review by default rather than auto-action.
- **Cross-skill handoff.** Conflicts → `vendor-detect-channel-conflict`. Clean placements that need coaching → `vendor-deal-coach-from-similar-wins`. Activation lever → `vendor-activate-network-with-personalized-campaigns`.
