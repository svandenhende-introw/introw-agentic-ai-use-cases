---
name: partner-incentive-maximizer
description: Use when a partner user wants to know exactly which actions to take this quarter to maximize commission earnings, hit the next bonus tier, or unlock the next accelerator. Pulls live goals, commissions, and pacing data, then prescribes specific high-leverage moves. Trigger phrases include "how do I maximize my earnings", "what should I focus on this quarter", "how close to the bonus", "next tier unlock", "incentive plan for me", "where's the easiest commission left".
---

# Incentive Maximizer (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP.
**Use case**: 13 — Commissions & Incentives.

## When to use this skill

Use when a partner user wants to know exactly which actions to take this quarter to maximize commission earnings, hit the next bonus tier, or unlock the next accelerator. Pulls live goals, commissions, and pacing data, then prescribes specific high-leverage moves.

**Sample prompts that fire this skill:**
- "how do I maximize my earnings"
- "what should I focus on this quarter"
- "how close to the bonus"
- "next tier unlock"
- "incentive plan for me"
- "where's the easiest commission left"

## Why this matters
Most partner programs publish their commission and tier rules and assume partners optimize behavior accordingly. They don't — partners are running their own businesses, juggling multiple vendors, and often don't have time to model "what would maximize my earnings with Vendor X this quarter." The result: partners leave money on the table, and the vendor's incentive design under-performs.

This skill closes the gap by doing the math the partner would do if they had time: where's the closest threshold, what activity moves the needle, and what specific deals or plays would unlock the next chunk of earnings. **Transparency multiplied by prescription** — the partner-side companion to the vendor's commission analytics.

## Process

### Step 1 — Resolve the portal
If the partner has access to multiple vendor portals, call `Introw_Connect_Staging:partners` first to get available portals. Confirm which `roomId` to use.

### Step 2 — Pull the partner's full incentive context
- `Introw_Connect_Staging:get_tier_information` — current tier, all tier definitions, what each unlocks (margin %, MDF, deal protection, accelerator multipliers).
- `Introw_Connect_Staging:get_goals` — committed goals, targets, progress, time remaining in the period.
- `Introw_Connect_Staging:search_commissions` — paid, accrued, pending; commission rate currently in effect.
- `Introw_Connect_Staging:search_crm_objects` — open deals (stage, value, close date, products) — these are the candidates for moving the needle.
- `Introw_Connect_Staging:search_form_submissions` — recent registration cadence.

### Step 3 — Compute earnings-impact per next-step action
For each plausible action the partner could take, estimate the marginal earnings impact:

- **Close deal X already in pipeline** — value × commission rate × tier multiplier. Sort open deals by EV (probability × value × marginal commission impact).
- **Register N more deals before period end** — for partners with a registration-volume bonus.
- **Hit the next tier threshold** — gap to next tier × what the next tier unlocks (if Gold gives 5 pts more margin on all subsequent business, that's a multi-quarter unlock, not just this quarter).
- **Hit a goal threshold** — for partners pacing close to a goal that triggers a bonus.
- **Activate a SPIF / accelerator** — currently active SPIFs and what they require (e.g., "+10% on healthcare deals over €50K closed before quarter-end").
- **Complete a certification that gates a higher-margin product** — for partners blocked from a higher-margin SKU by a missing cert.

### Step 4 — Identify the highest-leverage moves
Rank the actions by:
- **Earnings impact** — actual € or % uplift.
- **Probability** — how achievable in the time remaining? (A deal at Stage 4 with 30 days left is high; a deal at Stage 1 is wishful.)
- **Effort** — relative effort vs. the partner's normal motion. (Closing a deal already in late stages is low-effort; recruiting a new logo from scratch is high.)

Score each action: impact × probability ÷ effort. Top 3–5 surface as the recommendation.

### Step 5 — Frame for action
Each recommendation includes:
- **The action** in concrete terms ("Close deal Globex by 30 March — currently at Stage 4, est. €120K").
- **The earnings impact** ("Adds €18K to your Q3 commission at your current rate; pushes you across the €500K threshold for Gold-tier eligibility next review").
- **Why it's leverageable** ("This deal is in the segment where your historical win rate is 65%; same partner closed a similar one last quarter").
- **What you need to unblock it** (link to deal-coaching skill if stuck, link to register-deal skill if not yet registered, link to CAM if executive engagement needed).

### Step 6 — Surface the dashboard view
Provide a single-glance summary:
- **Current period earnings**: paid / accrued / projected.
- **Distance to next tier**: revenue gap, certs gap, time remaining.
- **Distance to next bonus / accelerator threshold**.
- **Active SPIFs you're eligible for**: list with requirements.
- **Top 3 next moves** ranked.

## Output format
- **Earnings dashboard** (current + projected + thresholds).
- **Top 3 recommendations** with concrete actions, impact, and unblock paths.
- **Active SPIFs / accelerators** the partner is eligible for, with requirements.
- **Certification gaps** that gate higher-margin products.
- **Direct links** to the relevant follow-up actions (deal coaching, registration, CAM call).

## Guardrails & PRM best practice
- **Strict scope.** Only this partner's data — never reference other partners' commissions, deals, or rates.
- **Don't promise outcomes.** Projections are estimates based on current pacing and stated probabilities. Always frame as "if you close deal X by date Y, this is the impact" — not "you will earn €Z."
- **Vendor rules are vendor rules.** Don't speculate about commission rate changes or tier eligibility being lowered. Refer rate questions to the partner's CAM.
- **Surface, don't pressure.** The skill prescribes; the partner decides their priorities. Vendor-side incentives shouldn't override the partner's strategic considerations.
- **Be honest about probability.** Suggesting a partner can close 5 stage-1 deals in 14 days to hit a threshold isn't realistic — flag low-probability paths as low-probability.
- **Multi-vendor reality.** The partner has other vendors competing for their attention. Recommendations should be honest about effort — high-effort recommendations need real impact to be worth it.
- **No self-dealing.** Don't recommend actions that benefit only the vendor (e.g., "register deals you're not really pursuing to hit volume thresholds"). Recommendations should be in the partner's actual interest.
- **Capture the conversation.** If the partner takes one of the recommended actions (close X, register Y), use `Introw_Connect_Staging:add_comment` on the relevant record to log the connection — gives the vendor's team context for the next QBR.
- **Refresh frequency.** Quarterly is too slow — monthly check-ins are more useful in the back half of a quarter when small moves still matter. Weekly in the final 30 days of a quarter for partners close to a threshold.
- **Cross-skill handoff.** Stuck deals → `partner-coach-my-deal`. Net-new registrations → `partner-register-deal`. Tier/goal status check-in → `partner-my-tier-and-goals` (if installed). Commission status → `partner-my-commissions` (if installed).
