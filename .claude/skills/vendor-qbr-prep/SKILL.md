---
name: vendor-qbr-prep
description: Use when a PDM, CAM, or Channel Chief wants to prepare a Quarterly Business Review (or MBR / WBR) — instantly assembling pipeline, goals, activity, engagement, commissions, MAP status, and a recommended agenda for one partner OR running a 100% coverage sweep across the entire partner book. Trigger phrases include "prep QBR for [partner]", "generate this quarter's QBRs", "QBR sweep across the book", "MBR / WBR prep", "100% QBR coverage", "ready every partner review", "quarterly business review preparation".
---

# QBR Preparation: Single-Partner & Book-Wide Coverage (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP.
**Use case**: 12 — QBRs / Meeting Prep.

## Why this matters
PDMs spend **2–4 hours per QBR** on manual data assembly. A 30-partner book × 4 quarterly reviews = **240–480 hours/year per PDM** of mechanical prep — before the actual meeting, follow-up, or strategic conversation. The honest reality: most programs only achieve **20–30% real QBR coverage** because the prep math makes 100% impossible. Top-tier partners get full reviews, mid-tier get half-baked versions, and the long tail gets a check-in email.

Agentic generation collapses prep to **~10 seconds** for the full draft + **~15 minutes** of PDM editing for strategic refinement. The math reverses: **100% coverage** becomes feasible. Time recovered per PDM: **250–500 hours/year** redirected from spreadsheet wrangling to the strategic conversation, recommendation, and decision work that humans uniquely do well.

This skill operates in two modes — single-partner prep, or a book-wide coverage sweep.

## Modes

### Mode A — Single-partner QBR prep
Generate a complete QBR draft for one named partner.

### Mode B — Book-wide coverage sweep
Generate QBR drafts for every partner in the user's book (or a defined cohort), one per partner, ready for 15 minutes of editing each. The defining outcome: every partner gets the same data depth — Gold to long-tail — and coverage hits 100%.

## Inputs to gather
- **Mode** (A or B).
- **Partner** (Mode A) or **cohort scope** (Mode B — book, tier, region).
- **Review type**: QBR (default), MBR, WBR.
- **Time window**: trailing quarter (default), trailing month, custom.
- **Audience**: PDM-internal review or joint partner-facing review (changes tone).

## Process

### Step 1 — Try the dedicated tool first
`Introw:generate_business_review` is purpose-built — call it with the partner ID and review type. For Mode B, iterate across the cohort.

### Step 2 — Enrich with current state
For each QBR, pull current state from connected systems:
- `Introw:search_crm_objects` — open pipeline, recent closed-won, slipped/lost deals, deal velocity vs. cohort.
- `Introw:get_goals` — goal targets and progress (MBOs, certification targets, quarterly commitments).
- `Introw:search_partner_engagement` — engagement intensity over the period (meetings, training, content engagement, asset views).
- `Introw:search_commissions` — paid, accrued, projected.
- `Introw:get_tier_information` — current tier, distance to next tier, tier benefits.
- `Introw:search_tasks` — open, completed, overdue.
- `Introw:search_form_submissions` — registration cadence, MDF requests.

### Step 3 — Assemble the standard QBR sections
Every QBR includes:

1. **Executive summary (3 bullets)** — state of the partnership, biggest win, biggest risk.
2. **Pipeline & revenue** — quarter actuals vs. plan, top deals, expansion opportunities, slipped deals with reasons.
3. **Goals & MAP** — progress on committed goals, MAP / joint-plan milestones (complete / blocked / due), quarterly commitments status.
4. **Activity & engagement** — registrations submitted, training completed, events attended, content engaged, partner engagement score vs. cohort benchmark.
5. **Tier trajectory** — current tier, run-rate to next tier, gap analysis, what unlocks at promotion.
6. **Commissions** — paid, accrued, projected, any aging payables flagged.
7. **Action items** — top 3–5 for next quarter with owners and dates.
8. **Recommended agenda** — 3–5 priority topics surfaced from the data, with talking points the PDM can carry into the live meeting.

### Step 4 — Surface risks and opportunities at the top, not buried
Auto-flag (in the executive summary):
- Aging commissions or payable disputes.
- Goal pacing behind run-rate.
- Engagement decay over the period.
- Stuck pipeline / aging deals.
- MAP commitments slipping.
- Tier trajectory at risk of demotion.

### Step 5 — Mode B specifics: coverage sweep mechanics
For book-wide:
- Iterate the partner cohort (default: every active partner the user manages).
- Generate one QBR draft per partner.
- Bundle the drafts in a clean order: high-touch (top tier / strategic) first, transactional last.
- Surface a coverage scorecard: how many drafts, average data quality, partners with thin data (where the QBR may be light).
- Flag any partners where data quality is too low to ship a meaningful QBR — those need PDM input before generation runs.

### Step 6 — Capture & hand off
- `Introw:add_comment` on each partner record — note that the QBR was generated and which sections required strategic editing.
- For action items in each QBR, optionally `Introw:add_task` to create trackable follow-ups with owners and dates.
- The QBR draft is ready for the PDM's 15-minute strategic edit pass.

## Output format
- **Mode A**: one complete QBR markdown draft, sectioned, copy-pasteable into slides / docs.
- **Mode B**: one draft per partner + a coverage scorecard showing book-wide coverage status.
- **Risk flags** highlighted at top, not buried.
- **Comparison to last QBR** if data available.
- **Action item list** separate from the QBR body, ready for tasking.

## Guardrails & PRM best practice
- **The 15-minute edit is the value.** PDMs personalize before delivery — the agent generates the scaffold; humans add the relationship intelligence. Don't ship un-edited.
- **One source of truth.** Every number in the QBR traces to a specific tool call. Don't paraphrase metrics; if the data isn't there, flag it as such rather than fabricating.
- **MAP honesty.** If MAP commitments are slipping, surface them — soft-pedaling the joint plan in QBRs is the #1 reason joint plans fail to deliver.
- **No surprises.** Risks in the QBR should have been raised in the trailing month via comments — use `Introw:add_comment` to log risks as they emerge, not just at quarter-end.
- **Tier-trajectory transparency.** Show the partner the path to the next tier even if they're far. Opacity here is a top trust eroder.
- **Coverage discipline.** Encourage Mode B for full books — agentic prep makes 100% feasible; lower-tier partners often deliver the biggest delta from a QBR they wouldn't otherwise receive. The economics of partial coverage are a self-inflicted constraint.
- **Quality consistency.** Every partner — Gold to long-tail — gets the same data depth in their review. Tier should affect strategic emphasis, not data thoroughness.
- **Tone awareness.** Internal-PDM-prep mode and joint-partner-facing mode are different documents. Ask which one is being generated; default to internal prep if unclear.
- **Don't replace the human in the meeting.** Automation replaces the *prep*, not the conversation. Frame outputs as PDM-ready drafts.
- **Pair with adjacent skills.** Coverage sweep that surfaces an at-risk partner → `vendor-detect-at-risk-partners` and `vendor-activate-network-with-personalized-campaigns`. QBR finds a coaching gap → `vendor-deal-coach-from-similar-wins`. QBR shows training gap → `vendor-microcourse-from-closed-lost`.
- **Do the work the PDM would want done, not just possible.** Surface the strategic question hiding in the data, not just the data.
