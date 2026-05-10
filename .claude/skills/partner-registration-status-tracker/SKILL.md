---
name: partner-registration-status-tracker
description: Use when a partner wants a single view of every deal/lead registration they have outstanding across all vendors — pending approval, approved, in conflict, approaching protection-window expiry — sorted by urgency and recommended action. Trigger phrases include "all my registrations", "what's pending approval", "deal regs across vendors", "protection windows expiring", "registrations in conflict", "registration status".
---

# Cross-Vendor Registration Status Tracker (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the partner has access to.
**Use case**: 08 — Deal Registration (partner-side, multi-vendor).

## When to use this skill

Use when a partner wants a single view of every deal/lead registration they have outstanding across all vendors — pending approval, approved, in conflict, approaching protection-window expiry — sorted by urgency and recommended action.

**Sample prompts that fire this skill:**
- "all my registrations"
- "what's pending approval"
- "deal regs across vendors"
- "protection windows expiring"
- "registrations in conflict"
- "registration status"

## Why this matters
Partners with active pipelines across 5+ vendors often have 20–50 registrations in flight at any given moment — pending approvals, approved-but-aging, in-conflict, sitting on the edge of protection-window expiry. Each vendor's portal shows you *its* slice. Nobody shows you the unified view.

The cost of missing one is significant: a protection window expiring on a deal-in-flight strips 10–15 points of margin off the eventual close. A conflict left unresolved for two weeks degrades vendor trust on every future registration. This skill makes the whole queue visible in one place, sorted by urgency, with recommended action per item.

## Process

### Step 1 — Enumerate vendor portals
- `Introw_Connect_Staging:partners` — get all portals.

### Step 2 — Pull registration state per portal
For each `roomId`:
- `Introw_Connect_Staging:search_form_submissions` — all registrations in trailing 6–12 months, with status.
- `Introw_Connect_Staging:search_crm_objects` — corresponding deal records (stage, value, last-activity, close-date).
- `Introw_Connect_Staging:get_tier_information` — protection-window length per tier (typically 30/60/90 days).

### Step 3 — Classify each registration
Bucket each registration:

- **Pending approval** (and aging) — submitted, vendor SLA running. Flag if past stated SLA.
- **Approved & in protection window** — clean, on track. Show days remaining in window.
- **Approved & nearing window expiry** — < 30 days left in protection. The most urgent class.
- **Approved & expired** — protection window closed; deal still open. Flag for re-registration request or extension ask.
- **In conflict** — vendor flagged as conflicting with another partner or direct sales. Action: respond to vendor with evidence, or accept resolution.
- **Rejected** — partner needs to either appeal, register correctly, or move on.
- **Closed-won** — confirm commission attribution is correct (cross-check `search_commissions`).
- **Closed-lost** — opportunity to log lessons; close cleanly.

### Step 4 — Surface urgency
Sort across all portals by urgency:
- **Red**: protection expiring < 7 days on an active deal; in-conflict registrations sitting > 48 hours; pending approvals past SLA.
- **Yellow**: protection expiring 7–30 days; approvals approaching SLA; aging post-approval with no deal activity.
- **Green**: clean, on track.

### Step 5 — Recommend action per item
For each non-green item:

- **Pending past SLA** → CAM ping, drafted message included.
- **Protection expiring soon, deal still open** → choose: (a) register protection extension, (b) accelerate close, (c) accept loss of protection. Surface the trade-off.
- **In conflict** → review the conflict, gather evidence (existing customer relationship, prior similar wins), draft response.
- **Rejected, recoverable** → draft the corrected resubmission.
- **Closed-won with attribution issues** → flag for finance/CAM follow-up.

### Step 6 — Surface aggregate insight
- **Approval velocity by vendor** — which vendors are slow vs. fast (informs future routing).
- **Conflict frequency by vendor** — which vendors have RoE issues.
- **Win rate by vendor** — which registrations actually close.

These are partner-internal insights, not for the QBR adversarially — just for the partner's own routing decisions.

## Output format
- **Status dashboard across vendors** — table with vendor, account, value, status, urgency, action.
- **Action queue** — sorted red → yellow, with recommended next move per item.
- **Drafted CAM pings** for SLA-breached approvals — copy-pasteable per vendor.
- **Drafted conflict responses** with evidence outline.
- **Aggregate insight** — vendor-by-vendor approval velocity, conflict rate, win rate.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each registration's data is fetched only with that vendor's `roomId`. No cross-portal data leakage in the responses sent back to vendors.
- **Don't submit vendor-confidential data into another vendor's portal.** Cross-vendor analysis happens locally; the partner's CAM pings to Vendor X never reference Vendor Y's data.
- **Conflict responses must be evidence-grounded.** Don't draft a conflict appeal that overclaims partner equity in an account. Surface the evidence honestly; let the partner decide what to argue.
- **Protection-window honesty.** Some vendors don't extend protection windows beyond the original term. Surface the policy if known; don't promise an extension that isn't policy.
- **Re-registration is rare.** If a deal already had protection that expired, re-registering is generally not allowed. Surface the right ask — extension, exception, or accept loss of protection.
- **Closed-won attribution.** When attribution looks off, draft the inquiry to vendor finance/CAM with the specifics (deal ID, expected commission, actual commission). Don't escalate before checking the data.
- **Don't auto-act.** Surface action; partner submits.
- **Capture every CAM ping** via `Introw_Connect_Staging:add_comment` on the relevant registration record so the trail exists for future audits.
- **Run on cadence.** Weekly default; daily during heavy-pipeline quarters. Daily-discovered issues are 10× cheaper to resolve than QBR-discovered ones.
- **Cross-skill handoff.** Stalled approved registrations → `partner-deal-war-room` to coach the deal forward. Conflicts that can't be resolved → escalate to vendor channel ops via `partner-helpdesk` or direct CAM.
