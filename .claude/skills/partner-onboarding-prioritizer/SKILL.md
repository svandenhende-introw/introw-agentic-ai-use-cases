---
name: partner-onboarding-prioritizer
description: Use when a partner is being onboarded by multiple vendors and wants a focused decision on *which onboarding to advance today / this week*, based on commitment dates, economic upside, sunk effort, and current bottleneck. Companion to the cross-vendor onboarding tracker — this one is decision-mode, not status-mode. Trigger phrases include "which onboarding should I focus on", "where should I spend my time", "prioritize my onboardings", "what's highest ROI today", "next move across all my onboardings".
---

# Onboarding Prioritizer (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** with active onboardings.
**Use case**: 03 — Onboarding (partner-side, multi-vendor decision support).

## When to use this skill

Use when a partner is being onboarded by multiple vendors and wants a focused decision on *which onboarding to advance today / this week*, based on commitment dates, economic upside, sunk effort, and current bottleneck. Companion to the cross-vendor onboarding tracker — this one is decision-mode, not status-mode.

**Sample prompts that fire this skill:**
- "which onboarding should I focus on"
- "where should I spend my time"
- "prioritize my onboardings"
- "what's highest ROI today"
- "next move across all my onboardings"

## Why this matters
The cross-vendor onboarding tracker (`partner-cross-vendor-onboarding-tracker`) gives the *status* — what's where with each vendor. This skill answers the harder question: **given that I have 90 minutes today and three open onboardings, which one do I touch first?** Most partners answer by gut. The wrong choice silently kills the most valuable onboarding.

The cost of attention drift on the highest-economic-upside onboarding is non-recoverable: the 90-day first-deal window closes, the partner-side enthusiasm wears off, the relationship drifts into the dormant 80%. This skill prevents that by ranking onboardings by **return-on-next-action**, not by completion percentage.

## Process

### Step 1 — Enumerate active onboardings
- `Introw_Connect_Staging:partners` — get all portals.
- For each portal, determine if onboarding is active (lifecycle stage = onboarding, or first-deal not yet registered, or onboarding tasks still open).
- Filter to onboardings actively in flight; skip ones already activated or aged out.

### Step 2 — Pull decision inputs per portal
Per active onboarding:
- `Introw_Connect_Staging:search_tasks` — open tasks + their due dates + the next milestone.
- `Introw_Connect_Staging:get_goals` — any onboarding-stage goals + pacing.
- `Introw_Connect_Staging:search_partner_engagement` — recent activity (signal of momentum vs. drift).
- `Introw_Connect_Staging:get_tier_information` — what completing onboarding unlocks (margin, MDF, deal protection, dedicated PDM).
- `Introw_Connect_Staging:search_crm_objects` — first deal status (in pipeline / not yet).

### Step 3 — Score each onboarding on the prioritization axes

- **Urgency**: days remaining to the 90-day cliff. Closer = higher priority.
- **Economic upside at activation**: tier benefits unlock value (margin uplift × expected pipeline volume in this vendor's segment for the partner).
- **Sunk effort**: how far in already (don't waste 60% complete onboardings — but don't keep pushing dead ones).
- **Effort to next unlock**: an onboarding 1 task from a tier benefit is high-ROI vs. 8 tasks from anything.
- **Momentum**: recent engagement vs. drift. Onboardings that have stalled need a momentum-restart move (a CAM ping, a first registration), not more tasks.
- **Relationship strategic weight**: vendors more central to the partner's portfolio (more pipeline / more existing customers) earn higher weighting.

### Step 4 — Compute Return-on-Next-Action
For each onboarding, the question is: *if I spend 1 hour on this today, what's the marginal value?* That's:
- **(Economic upside at activation × probability the action moves activation forward) ÷ (effort of the action)**

Rank by ROI of next action. Top 1–3 are the focus list.

### Step 5 — Recommend the specific next action per top-ranked onboarding
For each:
- **The action** in concrete terms ("Register your first deal — Account X is closest in your pipeline. Vendor Y's first-deal protection unlocks ~€8K margin").
- **The unblock**: if the action is gated by a missing task / cert / asset, surface that.
- **Effort estimate** (10 min / 1 hr / 1 day).
- **What it unlocks immediately**.

### Step 6 — Surface stall-recovery moves
Some onboardings are stalled — engagement decay, no recent activity. For those:
- Recommend a momentum-restart move (CAM ping with drafted message; small first deal to unlock first-deal status).
- Or recommend honest abandonment if the math doesn't justify continuing (some vendor relationships aren't going to be productive — surface that conclusion).

## Output format
- **Today's focus list** — top 1–3 onboardings, each with the specific next action + effort + payoff.
- **Stall-recovery moves** — onboardings that need a momentum reset.
- **Honest skip list** — onboardings where ROI doesn't justify continuing (with rationale).
- **Aggregate context** — total onboardings active, total ARR potential at full activation, weeks of attention "owed" given current pacing.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each onboarding's data is fetched with its own `roomId`. No cross-portal data leakage.
- **Don't shame.** If the partner has 5 stalled onboardings, the framing isn't "you've been failing at this." It's "here's the highest-ROI single move you could make today." Action-bias, not judgment.
- **Honest about diminishing returns.** Some onboardings should be deprioritized — and saying that explicitly is more useful than implying it. If the math says "skip Vendor Z this quarter," surface it cleanly.
- **Effort honesty.** A 10-minute action ranks higher than a 4-hour action with similar payoff. Surface effort estimates honestly.
- **Don't ignore strategic weight.** A vendor with smaller per-deal margin but huge customer-base overlap may rank higher than a high-margin vendor with no customer fit.
- **Capture the decision.** When the partner picks a focus, log via `add_comment` so future runs see the trail.
- **Update on cadence.** This skill is meant to run weekly (or daily during high-onboarding load). Once-a-quarter usage misses the point.
- **Cross-skill handoff.** Once the partner commits to a focus and starts the action: status-mode → `partner-cross-vendor-onboarding-tracker`. Stuck-in-cert-gating → `partner-cross-vendor-cert-tracker`. First-deal motion → `partner-deal-war-room` to coach the deal forward.
