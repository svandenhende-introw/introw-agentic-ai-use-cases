---
name: vendor-acquisition-abm-orchestrator
description: End-to-end agentic partner acquisition. Use when a Channel Chief, VP Partnerships, Partner Recruiter, or RevOps user wants to (a) identify top-performing partners (combining revenue with Crossbeam-based ecosystem-reach signals — overlapping customers, customers in the vendor's ICP, customers in the vendor's pipeline), (b) surface ecosystem coverage gaps against strategic goals, (c) build a lookalike profile, (d) find key stakeholders at target partner accounts, and (e) launch a relevance-tight ABM campaign with joint-value messaging — while pre-configuring the Introw Partner Portal experience for incoming targets. Trigger phrases include "agentic partner acquisition", "build a partner ABM campaign", "find me partners we should recruit", "ecosystem coverage gap", "joint-value outreach", "lookalike + outbound", "ICP-overlap-driven partner recruitment", "find under-leveraged partners by Crossbeam overlap", "ecosystem-reach lookalikes", "high-overlap low-revenue partners".
---

# Strategic Partner Acquisition: ABM Orchestrator (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP + **optional claude.ai Crossbeam** MCP (+ optional Clay / ABM-platform MCPs if installed).
**Use case**: 01 — Partner Acquisition.

## When to use this skill

End-to-end agentic partner acquisition. Use when a Channel Chief, VP Partnerships, Partner Recruiter, or RevOps user wants to (a) identify top-performing partners — combining revenue with Crossbeam-based ecosystem reach (overlapping customers, customers at the partner that match the vendor's ICP, customers at the partner that are in the vendor's open pipeline), (b) surface ecosystem coverage gaps against strategic goals, (c) build a lookalike profile, (d) find key stakeholders at target partner accounts, and (e) launch a relevance-tight ABM campaign with joint-value messaging — while pre-configuring the Introw Partner Portal experience for incoming targets.

**Sample prompts that fire this skill:**
- "agentic partner acquisition"
- "build a partner ABM campaign"
- "find me partners we should recruit"
- "ecosystem coverage gap"
- "joint-value outreach"
- "lookalike + outbound"
- "ICP-overlap-driven partner recruitment"
- "find under-leveraged partners by Crossbeam overlap"
- "ecosystem-reach lookalikes"
- "high-overlap low-revenue partners"

## Why this matters
Channel partner activation baseline sits at **30–50%**, with unmanaged programs **below 20%** (Unifyr Channel Atlas). At ~€15K effective cost-per-acquired-partner, a 100-partner-per-year intake at 50% activation **wastes €750K/year** on partners who never produce pipeline. Lifting activation 30% → 50% on the same intake = **67% more productive partners** ≈ **€10M incremental sourced ARR per 100-partner cohort**. Partner recruitment has been the least-instrumented part of the channel motion; this skill instruments it end-to-end.

**Ecosystem reach is a top-performer signal that revenue alone misses.** A partner with €100K in sourced revenue but 200 customers overlapping the vendor's ICP (per Crossbeam) is *not* a low performer — they're a massively *under-leveraged* one. The lookalike profile built from such a partner unlocks net-new recruitment that revenue-only ranking would never surface. When Crossbeam is connected, this skill weighs **revenue × ecosystem reach** rather than revenue alone, and explicitly surfaces high-overlap-low-revenue partners as both (a) lookalike templates for net-new recruitment and (b) activation candidates inside the existing base.

## What this skill orchestrates
1. **Top-performer pattern extraction** — what makes our best partners actually best, combining revenue and (when Crossbeam is connected) ecosystem reach into our ICP and pipeline.
2. **Under-leveraged-partner detection** — partners with high Crossbeam overlap but low realized revenue, who are both (a) the strongest lookalike templates and (b) activation candidates inside the existing base.
3. **Strategic-goal-aligned gap analysis** — where the ecosystem is short relative to revenue ambition.
4. **Lookalike candidate sourcing** — net-new targets matching the pattern.
5. **Stakeholder identification** — *which humans* inside those targets to engage.
6. **Joint-value ABM campaign generation** — relevance-tight messaging per target.
7. **Portal experience pre-configuration** — so when a prospect engages, they land in a fine-tuned Introw experience, not a generic application form.

## Inputs to gather first
- **Reference cohort scope**: top performers by what (sourced ARR, win rate, expansion ARR, certification depth)? Default: top 10–20 by trailing-4-quarter sourced ARR.
- **Strategic goals**: Net-new region coverage? Vertical penetration? Product-line attach? Pull from `Introw:get_goals` if encoded; else ask.
- **Geo / vertical / segment / partner-type constraints.**
- **Volume + cadence**: how many targets, what outbound cadence.
- **CTA**: deal-reg-eligible co-sell, joint webinar, pilot offer, lead share?

## Process

### Step 1 — Build the reference cohort
**Revenue dimension** (always available):
- `Introw:search_crm_objects` — closed-won deals (trailing 4 quarters), grouped by sourcing partner.
- `Introw:search_partners` — enrich with tier, lifecycle, categories, contact info.
- `Introw:search_partner_engagement` — engagement intensity (comments, deal updates, asset views, form submits).
- `Introw:search_commissions` — commissions earned as a sustained-performance proxy.
- `Introw:get_tier_information` — tier rules if scoping to a specific tier.

**Ecosystem-reach dimension** (when Crossbeam MCP is connected — heavily recommended for this skill):
- `Crossbeam:*` — for each existing partner, pull customer overlap counts:
  - **Total overlap**: how many customers they have that exist in the vendor's CRM in any form.
  - **ICP overlap**: how many of their customers match the vendor's defined ICP (segment / vertical / size).
  - **Pipeline overlap**: how many of their customers are currently *open opportunities* in the vendor's pipeline (these are the highest-value overlap — they're warm-introduction opportunities sitting on the table).
  - **Closed-won overlap**: customers the vendor has already won where the partner is also present (validates partner-vendor compatibility).
  - **Lapsed-customer overlap**: vendor's churned customers the partner still serves (reactivation opportunity).
- Weight overlap *type* (pipeline > ICP > total > lapsed) and *recency* (last 90 days > older).

Build a unified score per existing partner: `(realized revenue) × (sustained-quarter weight) + (ecosystem-reach weight × overlap_score)`. Partners with strong ecosystem reach but weak revenue surface as a separate "under-leveraged" bucket — they're the highest-value lookalike templates.

### Step 2 — Extract the lookalike signature
Across the reference cohort (now including the under-leveraged-but-high-overlap bucket), summarize:
- Vertical / segment / geography
- Partner type (SI, reseller, referral, MSP, marketplace)
- Tech-stack signals from CRM custom fields
- Headcount band
- Avg deal size, sales cycle, win rate
- Onboarding → first-deal lag
- Engagement intensity (activities per active week)
- **Customer-base composition** (Crossbeam) — what segments / verticals dominate the partner's customer book? What % of their customers fall in our ICP? What's the typical *overlap-to-revenue ratio* (a partner with high ratio is converting overlap to revenue efficiently; low ratio is the activation gap).
- **Pipeline overlap density** (Crossbeam) — partners whose existing customer base correlates with our open-pipeline accounts are the strongest co-sell-fit profile.

### Step 3 — Map ecosystem coverage gaps to strategic goals
Cross-check the lookalike signature and current footprint against goals:
- `Introw:get_goals` — strategic goals (regions, verticals, products to grow).
- Compute coverage: do we have enough lookalike-pattern partners in each goal area?
- Surface gaps: e.g., "Germany generates 3× the revenue but has 50% of the partner bandwidth — or no partner at all in healthcare."
- **Crossbeam-driven gap**: cross-check the vendor's open pipeline + ICP target accounts against the existing partner base — are there segments / verticals where the vendor has heavy pipeline but no partner with overlap into it? Those are the highest-priority recruitment targets.
- The output of this step is a **ranked acquisition brief**, not a generic prospecting list.

### Step 4 — Source net-new targets
- If a Clay / ABM-platform MCP is installed, use it to source firmographically-matched candidates against the lookalike signature + gap brief.
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
- **Reference cohort summary** — top performers + revenue + engagement metrics + (Crossbeam) total / ICP / pipeline overlap counts.
- **Under-leveraged-partner list** — high-overlap, low-revenue partners surfaced separately as both lookalike templates AND activation candidates.
- **Lookalike signature** — 5–8 firmographic + behavioral + ecosystem-reach bullets.
- **Ecosystem coverage gap map** — gaps ranked by strategic-goal alignment + revenue impact + pipeline-overlap absence.
- **Target list** — accounts × stakeholders × match score × joint-value framing.
- **ABM message variants per target** — drafted, not sent.
- **Portal experience brief per target** — personalization payload ready for activation.
- **Suggested next actions** with owners + ETA.

## Guardrails & PRM best practice
- **Evidence-based, not vibes-based.** Every recommendation traces back to a tool call. CSO Insights: top-quartile programs outperform peers on win rate by **+17.9 pts** — this only holds if you recruit the right partners, not the loudest applicants.
- **Revenue ≠ performance when ecosystem reach exists.** A partner with €100K revenue and 200 ICP-matched customers is under-leveraged, not low-performing. Don't filter them out of top-performer ranking based on revenue alone — they're often the most informative lookalike template AND a high-priority activation candidate.
- **Crossbeam data has lag.** Overlap data refreshes typically run nightly or weekly; flag stale data and avoid acting on overlaps > 30 days old without confirmation.
- **Crossbeam respects data-sharing scope.** Only surface overlaps within authorized population groups / partner-data-sharing agreements. Never surface partner customer names outside the vendor-internal scope.
- **Territory check before outbound.** `Introw:search_partners` for existing coverage in the geo/vertical to avoid flooding territory and seeding channel conflict.
- **Don't auto-create partner records.** End at the brief + outbound. Partner record creation is a deliberate human action.
- **Joint value, not vendor benefit.** Messaging must articulate what the *partner* gets, framed in their economics — not what we get.
- **No spray-and-pray.** If the target list exceeds the lookalike pattern's natural population, segment harder; don't dilute relevance to hit volume.
- **Lookalike ≠ filter.** The signature frames the search; let the recruiter override on judgment.
- **Frame outcomes in expected ARR uplift.** A 1pt activation lift on a 100-partner cohort beats hiring 30 mediocre partners — keep the user honest about the math.
- **Capture decisions** via `Introw:add_comment` on the partner/prospect record so the audit trail survives reorgs.
- **Hand off cleanly** — when a target converts, the personalization payload feeds the onboarding orchestrator. No "what was that conversation about" gaps.
- **Cross-skill handoff.**
  - Under-leveraged partners (high overlap, low revenue) found in Step 1 → feed `vendor-activate-network-with-personalized-campaigns` to wake them up before recruiting their lookalikes.
  - Pipeline-overlap signals on existing partners → `vendor-pipeline-partner-influence-scout` to convert overlap into deal-registration opportunities now (don't wait for the recruitment cycle).
  - Target-account list with overlap signals on prospective partners → `vendor-crossbeam-cosell-finder` (proactive co-sell variant).
  - Once a target converts → `vendor-personalized-onboarding-from-transcripts` to pick up cleanly.
