---
name: vendor-slack-weekly-channel-digest
description: Use when a Channel Chief, Channel Ops, or RevOps user wants to generate the weekly partner-team Slack digest — wins, registrations, at-risk partners, pending approvals, KPI deltas, action items — and post it directly to the channel-team Slack channel. Trigger phrases include "weekly channel digest", "Monday partner update", "post the partner digest", "weekly Slack update", "channel team digest", "what happened with partners this week".
---

# Weekly Channel Slack Digest (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP + **claude.ai Slack** MCP.
**Use case**: 14 — Ecosystem Performance.

## When to use this skill

Use when a Channel Chief, Channel Ops, or RevOps user wants to generate the weekly partner-team Slack digest — wins, registrations, at-risk partners, pending approvals, KPI deltas, action items — and post it directly to the channel-team Slack channel.

**Sample prompts that fire this skill:**
- "weekly channel digest"
- "Monday partner update"
- "post the partner digest"
- "weekly Slack update"
- "channel team digest"
- "what happened with partners this week"

## Why this matters
Most channel teams write their Monday digest by hand: someone opens 5 tabs (CRM, PRM, finance, Slack threads, Linear), copies numbers, paragraphs them up, posts to `#channel-team`. It takes 60–90 minutes and gets skipped half the time. The information ages by Tuesday.

Agentic generation collapses prep to seconds. The digest stops being a chore (and stops getting skipped). The leadership team gets a consistent, current weekly heartbeat. Pair it with `vendor-anomaly-detector` to make the digest predictive — not just retrospective.

## What the digest contains (default sections)

1. **Wins** — closed-won partner-sourced deals this week, with partner attribution.
2. **New registrations** — count, total ARR value, top deals.
3. **Movers** — partners pacing up or down notably vs. prior week (engagement, registration cadence, deal velocity).
4. **At risk** — partners who slipped this week (engagement decay, missed milestones, dormant). Top 3 with suggested intervention.
5. **In the queue** — pending approvals, MDF requests, deal-reg conflicts awaiting resolution. Aging items flagged.
6. **KPI snapshot** — activation rate, partner-sourced pipeline, tier movement, week-over-week deltas.
7. **Anomalies** — anything unusual surfaced by `vendor-anomaly-detector` worth a human eye.
8. **Action items** — top 3–5 things the team should focus on this week, with owners.

User can configure which sections appear, the time window (default trailing 7 days), and which Slack channel to post to.

## Process

### Step 1 — Resolve config
- Default time window: trailing 7 days, ending at run time.
- Default Slack channel: ask the user the first time, then capture.
- Section toggles: ask for any sections to skip (e.g., user only wants Wins + At risk).

### Step 2 — Pull data
- `Introw:search_crm_objects` — closed-won deals + new opps in window (partner-sourced).
- `Introw:search_form_submissions` — new registrations in window.
- `Introw:search_partner_engagement` — engagement deltas vs. prior period.
- `Introw:search_partners` — partner roster + lifecycle states.
- `Introw:search_tasks` — overdue / aging tasks across the team.
- `Introw:search_commissions` — commission events for context.
- `Introw:get_goals` — pacing vs. quarterly goals.
- Optionally: re-use output from `vendor-anomaly-detector` if it ran.

### Step 3 — Compose the digest
Build a Slack-friendly message using Slack's block kit (or simple markdown if user prefers):
- Header block with brand + week-of date range.
- Section blocks for each enabled section.
- Use bullet lists with bold labels.
- Include partner names with hyperlinks back to the partner record in Introw where possible.
- Keep total length under ~3,000 characters — Slack truncates long messages.
- For long sections, summarize in the post + link to a full report.

### Step 4 — Post (or surface for approval)
- **First run**: surface the drafted digest to the user for review. Confirm channel + tone. Don't auto-post.
- **After approval**: post via `Slack:*` to the configured channel.
- For recurring runs (e.g., weekly cron), the user can enable auto-post once the format is dialed in.
- Capture the posted message URL via `Introw:add_comment` on a designated "weekly digest log" record (or a custom CRM object) so the audit trail exists.

## Output format
- **The digest itself** — Slack-formatted message (block kit JSON or markdown).
- **Confirmation**: posted-to channel, message link, timestamp.
- **Variants** for different audiences if requested (e.g., a shorter exec version for CRO Slack).

## Guardrails & PRM best practice
- **Don't auto-post on first run.** Always preview + approve. Tone calibration matters — a digest that misreads sentiment ("celebrating" a partner who just churned) burns trust faster than no digest.
- **Be honest about losses.** If the week was bad, the digest should say so. Sugarcoated digests train the team to ignore them.
- **Names matter.** Cite partners and team members by name (with proper Slack mentions where relevant) — generic "the team" digests get skimmed.
- **Action items must have owners.** "Need to follow up on X" with no name attached doesn't drive action; either assign or remove.
- **Aging is the alarm bell.** Items aging past SLA (approvals > 24h, conflicts unresolved > 48h) get flagged in red — this is the single most useful section for ops.
- **Respect channel volume.** If the channel is high-traffic, default to a shorter format and link out for detail. If it's quiet, the digest is the headline.
- **No partner-confidential data in public channels.** Commission specifics, strategic-account discussions, tier moves — none of those go in `#channel-team` if it's broadly accessible. Use a private channel for those if needed.
- **Don't post during incidents.** If the team is mid-fire (outage, major customer escalation), defer the digest. The skill should ask before posting if the user wants to skip this week.
- **Cross-skill handoff.** Anomaly section feeds from `vendor-anomaly-detector`; KPI snapshot is essentially the standing health check from `vendor-ecosystem-health-check` if installed; at-risk section can hand off to `vendor-activate-network-with-personalized-campaigns` for follow-up.
- **Iterate the format.** After 4 weeks, ask the team what they actually read. Cut the sections that don't get traction. The best digest is the one people open.
