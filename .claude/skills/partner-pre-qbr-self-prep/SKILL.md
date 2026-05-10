---
name: partner-pre-qbr-self-prep
description: Use before a partner heads into a QBR / MBR with a vendor — generates the partner's *own* data view (deals sourced, engagement, training, goals progress, asks to bring up, the partner's own scorecard of how the vendor has been performing as a partner) so the partner walks in with their own narrative, not just the vendor's slides. Trigger phrases include "prep my QBR", "I have a QBR with [vendor]", "what should I bring up in the QBR", "my QBR data", "pre-meeting prep with vendor", "partner-side QBR prep".
---

# Pre-QBR Self-Prep (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP. Single-vendor scope per invocation (the QBR is with one vendor).
**Use case**: 12 — QBRs / Meeting Prep.

## When to use this skill

Use before a partner heads into a QBR / MBR with a vendor — generates the partner's *own* data view (deals sourced, engagement, training, goals progress, asks to bring up, the partner's own scorecard of how the vendor has been performing as a partner) so the partner walks in with their own narrative, not just the vendor's slides.

**Sample prompts that fire this skill:**
- "prep my QBR"
- "I have a QBR with [vendor]"
- "what should I bring up in the QBR"
- "my QBR data"
- "pre-meeting prep with vendor"
- "partner-side QBR prep"

## Why this matters
QBRs are usually run *to* the partner, not *with* them. The vendor's PDM walks in with prepared slides, owns the agenda, and frames the conversation. The partner shows up reactively — answering questions about pipeline, hearing concerns, taking notes. The result is QBRs that miss the partner's perspective entirely: their constraints, their wins with this vendor's product they want to celebrate, their asks (more MDF, deal-protection extension, tier promotion, lead share, regional support), and their honest read on how the vendor is treating them as a partner.

This skill flips that. Before the QBR, the partner gets their own data view + drafted talking points. They walk in with their own narrative and asks. The QBR becomes a real two-way review instead of a vendor-led report-out.

## Process

### Step 1 — Resolve the portal
- If the partner has access to multiple vendor portals, call `Introw_Connect_Staging:partners` and confirm which vendor's QBR this is for. **Single vendor per invocation.**

### Step 2 — Pull the partner's own performance with this vendor
- `Introw_Connect_Staging:search_crm_objects` — partner-sourced deals (closed-won, in-flight, slipped, stalled) over the review period.
- `Introw_Connect_Staging:search_form_submissions` — registrations submitted, with status (approved, pending, rejected, conflict).
- `Introw_Connect_Staging:search_partner_engagement` — engagement intensity over the period.
- `Introw_Connect_Staging:search_tasks` — open + completed tasks (training, MAP commitments).
- `Introw_Connect_Staging:get_goals` — committed goals + progress.
- `Introw_Connect_Staging:search_commissions` — commissions earned, paid, accrued, pending — and any disputes.
- `Introw_Connect_Staging:get_tier_information` — current tier + distance to next tier.

### Step 3 — Compute partner's-eye-view metrics
Build the partner's narrative:

- **What we sourced this quarter** — count, ARR, breakdown by product / vertical / region.
- **What we closed** — wins, with the case studies behind them (so the partner can name-drop in the QBR).
- **What stalled / lost** — and a partner-side read on why (vendor's pricing? competitor? lack of vendor support?).
- **Our pipeline trajectory** — what's coming, when, deal-protection coverage, support needs.
- **Our investment in the vendor** — training completed, certs earned, events attended.
- **Goal pacing** — on track / behind / ahead of committed goals.
- **Our financial picture with this vendor** — commissions earned, payment timeliness, disputes.

### Step 4 — Compute the partner's "vendor scorecard"
The honest part — how is this vendor performing as a *partner* to me? Score:

- **Approval responsiveness**: avg days to deal-reg approval, MDF approval, conflict resolution.
- **Lead share generosity**: leads passed to me + their conversion rate.
- **Pricing flexibility**: deal exceptions granted vs. requested.
- **Field support quality**: SE / pre-sales availability when I asked.
- **Payment timeliness**: on-time vs. aged payable.
- **Communication quality**: PDM responsiveness, info flow on launches.

This isn't to attack the vendor — it's to give the partner data to bring up specific friction with concrete asks ("approvals took avg 5 days this quarter, would help to get under 2 days").

### Step 5 — Surface the asks
Based on the data, identify what the partner should bring up:

- **Tier promotion ask** — if pacing strong but tier not yet moved.
- **Deal protection extensions** — for slipping deals where the protection window is closing.
- **MDF asks** — campaigns the partner wants to fund.
- **Lead share asks** — segments where the partner has capacity.
- **Pricing flexibility** — for specific in-flight deals where pricing is the blocker.
- **Field support** — vendor SE engagement on strategic deals.
- **Process improvements** — based on the scorecard's pain points.
- **New product / vertical interest** — if the partner sees an opportunity to expand the partnership.

### Step 6 — Draft the partner's narrative
Generate a 3–5 minute opening the partner can use in the QBR (or just structure their notes):

- **What worked** (1–2 wins to celebrate, named).
- **Our investment** (concrete numbers — registrations, certs, events).
- **What stalled and why** (honest, blame-shared where appropriate).
- **What we're asking for** (the specific list, in priority order).
- **What's coming** (pipeline framing, with numbers).

Tone: collaborative, data-grounded, asks specific things. Not a complaint list, not a victory lap.

## Output format
- **Partner performance dashboard** — sourced/closed/in-flight, cert/training, engagement, goal pacing.
- **Partner's vendor scorecard** — how the vendor performed for this partner this quarter.
- **Asks list** — prioritized, with data backing each.
- **Drafted QBR opening** — copy-pasteable, 3–5 minutes spoken.
- **Talking points for the agenda** — bullet-pointed, in case the vendor leads with their slides.
- **Watch-outs** — anything the partner should be ready to be asked about that the vendor will likely raise.

## Guardrails & PRM best practice
- **Single-vendor scope.** The QBR is with one vendor; the data view is scoped to that portal. Don't blend in other vendors' data.
- **Honest, not adversarial.** The vendor scorecard is for the partner's planning. Bring up specific friction with specific data — but frame asks as *partnership investments*, not complaints.
- **Don't surface other partners' data.** Even when the partner can see vendor-aggregate stats, don't quote other partners' numbers in the QBR — destroys the vendor's trust.
- **Strategic > comprehensive.** Pick 2–3 asks, not 12. A QBR isn't a wishlist; it's a focused conversation.
- **Pre-empt vendor concerns honestly.** If you have stalled deals the vendor will flag, address them in your own opening — don't make the vendor raise it first.
- **Tier-trajectory transparency.** If the partner is far from a tier promotion, don't manufacture a request that won't land. Use the data.
- **Capture commitments made.** After the QBR, the vendor may run `vendor-qbr-recording-to-portal-followup` (if installed). The partner should also log their own takeaways via `Introw_Connect_Staging:add_comment` — gives the partner-side audit trail.
- **Don't draft the vendor's responses.** The partner's prep is the partner's prep. Speculating on what the vendor will say is unhelpful.
- **Cross-skill handoff.** Stalled deals identified during prep → `partner-deal-war-room`. Cert-ask asks → cross-check via `partner-cross-vendor-cert-tracker`. Renewal/expansion deals to surface → `partner-renewal-and-expansion-coordinator` (if installed).
