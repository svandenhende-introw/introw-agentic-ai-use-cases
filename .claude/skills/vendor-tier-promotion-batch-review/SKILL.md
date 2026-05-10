---
name: vendor-tier-promotion-batch-review
description: Use quarterly (or on demand) when a Channel Chief, RevOps, or PDM wants to audit the entire partner base for tier promotion or demotion eligibility — combining revenue, certifications, engagement, and goal attainment — and draft the partner-facing comms for each move. Trigger phrases include "tier review", "who's ready for promotion", "tier promotion batch", "who should we demote", "annual tier audit", "Gold/Silver/Bronze review".
---

# Tier Promotion Batch Review (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP.
**Use case**: 02 — Partner Segmentation.

## When to use this skill

Use quarterly (or on demand) when a Channel Chief, RevOps, or PDM wants to audit the entire partner base for tier promotion or demotion eligibility — combining revenue, certifications, engagement, and goal attainment — and draft the partner-facing comms for each move.

**Sample prompts that fire this skill:**
- "tier review"
- "who's ready for promotion"
- "tier promotion batch"
- "who should we demote"
- "annual tier audit"
- "Gold/Silver/Bronze review"

## Why this matters
Tier reviews are the most economically consequential ritual in a partner program — they determine margin, MDF eligibility, deal protection priority, and PDM access — and they're also the most commonly **arbitrary or skipped** ritual. Most programs run them once a year, rush the analysis, promote a few favorites, and demote nobody (because nobody wants the conversation). The result: tier inflation that makes the whole tier system meaningless, and partners who *should* have been promoted feeling overlooked.

This skill makes tier reviews **rigorous, consistent, and complete**: every partner gets reviewed against the same criteria; promotions and demotions are evidence-grounded; the comms are drafted so the actual conversation gets had instead of deferred.

## Inputs to gather first
- **Tier definitions**: revenue thresholds, certification requirements, sustained-quarter requirements per tier. Pull from `Introw:get_tier_information` if encoded; else ask.
- **Review window**: trailing 4 quarters (default), trailing 2 quarters (more reactive), trailing year-to-date, custom.
- **Move policy**: do you allow demotion? Do you allow tier-jumps (Bronze → Gold) or only adjacent moves (Bronze → Silver)?
- **Notification policy**: how much advance notice do partners get on demotion (default 60–90 days)?

## Process

### Step 1 — Pull the partner base
- `Introw:search_partners` — full active partner roster with tier, lifecycle stage, categories, region.
- `Introw:get_tier_information` — current tier rules and requirements.
- For each partner, capture current tier and tenure-in-tier.

### Step 2 — Compute eligibility per partner per tier
For each partner, against each tier's requirements:
- **Revenue criteria**: closed-won partner-sourced ARR over the review window. Use `Introw:search_crm_objects` filtered to closed-won and `Introw:search_commissions`.
- **Certification criteria**: required certs present? Use `Introw:search_partner_engagement` for completion records.
- **Engagement criteria**: minimum activity thresholds? Use `Introw:search_partner_engagement`.
- **Goal attainment**: pacing on committed goals? Use `Introw:get_goals`.
- **Sustained-quarter criteria**: were they at this performance level for ≥ N consecutive quarters? Critical to avoid promoting on a single mega-deal.

Score: meets / exceeds / approaches / below for each criterion.

### Step 3 — Generate move recommendations
Bucket each partner:
- **Promote** — meets or exceeds all next-tier criteria, sustained.
- **Hold (target review next quarter)** — approaching next tier, but one criterion lagging.
- **Hold (stable)** — meets current tier squarely; nothing to change.
- **Demote** — falls below current tier criteria, sustained ≥ 2 quarters, not recoverable through near-term intervention.
- **Watch (demotion candidate)** — falls below current tier this quarter only; needs runway + intervention before demotion.

### Step 4 — Apply tier-move guardrails
- No tier-jumps unless policy allows (most programs limit to adjacent moves).
- Demotions require ≥ 2 quarters of underperformance — single-bad-quarter demotions destroy partner trust.
- Notice period applied: demotions get the configured advance notice (e.g., effective in 90 days).
- Any partner with a major in-flight strategic deal gets flagged for human override consideration before demotion.

### Step 5 — Draft per-partner comms
Three templates to generate:

**Promotion comms** (celebratory + concrete unlocks):
- Subject: "Welcome to [Tier], [Partner Name] — and what unlocks for you"
- Lead with the celebration.
- Concretely list new benefits (margin uplift, deal protection upgrades, MDF access, dedicated PDM, etc.).
- Soft close with an invitation to a 30-min call to walk through what changes.

**Demotion comms** (empathetic + path-forward):
- Subject: "[Partner Name] — a heads-up about your tier status and how we get back on track"
- Lead with appreciation for the partnership.
- State the move and the why (specific criteria not met, with numbers).
- Offer a clear path back (what would qualify them for promotion next review).
- Invitation to a CAM call to plan the recovery.
- Effective date with the configured runway.

**Hold-watch comms** (proactive heads-up):
- Subject: "[Partner Name] — staying at [Tier], with one thing to watch"
- Where they stand, what's strong, what's at risk.
- What to focus on this quarter.
- This is the most-skipped category and the highest-leverage one.

### Step 6 — Surface for executive review
- Bundle the recommendations into a reviewable packet:
  - Promotion list (count, ARR represented).
  - Demotion list (count, ARR at risk).
  - Hold-watch list.
  - Override candidates flagged.
- Channel Chief signs off.
- Once approved: schedule comms send (don't auto-send unless explicitly authorized).

### Step 7 — Capture and execute
- For approved moves: `Introw:update_crm_object` to update tier on each partner record.
- `Introw:add_comment` on each partner with the rationale + the criteria scoring.
- `Introw:add_task` for the relevant CAM/PDM to follow up post-comms with a call.
- For any partner where the agent's recommendation was overridden by a human, log the override + reason — feeds rule evolution next cycle.

## Output format
- **Tier review summary**: bucket counts, ARR represented, comparison to last review.
- **Per-partner detail table**: name, current tier, recommended move, criteria scoring, evidence references, drafted comms.
- **Override candidates** with full context.
- **Comms drafts** ready for review.
- **Rule-tightness diagnostic**: criteria that almost nobody meets (probably set too high) or almost everybody meets (probably set too low).

## Guardrails & PRM best practice
- **Sustained performance, not single-quarter.** Promoting on a mega-deal sets the partner up to be demoted next quarter. Use ≥ 2-quarter sustained performance as the bar.
- **Demotions need runway.** Surprise demotions destroy partner trust. Configured notice period (default 60–90 days) with a clear path-back is non-negotiable.
- **No silent moves.** Every promotion and demotion is communicated to the partner with reasoning. Tier moves the partner discovers in the portal six months later are the #1 cause of churn for mid-tier partners.
- **Override transparency.** When channel leadership overrides the agent's recommendation, capture the rationale via `Introw:add_comment`. Pattern overrides should evolve the rules.
- **Tier rules audit.** If the criteria are so loose that 80% of partners are eligible for promotion, the criteria are wrong. If only 1 partner per cycle ever promotes, also wrong. Use this skill's output to surface that diagnostic.
- **No tier inflation.** Resist the temptation to promote across the board to avoid hard conversations. Inflation makes the entire tier system meaningless.
- **Strategic deal protection.** Partners with a major in-flight deal don't get demoted mid-cycle even if the criteria say so — surface for human override.
- **Don't auto-execute.** Surface recommendations + comms drafts; require executive sign-off before any tier change is written or any comms are sent.
- **Capture the audit trail.** Every move must have a comment trail showing the criteria evaluated and the decision rationale. Auditors and disputing partners will ask.
- **Cross-skill handoff.** Promotion candidates who look strong but lag on certifications → `vendor-microcourse-from-closed-lost` or `vendor-training-gap-analysis` to close the gap before next review. Demotion-candidates with recoverable engagement issues → `vendor-activate-network-with-personalized-campaigns` for intervention.
