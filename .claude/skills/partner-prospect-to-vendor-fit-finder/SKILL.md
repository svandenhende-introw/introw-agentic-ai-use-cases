---
name: partner-prospect-to-vendor-fit-finder
description: Use when a partner has a new prospect and wants to know which of their vendors fit best, in what order, and how to position each — based on the prospect's stack, segment, vertical, and pain points. Pre-stages the deal-registration payloads. Trigger phrases include "which vendor for this prospect", "best vendor fit for [account]", "what should I lead with", "vendor sequencing for this deal", "match prospect to my vendors", "where do I register this".
---

# Prospect-to-Vendor Fit Finder (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the partner has access to.
**Use case**: 08 — Deal Registration (partner-side, multi-vendor).

## When to use this skill

Use when a partner has a new prospect and wants to know which of their vendors fit best, in what order, and how to position each — based on the prospect's stack, segment, vertical, and pain points. Pre-stages the deal-registration payloads.

**Sample prompts that fire this skill:**
- "which vendor for this prospect"
- "best vendor fit for [account]"
- "what should I lead with"
- "vendor sequencing for this deal"
- "match prospect to my vendors"
- "where do I register this"

## Why this matters
A good reseller / SI often has 5–20 vendors in their portfolio, and every new prospect surfaces the same questions: *which vendor fits best? what's the right opening move? in what order do I bring each vendor in? where do I register first?* Most partners answer these on instinct — and lose deals by leading with the wrong product, registering with the wrong vendor first, or splintering attribution by registering everywhere at once.

This skill turns those decisions into structured analysis grounded in the partner's actual vendor portfolio + each vendor's actual sweet spot. Then it pre-stages the registration payloads so the partner can act in seconds.

## Inputs to gather first
- **Prospect context**: company name, domain, segment / size, vertical, current tech stack (if known), stated pain points or initiative.
- **Sales motion intent**: solo deal, multi-vendor co-sell, services-led implementation, transactional resell.
- **Time horizon**: imminent (closing this quarter), exploratory (educating the buyer).

## Process

### Step 1 — Enumerate vendor portals
- `Introw_Connect_Staging:partners` — get all portals the partner has access to. Capture vendor name, partner record, tier per vendor.

### Step 2 — Pull each vendor's sweet spot signals
For each `roomId`, in parallel:
- `Introw_Connect_Staging:get_tier_information` — what the partner's tier unlocks (margin, MDF, deal protection, certifications held).
- `Introw_Connect_Staging:search_crm_objects` — partner's own closed-won deals with this vendor (vertical, deal size, products) — the partner's *track record* with each vendor.
- `Introw_Connect_Staging:search_partner_engagement` — engagement intensity (signal of relationship health).
- Whatever vendor case-studies / battle cards are accessible in each portal (the vendor's official sweet spot).

### Step 3 — Score vendor-prospect fit per vendor
For each vendor, score along:
- **Vertical fit** — does the vendor have customer wins / case studies in the prospect's vertical?
- **Segment fit** — vendor's typical deal size matches the prospect's profile? (Don't pitch enterprise tooling to a 50-person company.)
- **Stack fit** — does the vendor integrate with the prospect's current tech stack? Are there displacement plays or extension plays?
- **Partner's track record with this vendor** — has the partner closed similar deals before? Win rate, sales cycle.
- **Tier/cert eligibility** — is the partner certified to sell the relevant SKU?
- **Deal-protection eligibility** — can the partner register this with deal protection?
- **Relationship health** — is this vendor relationship active, dormant, strained?

### Step 4 — Recommend sequencing
For multi-vendor opportunities (most common in SI motions), recommend the order:
- **Lead with**: the vendor whose product solves the prospect's *primary* pain, with strongest fit + partner's best track record.
- **Attach**: vendors whose products extend the lead solution naturally (e.g., security ↔ observability, CRM ↔ data tools).
- **Hold for later**: vendors whose products are speculative for this prospect — bring in only after the lead motion is closing.
- **Skip**: vendors with poor fit (don't dilute the conversation).

For each recommended vendor, articulate:
- **Why it fits** (one sentence).
- **Opening positioning** — the framing to use ("Vendor X for healthcare-grade security on top of your existing stack").
- **Asset to send first** — case study or battle card from that vendor.
- **Estimated deal size and cycle** based on partner's track record with that vendor.

### Step 5 — Pre-stage registration payloads
For each vendor in the recommended sequence:
- Pre-fill the deal-registration form with what's known (account, vertical, est. size, products).
- Surface for the partner to confirm and submit via `Introw_Connect_Staging:share_lead_or_register_deal`.
- Mark which registration to file first (sequence matters for deal-protection windows).
- Pre-flight check: any conflict with partner's existing registrations on this account?

### Step 6 — Capture the analysis
- `Introw_Connect_Staging:add_comment` on each relevant vendor portal — log that this prospect was evaluated, the framing decision, and the registration plan.

## Output format
- **Vendor fit matrix** — vendors × fit dimensions × scores.
- **Recommended sequence** — Lead / Attach / Hold / Skip, each with one-line rationale.
- **Per-vendor opening framing + asset** — copy-pasteable.
- **Registration sequence + payloads** — ready for confirmation/submission.
- **Conflict pre-flight** — flags if anything risks channel conflict.

## Guardrails & PRM best practice
- **Don't register with everyone "just in case".** Splintering attribution dilutes the partner's claim with each vendor and fragments the prospect conversation. Pick a sequence and execute it.
- **Lead with fit, not commission.** Recommending the highest-margin vendor regardless of prospect fit erodes the partner's reputation. Fit first, commission optimization second (and only as a tiebreaker between equally-good fits).
- **Honest about gaps.** If no vendor in the partner's portfolio is a strong fit for this prospect, say so — don't force-fit. The partner's reputation depends on bringing the right tool, not the available one.
- **Track-record honesty.** If the partner has zero closed-won deals with a vendor, the "track record" score is empty — flag it. Don't pretend an untested vendor relationship is a strength.
- **Tier eligibility hard-gates.** If the partner's tier or certifications don't authorize selling a vendor's relevant SKU, that vendor drops out — even with otherwise great fit.
- **Pre-flight conflict checks.** Before recommending a registration, scan partner's existing registrations on the same account. Re-registering an already-claimed account creates conflict, not value.
- **Sequencing matters for deal protection.** Most vendors offer deal protection on first-mover registrations within their window. Recommend the registration order that maximizes protection coverage.
- **Don't leak vendor-confidential data.** Each vendor's data stays scoped to its portal. The cross-vendor analysis happens locally; vendor-confidential framings (specific pricing, internal sales motion details) never get echoed into another vendor's portal or the partner's prospect outreach.
- **Capture the rationale.** When the partner picks a sequence, log it via `add_comment` so future analyses (and CAM conversations) have the trail.
- **Cross-skill handoff.** Once registered → `partner-deal-war-room` for stage-aware coaching. Multi-vendor co-sell coordination needed → flag for human handoff (CAMs from both vendors, not the agent).
