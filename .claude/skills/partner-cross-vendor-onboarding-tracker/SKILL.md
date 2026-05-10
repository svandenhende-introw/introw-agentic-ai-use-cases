---
name: partner-cross-vendor-onboarding-tracker
description: Use when a partner user is being onboarded by multiple vendors and wants a single aggregated view of progress, open tasks, milestones, and time-to-first-deal across every vendor portal they have access to. Trigger phrases include "onboarding status across vendors", "where am I with each vendor", "all my onboardings", "cross-vendor onboarding progress", "what do I owe each vendor", "vendor onboarding scoreboard".
---

# Cross-Vendor Onboarding Tracker (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the user has access to.
**Use case**: 03 — Onboarding (partner-side, multi-vendor aggregation).

## When to use this skill

Use when a partner user is being onboarded by multiple vendors and wants a single aggregated view of progress, open tasks, milestones, and time-to-first-deal across every vendor portal they have access to.

**Sample prompts that fire this skill:**
- "onboarding status across vendors"
- "where am I with each vendor"
- "all my onboardings"
- "cross-vendor onboarding progress"
- "what do I owe each vendor"
- "vendor onboarding scoreboard"

## Why this matters
A typical reseller / SI / MSP is being onboarded by 3–10 vendors at any given time. Each vendor has its own portal, its own checklist, its own CAM, its own "what's next" framing. The partner has zero unified view — and the natural result is that *some* of those onboardings stall (often the most economically valuable one), because the partner just runs out of attention. This skill solves that by aggregating across portals: one screen, all open onboardings, ranked by what to do next.

Partners who close their first deal within 90 days are **3–4× more likely** to remain active (Unifyr Channel Atlas) — applying that benchmark across multiple vendors compounds the cost of attention drift.

## Process

### Step 1 — Enumerate portals
- Call `Introw_Connect_Staging:partners` to get the full list of portals this user has access to. Capture `roomId`, vendor name, partner record ID per portal.
- If the user is in just one portal, this skill still works — but the value is highest with 2+.

### Step 2 — Pull onboarding state per portal
For each `roomId`, in parallel where possible:
- `Introw_Connect_Staging:search_tasks` (with that `roomId`) — open and recently completed onboarding tasks.
- `Introw_Connect_Staging:get_goals` — onboarding-stage goals and progress.
- `Introw_Connect_Staging:search_partner_engagement` — recent activity + the cadence vs. the partner's baseline with that vendor.
- `Introw_Connect_Staging:search_form_submissions` — first-deal registration if any.
- `Introw_Connect_Staging:search_crm_objects` — first deal in pipeline if any.
- `Introw_Connect_Staging:get_tier_information` — what onboarding completion unlocks for this vendor.

### Step 3 — Compute per-vendor onboarding state
For each vendor:
- **% complete** (tasks done / tasks total).
- **Days since onboarding start.**
- **Days to 90-day cliff** (the activation window).
- **First deal status**: not yet, in pipeline, registered, closed.
- **Top blockers**: tasks overdue, missing certifications, missing assets/contacts.
- **What unlocks next**: deal protection, MDF eligibility, tier benefits, dedicated PDM access.
- **Risk flag**: stalled (engagement decay + missed milestones), at-risk (slipping), on track, near activation.

### Step 4 — Rank for partner attention
Surface vendors in priority order based on:
- **Urgency**: closeness to the 90-day cliff (first-deal window).
- **Economic upside**: tier benefits at completion (margin uplift, MDF access).
- **Sunk effort**: how far in already (don't waste 60% complete onboardings).
- **Effort to next unlock**: a vendor 1 task from a tier promotion is high-ROI vs. one with 8 tasks remaining.

The partner sees a clear "do this next, then this, then this" recommendation across the whole onboarding portfolio.

## Output format
- **Cross-vendor onboarding scoreboard** — table with vendor, % complete, days-in, first-deal status, top blocker, next unlock, risk flag.
- **Today's recommended actions** — top 3 highest-ROI moves, each tagged with which vendor and which `roomId`.
- **At-risk callouts** — any vendor onboarding where the 90-day cliff is approaching without first-deal traction.
- **Stalled escalation suggestions** — where to ping the CAM (with drafted message) to unstick.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each portal's data is fetched only with that portal's `roomId` — no cross-portal data leakage.
- **Don't compare vendors competitively to each other in the output.** It's the partner's view; it's fine to rank for attention. But framing like "Vendor X is treating you better than Vendor Y" is messy and risks leaking into vendor-facing comms.
- **Time-bound every signal.** "Stalled" without a window is meaningless; always state the days since last activity.
- **Honor stated constraints.** If the partner has already told a specific vendor they're slow this quarter, don't re-flag the same delay as "at risk" — capture context once via `add_comment` to that portal.
- **Action over commentary.** Every flag carries a next-best move. Don't list problems without prescriptions.
- **First-deal gravity.** Across all vendors, prioritize first-deal motion in vendors past day 60 — that's where the economics flip.
- **Capture the loop.** When the partner takes a recommended action, log via `Introw_Connect_Staging:add_comment` on the relevant portal so the next run sees the progression.
- **Cross-skill handoff.** Decision-style "where do I focus today?" → `partner-onboarding-prioritizer`. Stuck onboarding → `partner-helpdesk` to find the answer or escalate. First-deal motion → `partner-register-deal` (if installed) or `partner-deal-war-room`.
