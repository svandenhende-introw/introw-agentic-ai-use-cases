---
name: partner-cross-vendor-content-calendar
description: Use when a partner wants a unified calendar of upcoming product launches, webinars, MDF programs, campaigns, and tier-promotion windows across all the vendors they work with — so they can plan their own outreach, sales motions, and customer communications around vendor activity. Trigger phrases include "what's coming up", "vendor calendar across all my vendors", "upcoming launches", "MDF windows", "what should I plan around", "vendor activity calendar".
---

# Cross-Vendor Content & Activity Calendar (Partner)

**Audience**: Partner user — uses **claude.ai Introw Connect Staging** MCP across **all portals** the partner has access to.
**Use case**: 07 — Campaigns & Announcements (partner-side, multi-vendor).

## When to use this skill

Use when a partner wants a unified calendar of upcoming product launches, webinars, MDF programs, campaigns, and tier-promotion windows across all the vendors they work with — so they can plan their own outreach, sales motions, and customer communications around vendor activity.

**Sample prompts that fire this skill:**
- "what's coming up"
- "vendor calendar across all my vendors"
- "upcoming launches"
- "MDF windows"
- "what should I plan around"
- "vendor activity calendar"

## Why this matters
Every vendor runs its own roadmap of launches, campaigns, MDF cycles, webinars, and incentive programs — and announces them in its own portal, on its own cadence. The partner who could capitalize on a Vendor X launch with their installed base often misses it because they didn't see the announcement until two weeks later. Multiplied across 5–10 vendors, the partner is constantly playing catch-up on vendor activity.

This skill aggregates: every vendor's announced upcoming activity, in one calendar, ranked by what's most leverageable for the partner's actual customer base. Plan outreach around launches; pre-stage campaigns; book SE time before the wave hits.

## Process

### Step 1 — Enumerate vendor portals
- `Introw_Connect_Staging:partners` — get all portals.

### Step 2 — Pull upcoming activity per portal
For each `roomId`:
- `Introw_Connect_Staging:search_partner_engagement` — recent and upcoming campaign / announcement events the partner has been invited to.
- `Introw_Connect_Staging:search_form_submissions` — open MDF program windows, co-marketing proposals, partner application deadlines.
- `Introw_Connect_Staging:search_tasks` — vendor-assigned tasks with due dates that hint at upcoming activity.
- Knowledge-base content where launch / event metadata is published.

### Step 3 — Classify each event
For each upcoming activity across vendors, capture:
- **Type**: product launch, feature release, webinar, certification cohort, MDF window, campaign template release, tier-review window, executive event, training drop.
- **Date / window**.
- **Audience** (which segments / verticals / regions does this apply to).
- **Partner action required** (read-only, register to attend, opt-in, MDF apply, campaign deploy).
- **Economic stake** (related to a SKU the partner sells, a vertical the partner serves, a tier the partner is approaching).
- **Vendor + portal**.

### Step 4 — Score relevance to this partner
Rank each event by:
- **Customer-base fit**: does the partner have prospects/customers in segments where this matters?
- **Partner motion fit**: does it apply to what the partner actually sells (avoid noise from products outside the partner's portfolio)?
- **Effort vs. impact**: a MDF window with 1-week deadline + low fit ranks lower than a launch in the partner's strongest vertical.
- **Vendor-relationship leverage**: high-value when it's a vendor where the partner is pacing for a tier promotion or activation.

### Step 5 — Build the unified calendar
- **This week**: items that need action now (deadlines, registrations, opt-ins).
- **Next 30 days**: items to plan around — pre-stage outreach, book SE time, queue campaigns.
- **Strategic 30–90 days**: bigger windows worth shaping the partner's quarter around.
- **FYI**: vendor activity not directly leverageable but worth knowing.

### Step 6 — Recommend partner moves per high-relevance item
For top-scored events:
- **Outreach plan**: which customers / prospects to contact when, framed around the launch.
- **Campaign queueing**: which assets to use, what segment to send to.
- **MDF application**: drafted proposal aligned to the program.
- **Pre-event prep**: certifications to complete before a launch hits, demos to schedule with vendor SE.

## Output format
- **Calendar across vendors** — table by date with vendor, event, type, action required, fit score.
- **This-week action queue** — anything time-sensitive.
- **30-day plan** — moves the partner should pre-stage now.
- **Strategic windows** — bigger opportunities worth shaping the quarter around.
- **Drafted outreach / MDF apps** — copy-pasteable per top-relevance item.

## Guardrails & PRM best practice
- **Strictly scoped per portal.** Each vendor's calendar data is only fetched with its own `roomId`. No cross-portal leakage in any partner-facing or vendor-facing output.
- **Vendor-confidential roadmap data stays internal.** Some vendor announcements are partner-confidential (e.g., advance notice on a launch). Don't surface those to customer-facing outreach or campaigns until embargo lifts.
- **Don't pre-announce.** If a vendor has shared advance launch info under embargo, the calendar can show it to the partner — but the partner's drafted customer outreach must respect the embargo date.
- **Relevance discipline.** Surface 5–10 high-fit events per cycle, not 50 generic vendor events. Generic feeds train the partner to ignore the calendar.
- **Honor capacity.** A partner can't action 12 launches in 2 weeks. Recommend a focused 3–5 priority moves; the rest is FYI.
- **Match to actual customer base.** If the partner's customer base skews mid-market services, an enterprise launch is FYI not action. Use deal/customer signals (`search_crm_objects`) to ground relevance.
- **Don't auto-deploy campaigns.** Campaign queueing means drafted + ready-for-review, not pushed to customers automatically.
- **Capture commitments.** When the partner commits to apply for MDF or attend an event, log via `add_task` on the relevant vendor portal.
- **Run on cadence.** Weekly default. Daily during heavy launch periods.
- **Cross-skill handoff.** Outreach plan → individual customer-level coaching via `partner-deal-war-room`. Cert pre-reqs for upcoming launches → `partner-cross-vendor-cert-tracker`. MDF program windows → drafted apps stay with this skill until applied.
