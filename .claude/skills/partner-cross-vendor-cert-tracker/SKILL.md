---
name: partner-cross-vendor-cert-tracker
description: Use when a partner user wants to see all required, optional, and expiring certifications across every vendor they work with — flagging what's table-stakes, what gates higher-margin SKUs, and what unlocks the next tier per vendor. Trigger phrases include "all my certifications", "what's expiring", "certs across vendors", "unified cert calendar", "what training is overdue", "cert obligations", "what unlocks higher margins".
---

# Cross-Vendor Certification Tracker (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the partner has access to.
**Use case**: 05 — Training (partner-side, multi-vendor).

## When to use this skill

Use when a partner user wants to see all required, optional, and expiring certifications across every vendor they work with — flagging what's table-stakes, what gates higher-margin SKUs, and what unlocks the next tier per vendor.

**Sample prompts that fire this skill:**
- "all my certifications"
- "what's expiring"
- "certs across vendors"
- "unified cert calendar"
- "what training is overdue"
- "cert obligations"
- "what unlocks higher margins"

## Why this matters
Partners working with 5–10 vendors are juggling 20–50 active certifications: table-stakes ones, expiring ones, optional-but-margin-unlocking ones, and the ones that gate the next tier promotion. Each vendor sends its own renewal nudges; nobody sends a unified view. The result is silent expirations that strip the partner of deal-protection eligibility on the next big deal — discovered exactly when it matters most.

This skill closes the gap: one calendar across every vendor, ranked by economic stakes (margin lost on expiry > tier promotion blocker > nice-to-have), with renewal effort estimates so the partner can plan.

## Process

### Step 1 — Enumerate vendor portals
- `Introw_Connect_Staging:partners` — get all portals the partner has access to.

### Step 2 — Pull cert state per portal
For each `roomId`:
- `Introw_Connect_Staging:get_tier_information` — what certifications each tier requires (held / required / optional).
- `Introw_Connect_Staging:search_partner_engagement` — completed training events, cert achievement records.
- `Introw_Connect_Staging:search_tasks` — any open cert-related tasks.
- `Introw_Connect_Staging:get_goals` — cert-related goals.

### Step 3 — Classify per certification
For each cert across all vendors, capture:
- **Status**: held (current), held (expiring soon), expired, in progress, not yet started.
- **Required vs. optional** at the partner's current tier.
- **What it unlocks**: tier-promotion gate, higher-margin SKU access, deal-protection eligibility on specific products, MDF eligibility.
- **Expiration date** if applicable.
- **Renewal effort** (typical hours / re-test / refresher course).
- **Vendor** + portal + relative tier.

### Step 4 — Score economic stakes per cert
Rank what's at stake for each cert by:
- **Cost of expiry**: revenue loss if it expires (deal protection lost on in-flight deals, SKU access removed, tier demotion risk).
- **Tier-promotion leverage**: does completing this cert close the gap to the next tier with a vendor where promotion is otherwise close?
- **Renewal urgency**: days to expiry × renewal effort — prioritize close-to-expiry-and-cheap-to-renew over far-off-and-effortful.
- **Strategic vendor weight**: certs with vendors who represent a larger share of partner revenue rank higher.

### Step 5 — Generate the calendar
- **This week / month**: certs to act on now (expiring, blocking active deals, near tier promotion).
- **Next 90 days**: scheduled renewals + new certs to start.
- **Strategic (no urgency, high upside)**: certs that would unlock notably higher margins.
- **Optional (skip-eligible)**: certs the vendor surfaces but with low ROI for this partner's motion.

### Step 6 — Recommend a study plan
For top-priority certs:
- Estimated time investment.
- Suggested order (renew expiring before starting new).
- Whether the cert can be earned async (course + assessment) or requires a scheduled event.
- Link to start in the relevant vendor portal.

## Output format
- **Cross-vendor cert calendar** — table with vendor, cert name, status, expiration, what-it-unlocks, urgency.
- **Action queue** — top 3–5 certs to tackle this month.
- **Tier-promotion bridges** — certs that would close a tier gap with a specific vendor.
- **Expiring-and-at-risk** — certs expiring in < 30 days with their economic exposure.
- **Skip list** — certs flagged as low-ROI for this partner's actual motion.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each vendor's cert data only fetched with that vendor's `roomId`. No cross-portal data leakage.
- **Time-bound everything.** "Expiring soon" without a window is meaningless — always state the date.
- **Don't compare vendors competitively.** It's the partner's view; rank for the partner's attention. But don't frame as "Vendor X has worse training than Vendor Y" in any output that could leak vendor-side.
- **Renewal effort honesty.** If a vendor's renewal is a 3-hour deep cert vs. a 15-min refresher, surface the difference. Partners optimize on time-per-margin-unlocked.
- **Strategic priority over completeness.** Don't push the partner to chase every optional cert; surface the ones with real economic stakes for *their* motion. Cert completion isn't the goal — margin and deal eligibility are.
- **Pair with deal context.** A cert that's "optional" abstractly may be critical if the partner has an in-flight deal that needs it. Cross-check `search_crm_objects` to flag this.
- **Don't auto-enroll.** Recommend, don't enroll. The partner schedules learning around their own bandwidth.
- **Capture intent.** When the partner commits to a cert path, use `add_task` on the relevant vendor portal — feeds the vendor's tier-promotion-batch-review next cycle.
- **Cross-skill handoff.** Cert that gates a tier promotion → flag for `partner-onboarding-prioritizer` (if onboarding) or watch for vendor-side tier review. Cert blocking an in-flight deal → urgent intervention via `partner-helpdesk` or CAM ping.
