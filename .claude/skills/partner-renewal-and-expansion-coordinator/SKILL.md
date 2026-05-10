---
name: partner-renewal-and-expansion-coordinator
description: Use when a partner who resells / co-sells ongoing services wants a unified view of customer renewal dates, expansion windows, and at-risk accounts across every vendor they work with — so they can coordinate proactive outreach before renewals lapse and surface expansion plays at the right moment. Trigger phrases include "upcoming renewals", "expansion windows across vendors", "customer renewal calendar", "what's renewing in 90 days", "at-risk customer accounts", "expansion opportunities", "customer base review across vendors".
---

# Renewal & Expansion Coordinator (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the partner has access to.
**Use case**: 04 — Activation (partner-side, multi-vendor — applies to ongoing customer-relationship motions: SaaS resell, MSP, services-led).

## When to use this skill

Use when a partner who resells / co-sells ongoing services wants a unified view of customer renewal dates, expansion windows, and at-risk accounts across every vendor they work with — so they can coordinate proactive outreach before renewals lapse and surface expansion plays at the right moment.

**Sample prompts that fire this skill:**
- "upcoming renewals"
- "expansion windows across vendors"
- "customer renewal calendar"
- "what's renewing in 90 days"
- "at-risk customer accounts"
- "expansion opportunities"
- "customer base review across vendors"

## Why this matters
Renewal and expansion revenue is where partner P&L compounds — a partner who actively manages renewals + expansions across their installed base earns 2–3× more lifetime customer value than one who sells, ships, and forgets. But for partners with customers across 5+ vendors, the calendar is impossible: each vendor's contract renewals are tracked in that vendor's portal (or worse, in the partner's spreadsheet), and the expansion windows aren't always known until the vendor announces a feature push.

This skill aggregates: every customer × every vendor × every renewal/expansion window in one view, sorted by what to act on now. Renewal slippage is the silent killer of partner P&L; this skill makes it visible early.

## Process

### Step 1 — Enumerate vendor portals
- `Introw_Connect_Staging:partners` — get all portals.

### Step 2 — Pull customer + contract state per portal
For each `roomId`:
- `Introw_Connect_Staging:search_crm_objects` — closed-won deals (the partner's installed base with this vendor); contract end dates if encoded; renewal-stage records.
- `Introw_Connect_Staging:search_partner_engagement` — recent activity on those accounts.
- `Introw_Connect_Staging:search_form_submissions` — any expansion/upsell registrations already in flight.
- `Introw_Connect_Staging:search_tasks` — vendor-assigned tasks tied to renewal/expansion motions.
- `Introw_Connect_Staging:search_commissions` — commission history per account (renewal-cycle commissions vs. one-time).

### Step 3 — Classify each customer × vendor relationship
For each customer-vendor pair:
- **Status**: active subscription / approaching renewal / in renewal / lapsed / expansion-eligible.
- **Renewal date** (if known) and **days remaining**.
- **Annual contract value** (if visible) and **expected renewal value** at current usage.
- **Expansion signals**: has the vendor launched a relevant new SKU? Has the customer's usage grown? Is there an adjacent product the partner could attach?
- **Health signals**: usage trending up vs. down (where vendor data exposes this); recent customer service tickets; CSM red-flags.
- **Partner action history**: when did the partner last touch the customer about this vendor's product?

### Step 4 — Build the unified calendar
- **In renewal now / past due**: drop everything. Highest urgency.
- **Renewing in 30 days**: action queue this week.
- **Renewing 30–90 days**: pre-renewal motion — confirmation outreach, expansion conversations.
- **Renewing 90–180 days**: strategic — early expansion plays, multi-product attach.
- **Expansion-eligible (off-cycle)**: customers where a vendor has launched something attachable.

### Step 5 — Score expansion-play priority
For expansion-eligible customers, rank by:
- **Customer health** (don't push expansion to an at-risk account).
- **Adjacent-product fit** (vendor's new SKU matches customer's stated needs).
- **Multi-product attach motion** (expansion across vendors — e.g., customer renews Vendor X security, partner pitches Vendor Y observability layered on top).
- **Effort vs. revenue impact**.

### Step 6 — Recommend per-customer next move
For top-priority renewals + expansion plays:
- **Outreach plan**: who at the customer to contact, when, what to lead with.
- **Coordinated multi-vendor pitch** if the customer is renewing one vendor and expansion-eligible on another — frame as a strategic conversation rather than disjoint pitches.
- **Drafted message** to the customer — copy-pasteable.
- **Drafted CAM ping** to the relevant vendor if the partner needs vendor SE / pricing engagement to close.
- **Pre-stage registration**: if expansion is likely to land, pre-fill the deal-reg payload via `share_lead_or_register_deal`.

## Output format
- **Renewal calendar across vendors** — table with customer, vendor, contract end, current ACV, days remaining, status, urgency.
- **Action queue this week** — top 5–10 by urgency.
- **Expansion plays** — customers with expansion-eligible signals, ranked.
- **Coordinated multi-vendor pitches** — accounts where 2+ vendors line up for a single conversation.
- **Drafted outreach + CAM pings** per priority item.
- **At-risk callouts** — customers showing churn signals, surfaced for vendor partnership.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each customer-vendor relationship is fetched with that vendor's `roomId`. The aggregated view is the partner's local synthesis.
- **Customer-confidential data stays scoped.** If the partner can see the customer's usage / renewal numbers in a vendor's portal, that data doesn't get echoed into another vendor's portal or any third-party communication.
- **Don't push expansion to at-risk customers.** A churn-flagged customer needs retention motion, not an upsell pitch. Surface health signals clearly; the partner picks the play.
- **Renewals are not assumptions.** Just because a contract is approaching renewal doesn't mean the customer renews. Don't pre-stage commissions; surface as opportunity.
- **Multi-vendor coordination respects the customer's reality.** A customer doesn't want 6 separate sales pitches in a quarter — the partner's value is in coordinating into one strategic conversation. Recommend that, not splintered outreach.
- **Don't surface vendor-confidential roadmap to customers.** Some vendors share advance feature info with partners under embargo. Expansion plays grounded in those features must respect the embargo date.
- **Capture customer-side commitments separately.** When the customer commits to a renewal or expansion, log the partner's-eye-view via `add_comment` on the relevant vendor portal. Don't auto-create the registration — let the partner confirm the deal first.
- **Don't auto-pitch at customer.** Drafts are starting points; the partner edits + sends with relationship voice.
- **Run on cadence.** Monthly default; weekly during heavy renewal quarters.
- **Cross-skill handoff.** Pre-staged registrations → `partner-register-deal` flow. In-flight expansion deals → `partner-deal-war-room` for coaching. Customer at risk → escalate to vendor CSM via `partner-helpdesk` or direct CAM.
