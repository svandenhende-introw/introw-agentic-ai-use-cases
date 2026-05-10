---
name: vendor-acquisition-abm-orchestrator
description: End-to-end agentic partner acquisition. Use when a Channel Chief, VP Partnerships, Partner Recruiter, or RevOps user wants to (a) identify top-performing partners, (b) surface ecosystem coverage gaps against strategic goals, (c) build a lookalike profile, (d) find key stakeholders at target partner accounts, and (e) launch a relevance-tight ABM campaign with joint-value messaging — while pre-configuring the Introw Partner Portal experience for incoming targets. Trigger phrases include "agentic partner acquisition", "build a partner ABM campaign", "find me partners we should recruit", "ecosystem coverage gap", "joint-value outreach", "lookalike + outbound".
---

# Strategic Partner Acquisition: ABM Orchestrator (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP (+ optional Clay / LinkedIn Sales Navigator / ABM-platform MCPs if installed).
**Use case**: 01 — Partner Acquisition.

## Why this matters
Channel partner activation baseline sits at **30–50%**, with unmanaged programs **below 20%** (Unifyr Channel Atlas). At ~€15K effective cost-per-acquired-partner, a 100-partner-per-year intake at 50% activation **wastes €750K/year** on partners who never produce pipeline. Lifting activation 30% → 50% on the same intake = **67% more productive partners** ≈ **€10M incremental sourced ARR per 100-partner cohort**. Partner recruitment has been the least-instrumented part of the channel motion; this skill instruments it end-to-end.

## What this skill orchestrates
1. **Top-performer pattern extraction** — what makes our best partners actually best.
2. **Strategic-goal-aligned gap analysis** — where the ecosystem is short relative to revenue ambition.
3. **Lookalike candidate sourcing** — net-new targets matching the pattern.
4. **Stakeholder identification** — *which humans* inside those targets to engage.
5. **Joint-value ABM campaign generation** — relevance-tight messaging per target.
6. **Portal experience pre-configuration** — so when a prospect engages, they land in a fine-tuned Introw experience, not a generic application form.

## Inputs to gather first
- **Reference cohort scope**: top performers by what (sourced ARR, win rate, expansion ARR, certification depth)? Default: top 10–20 by trailing-4-quarter sourced ARR.
- **Strategic goals**: Net-new region coverage? Vertical penetration? Product-line attach? Pull from `Introw:get_goals` if encoded; else ask.
- **Geo / vertical / segment / partner-type constraints.**
- **Volume + cadence**: how many targets, what outbound cadence.
- **CTA**: deal-reg-eligible co-sell, joint webinar, pilot offer, lead share?

## Process

### Step 1 — Build the reference cohort
- `Introw:search_crm_objects` — closed-won deals (trailing 4 quarters), grouped by sourcing partner.
- `Introw:search_partners` — enrich with tier, lifecycle, categories, contact info.
- `Introw:search_partner_engagement` — engagement intensity (comments, deal updates, asset views, form submits).
- `Introw:search_commissions` — commissions earned as a sustained-performance proxy.
- `Introw:get_tier_information` — tier rules if scoping to a specific tier.

### Step 2 — Extract the lookalike signature
Across the reference cohort, summarize:
- Vertical / segment / geography
- Partner type (SI, reseller, referral, MSP, marketplace)
- Tech-stack signals from CRM custom fields
- Headcount band
- Avg deal size, sales cycle, win rate
- Onboarding → first-deal lag
- Engagement intensity (activities per active week)
- Customer ICP overlap (what end customers do they win at?)

### Step 3 — Map ecosystem coverage gaps to strategic goals
Cross-check the lookalike signature and current footprint against goals:
- `Introw:get_goals` — strategic goals (regions, verticals, products to grow).
- Compute coverage: do we have enough lookalike-pattern partners in each goal area?
- Surface gaps: e.g., "Germany generates 3× the revenue but has 50% of the partner bandwidth — or no partner at all in healthcare."
- The output of this step is a **ranked acquisition brief**, not a generic prospecting list.

### Step 4 — Source net-new targets
- If a Clay / LinkedIn Sales Navigator / ABM-platform MCP is installed, use it to source firmographically-matched candidates against the lookalike signature + gap brief.
- If not, output a **directly-pasteable acquisition brief** (firmographic filters + intent signals) for the recruiter to feed into their tool of choice.

### Step 5 — Identify key stakeholders at target accounts
For each target partner account:
- Look for the channel/alliances/business-development decision-maker.
- Look for sales leaders who'd benefit from the joint motion.
- Look for technical leads if the relationship requires integration.
- Use Clay/LinkedIn enrichment if available; otherwise output a stakeholder-role checklist for human enrichment.

### Step 6 — Generate joint-value ABM messaging per target
The defining quality of this skill: messaging is **relevance-tight, not template-tight**. For each target:
- Open with a specific reason this partnership creates joint value (not "we'd love to partner").
- Reference the target's actual customer ICP overlap with our top performers.
- Quantify the joint outcome (typical sourced ARR per top performer of this profile).
- Tier-aware CTA — pilot, co-sell, lead share, joint webinar.
- Localize tone (DACH = compliance-forward, US = use-case-forward).
- Drafts should pass the "would I respond?" test before being sent.

### Step 7 — Pre-configure the Introw Partner Portal experience
A target who engages should not land in a generic "fill out this 14-field form" experience. For each target, prepare:
- A **personalized landing brief**: why we reached out, the specific joint-value framing, the relevant case studies for their vertical/geo.
- Pre-filled application fields where data is already known.
- Recommended first-90-days journey aligned to their partner type (this hands off cleanly to `vendor-personalized-onboarding-orchestrator`).
- Use `Introw:add_comment` on the prospect record to capture the personalized framing so the CAM has full context when the target engages.
- If using `Introw:share_lead_or_register_deal` to nominate the target for outreach, attach the personalization payload in the comment.

### Step 8 — Hand off to outbound execution
- If outbound execution MCPs are available, fire the sequences with the per-target messaging.
- Otherwise, package into an outbound brief the recruiter can run.
- Set follow-up tasks via `Introw:add_task` so engagement signals get captured back.

## Output format
- **Reference cohort summary** — top performers + revenue + engagement metrics.
- **Lookalike signature** — 5–8 firmographic + behavioral bullets.
- **Ecosystem coverage gap map** — gaps ranked by strategic-goal alignment + revenue impact.
- **Target list** — accounts × stakeholders × match score × joint-value framing.
- **ABM message variants per target** — drafted, not sent.
- **Portal experience brief per target** — personalization payload ready for activation.
- **Suggested next actions** with owners + ETA.

## Guardrails & PRM best practice
- **Evidence-based, not vibes-based.** Every recommendation traces back to a tool call. CSO Insights: top-quartile programs outperform peers on win rate by **+17.9 pts** — this only holds if you recruit the right partners, not the loudest applicants.
- **Territory check before outbound.** `Introw:search_partners` for existing coverage in the geo/vertical to avoid flooding territory and seeding channel conflict.
- **Don't auto-create partner records.** End at the brief + outbound. Partner record creation is a deliberate human action.
- **Joint value, not vendor benefit.** Messaging must articulate what the *partner* gets, framed in their economics — not what we get.
- **No spray-and-pray.** If the target list exceeds the lookalike pattern's natural population, segment harder; don't dilute relevance to hit volume.
- **Lookalike ≠ filter.** The signature frames the search; let the recruiter override on judgment.
- **Frame outcomes in expected ARR uplift.** A 1pt activation lift on a 100-partner cohort beats hiring 30 mediocre partners — keep the user honest about the math.
- **Capture decisions** via `Introw:add_comment` on the partner/prospect record so the audit trail survives reorgs.
- **Hand off cleanly** — when a target converts, the personalization payload feeds the onboarding orchestrator. No "what was that conversation about" gaps.
