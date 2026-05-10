---
name: vendor-activate-network-with-personalized-campaigns
description: Use when a Channel Chief, PDM, RevOps, or Channel Ops user wants to run a full activation sweep across the entire partner network — auditing every partner against their goals, identifying who needs activation, and generating per-partner personalized activation campaigns whose messaging maps to each partner's specific goals and gap. Trigger phrases include "activate the network", "who needs activation", "personalized activation campaigns", "audit and activate", "partner activation sweep", "fix the long tail".
---

# Activate the Network with Personalized Campaigns (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP.
**Use case**: 04 — Activation.

## Why this matters
Industry baseline activation: **30–50%** for managed programs, **below 20%** unmanaged. Half or more of every recruitment dollar produces zero pipeline because partners drift through onboarding without registering deals — and nobody notices until quarterly reporting. Lifting activation 30% → 50% on the same intake = **67% more productive partners** ≈ **€10M incremental sourced ARR per 100-partner cohort**. Reactivation after disengagement is dramatically more expensive than catching the drop-off early — re-engagement flows can lift dormant activity from ~4% to 12% (ReferralCandy), but prevention beats reactivation by an order of magnitude.

This skill is a **workflow**, not a query. It audits the entire network, scores activation state per partner, and generates campaigns where each partner gets messaging tied to their *specific goals* — not a generic "we miss you" blast.

## Process

### Step 1 — Define the audit scope
Default: every active partner, including freshly onboarded. Confirm with the user. Optional scoping: tier, region, partner type, time-since-onboarding.

### Step 2 — Pull network-wide signals
- `Introw:search_partners` — full partner list with tier, region, lifecycle stage.
- `Introw:get_goals` — committed goals per partner (KEY: this skill's personalization hinges on goal data).
- `Introw:search_crm_objects` — pipeline state and recent registrations per partner.
- `Introw:search_form_submissions` — last registration / lead share timestamp.
- `Introw:search_partner_engagement` — engagement intensity over 30/60/90-day windows.
- `Introw:search_tasks` — overdue / aging tasks per partner.
- `Introw:get_tier_information` — what each partner's current tier expects of them.
- `Introw:search_commissions` — earned vs. expected as a performance proxy.

### Step 3 — Score every partner
Apply a multi-signal score per partner:
- **Activated** — first deal registered or closed within 90 days of onboarding.
- **Pacing** — on track for committed goals (`get_goals` progress vs. target run-rate).
- **Stalled** — completed onboarding, zero deal activity in 30/60/90 days.
- **Dormant** — was active, dropped off (declining engagement, no recent registrations).
- **At risk** — engagement decay + missed milestone but recoverable.

### Step 4 — Diagnose *why* per partner
Don't just bucket — identify the specific blocker for each non-activated partner:
- **Capability gap** — never completed key training/cert.
- **Lead drought** — no inbound or warm leads to act on.
- **Stuck pipeline** — has open opportunities not advancing in 14+ days.
- **Goal mismatch** — partner's stated goals don't match what the program is enabling them on.
- **Stakeholder gap** — primary contact left; relationship orphaned.
- **Channel preference miss** — vendor pushed via email; partner lives in Slack.
- **Margin / incentive friction** — recent commission dispute or rate-perception issue.

### Step 5 — Generate per-partner personalized activation campaigns
For each non-activated partner, build a campaign whose messaging maps to **their specific goals** and **their specific blocker**:

- **Subject / hook** — references the partner's stated goal (from `get_goals`) and their tier or vertical.
- **Joint-value framing** — concretely articulates what activating produces for *them*: deal-protection margin (10–15 pts), MDF access, pre-sales support, tier-progression unlocks.
- **Asset / next step** — directly tied to the diagnosed blocker:
  - Capability gap → micro-course nudge.
  - Lead drought → warm lead share via `Introw:share_lead_or_register_deal`.
  - Stuck pipeline → deal coaching invite (hand off to `vendor-deal-coach-from-similar-wins` or `vendor-coach-partner-deal`).
  - Stakeholder gap → CAM intro to a new contact.
  - Channel preference miss → re-deliver via the partner's preferred channel.
  - Margin friction → CAM call to address.
- **CTA** — one specific action, with the next-step link or task.
- **Tone** — partner-type-aware (transactional for SMB resellers, strategic for enterprise SIs, educational for new partners).

### Step 6 — Distribute and track
- Push messages via the partner's preferred channel (email / Slack / Teams / portal).
- Use `Introw:add_task` to create CAM follow-ups for high-touch partners (top tier, strategic).
- Use `Introw:add_comment` on the partner record to capture the activation attempt for the audit trail.
- Schedule a re-audit window (default 14 days) to measure campaign-driven activation lift via `Introw:search_partner_engagement` and `search_form_submissions`.

## Output format
- **Network audit summary**: counts by bucket (Activated / Pacing / Stalled / Dormant / At risk).
- **Stalled & dormant table**: partner, tier, days since last engagement, diagnosed blocker, recommended intervention.
- **Per-partner campaign drafts**: hook, body, CTA, channel — copy-pasteable.
- **Distribution plan**: who gets what, when, via which channel, with which CAM owner.
- **Re-audit schedule**: when to measure activation lift.

## Guardrails & PRM best practice
- **Goal-driven, not generic.** If you can't tie a campaign's framing to a partner's specific goal from `get_goals`, the campaign isn't personalized — it's a blast in disguise. Push back rather than ship a generic version.
- **Diagnose before prescribing.** A campaign that nudges a "training-completed-no-leads" partner to do more training will accelerate disengagement, not fix it. Match the intervention to the diagnosed blocker.
- **Don't blast the whole network at once.** Partners talk; if the activation cadence reads as automated, trust collapses. Stagger campaigns and respect engagement saturation.
- **Tier-fairness with effort-tiering.** Top-tier strategic partners get a CAM call recommendation, not a templated email — even when the message would otherwise be the same.
- **Action over commentary.** Every flag carries a next-best action. A list without prescriptions creates fatalism.
- **Capture the loop.** Every campaign send + every response routes through `Introw:add_comment` on the partner record so the next quarter's QBR has the trail.
- **Channel preference is sacred.** Pushing in the wrong channel reads as "doesn't know me" — exactly the message activation should *not* send.
- **Don't down-tier or deactivate from this skill.** Activation surfaces and prescribes; tier moves and program decisions go through governance.
- **Pair with other skills.** Hand off cleanly: blocked-on-coaching → `vendor-deal-coach-from-similar-wins`; blocked-on-training → `vendor-microcourse-from-closed-lost` or `vendor-training-gap-analysis`; blocked-on-onboarding → `vendor-onboarding-progress-audit`.
