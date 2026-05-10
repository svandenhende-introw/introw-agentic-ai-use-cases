---
name: partner-deal-war-room
description: Use when a partner seller is working a specific deal and wants a comprehensive coaching packet — vendor playbook for the stage, similar past wins, competitive battle cards, reference customers, objection handling, suggested next moves — pulled live from the relevant vendor portal(s). The partner-side counterpart to the vendor's deal-coaching skills. Trigger phrases include "war room for this deal", "coach me on [deal]", "what do I do next on [account]", "how have we won deals like this", "objection handling for [deal]", "competitive position on [deal]", "draft the next message".
---

# Deal War Room (Partner)

**Audience**: Partner seller — uses **claude.ai Introw Connect Staging** MCP. Operates per-portal (one vendor at a time, or across both vendors in a multi-vendor deal).
**Use case**: 11 — Deal Coaching (partner-side; companion to vendor `vendor-deal-coach-from-similar-wins`).

## When to use this skill

Use when a partner seller is working a specific deal and wants a comprehensive coaching packet — vendor playbook for the stage, similar past wins, competitive battle cards, reference customers, objection handling, suggested next moves — pulled live from the relevant vendor portal(s). The partner-side counterpart to the vendor's deal-coaching skills.

**Sample prompts that fire this skill:**
- "war room for this deal"
- "coach me on [deal]"
- "what do I do next on [account]"
- "how have we won deals like this"
- "objection handling for [deal]"
- "competitive position on [deal]"
- "draft the next message"

## Why this matters
Direct sales reps get coaching weekly; partner sellers usually get a portal full of PDFs and a quarterly QBR. AI deal coaching closes that gap — but only if the coaching is **immediate, specific, and grounded in the partner's own deal context**, not generic playbook quotes.

This skill is the partner's in-deal war room: the seller pulls up the deal, asks "what's the move?", and gets stage-aware guidance, similar wins to model on, the right battle card, the right reference customer, and a drafted next-message — all in seconds. Industry research: AI coaching produces **34% win-rate lift within six months** (Whatfix); coached reps navigate objections **61% more effectively** (Careertrainer.ai). Extending that to partner sellers is the unlock the channel motion has been missing.

## Process

### Step 1 — Resolve the portal(s)
- `Introw_Connect_Staging:partners` — confirm which vendor portal(s) the deal involves. Most deals are single-vendor; some (multi-product / SI motions) span 2+.
- If multi-vendor, run the war room independently per portal and synthesize.

### Step 2 — Pull the active deal context
- `Introw_Connect_Staging:search_crm_objects` — full deal record: stage, value, products, contacts, last activity, close date, competitor mentions, recent comments, stalled flag.
- `Introw_Connect_Staging:search_partner_engagement` — partner's own activity on this deal.
- `Introw_Connect_Staging:search_tasks` — open tasks tied to the deal.

### Step 3 — Use the dedicated coaching tool first
`Introw_Connect_Staging:deal_coaching` is purpose-built — pass the deal context. It returns persona-aware guidance grounded in the vendor's playbook. Treat its output as the foundation; the rest of this skill enriches it.

### Step 4 — Find similar past wins (partner's own)
- `Introw_Connect_Staging:search_crm_objects` — partner's own closed-won deals in the trailing 12 months, filter to similar vertical / deal size / product / customer segment.
- Aim for 3–7 high-similarity wins. If thin, surface the caveat — fabricated patterns are worse than honest absence.
- For each: how long in stage, what worked, what objections came up, which assets / case studies / reference customers were used.

### Step 5 — Pull the right vendor assets
For the deal's product / vertical / competitive context, identify (from the vendor's connected knowledge base):
- **Battle cards** for any competitor named.
- **Case studies** in the prospect's vertical / segment.
- **Reference customers** the partner can name-drop or arrange a call with.
- **Pricing / packaging guidance** — including deal-protection eligibility (10–15 pts margin reminder).
- **Compliance attestations** (SOC 2, HIPAA, GDPR) if vertical-relevant.

### Step 6 — Surface stage-aware next moves
Based on stage, deal age, and similar-win patterns, prescribe:
- **Top 3 next actions** — concrete moves with rationale, ranked by impact.
- **Champion / power assessment** — is there an executive sponsor? If not, the gap.
- **Drafted message** for the most important next outreach (email / Slack / LinkedIn) — copy-pasteable.
- **Risk flags** — patterns from comparable lost-or-stalled deals to actively avoid.
- **Realistic close timeline** — based on comparables, not stated.

### Step 7 — Capture and queue
- `Introw_Connect_Staging:add_comment` on the deal — log the war-room session so the vendor's PDM can see the coaching trail at next QBR.
- `Introw_Connect_Staging:add_task` — convert top 3 next actions into trackable tasks with due dates.
- For stuck deals where the partner needs vendor help (technical Q, exec sponsorship, pricing exception): draft the CAM/PDM ask.

## Output format
- **Deal snapshot** (2 lines).
- **Vendor's coaching baseline** (from `deal_coaching` tool).
- **Similar past wins** — 3–7 with similarity rationale + what worked.
- **Vendor assets to use** — battle cards, case studies, reference customers (named + linked).
- **Top 3 next actions** with ETA + rationale.
- **Drafted next message** — copy-pasteable, persona-tuned.
- **Risk flags** — what to avoid based on comparable losses.
- **Logged artifacts** — comment ID + task IDs created.

## Guardrails & PRM best practice
- **Partner-side scope.** Only the partner's own deals + vendor-shared content. Never reference other partners' deals.
- **Don't push off-strategy.** Stay aligned to the vendor's playbook (pricing, ICP, positioning). Coaching that contradicts the vendor's strategy damages the co-sell motion.
- **Persona match is non-negotiable.** Coaching an SI motion like a transactional reseller motion breaks both the deal and the relationship. The `deal_coaching` tool handles this — reinforce it, don't override it.
- **Honest signal density.** If similar wins are thin (< 3), say so. Don't extrapolate from 1 comparable as if it were a pattern.
- **Don't draft customer-facing content the seller hasn't seen.** Drafts are starting points; the seller tailors before sending.
- **Reference customers require permission.** Don't recommend name-dropping a reference customer without checking the vendor has cleared them for partner use in this segment.
- **Capture the coaching.** Every war-room session logs to the deal via `add_comment` so the trail survives.
- **Margin discipline.** When suggesting concession paths, surface the deal-protection margin (10–15 pts) the partner already earns by registering — concessions come out of *that* envelope, not on top of it.
- **Multi-vendor deals.** If two vendors are involved, run the war room per portal and surface both views. Don't blend; let the seller see each vendor's playbook.
- **Cross-skill handoff.** Net-new prospect not yet registered → `partner-register-deal` (if installed). Stuck on champion / power gap and need vendor exec engagement → draft the CAM ask. Multi-vendor opportunity → check `partner-prospect-to-vendor-fit-finder` for sequencing.
