---
name: vendor-content-radar
description: Use when a Partner Marketing Manager wants a continuous-running content radar — scanning the vendor's release notes, LinkedIn, blogs, industry publications, and competitor news for partner-relevant content, transforming relevant items into partner-ready messaging per segment, and distributing + tracking through Introw. Auto-updates partners on new product releases. Trigger phrases include "scan release notes", "update partners on new releases", "convert release notes to partner outreach", "scan LinkedIn for partner content", "content radar", "what's new for partners this week", "convert blog posts to partner outreach", "weekly partner content sweep", "competitive content distribution".
---

# Content Radar & Distribution (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP (+ WebFetch / WebSearch, and any installed LinkedIn / RSS / blog MCPs).
**Use case**: 07 — Campaigns & Announcements.

## When to use this skill

Use when a Partner Marketing Manager wants a continuous-running content radar — scanning the vendor's release notes, LinkedIn, blogs, industry publications, and competitor news for partner-relevant content, transforming relevant items into partner-ready messaging per segment, and distributing + tracking through Introw. Auto-updates partners on new product releases.

**Sample prompts that fire this skill:**
- "scan release notes"
- "update partners on new releases"
- "convert release notes to partner outreach"
- "scan LinkedIn for partner content"
- "content radar"
- "what's new for partners this week"
- "convert blog posts to partner outreach"
- "weekly partner content sweep"
- "competitive content distribution"

## Why this matters
**96% of B2B marketers expect to grow channel revenue** (Demand Gen Report) — but most can't, because their partners aren't sufficiently informed. Communication is the carrier wave for everything else: campaigns, launches, competitive responses, customer wins. Manual production caps the partner marketing manager at ~4 partner-facing communications/month; agentic radar+segment+distribute lifts that to **40–80 (10–20×)** without hiring, with **2–4× engagement** vs. generic blasts. Competitive responses ship in **under one hour** instead of weeks.

This skill is a **continuously-running radar**, not a one-shot generator. It scans, filters, transforms, distributes, and tracks — and is meant to run on a cadence (weekly default) so partner-facing content velocity is sustained.

## Sources to monitor
1. **Release notes / changelog feeds / product update pages** — the **highest-leverage source** for partners. Every shipped feature is something partners need to position with prospects, but most release notes never reach partner-facing comms in time. Sources include Notion / Confluence release pages, public changelog URLs, and vendor docs sites.
2. **Vendor's own LinkedIn** — exec posts, brand posts, employee thought leadership. (Vendor's best content historically dies in the partner channel.)
3. **Vendor blog / press / launch feeds.**
4. **Industry publications** — partner-relevant analyst notes, trend pieces, customer-vertical news.
5. **Competitor moves** — public announcements, pricing changes, leadership changes that change the partner's competitive context.
6. **Customer wins / case studies** as they're published.
7. **Loom / video drops** the executive team shares — extract transcript, treat as a content source.

The user should configure source URLs / handles up front; the skill scans them.

## Process

### Step 1 — Scan
- **Release notes**: use installed knowledge-base MCPs (Notion, Confluence, Box, Google Drive) when the changelog lives there; otherwise WebFetch on the public changelog URL or RSS feed. Capture each release entry with version, date, title, body, and any tagging the vendor applies (feature / fix / breaking change / pricing / packaging).
- **LinkedIn**: use installed LinkedIn MCP if available; otherwise WebFetch on profile/company pages or rely on a saved RSS-style feed.
- **Blogs / publications**: WebFetch on the source, or RSS MCP if installed.
- **Competitor news**: WebSearch with site filters.
- Tag each item with source + publish-date + raw text.

### Step 2 — Filter to partner-relevant content
For each candidate item, score relevance:
- **Product / feature update** that partners need to know to sell.
- **Competitive response** material — how to position vs. a competitor's move.
- **Customer win** — case study a partner can use in their own outreach.
- **Industry / vertical signal** — context for partners selling into that vertical.
- **Executive thought leadership** that the partner can reshare or quote.
- **Compliance / regulatory** signal that affects partner motion.

Drop low-relevance items (internal HR posts, generic "we're hiring" content, anniversary celebrations) — relevance discipline is the whole point.

**Release-notes-specific filtering** (release notes need their own classifier — most release entries are ignorable to partners):
- **Customer-facing feature** (visible to end users / changes the demo / unlocks new use cases) → **push** (high priority).
- **Competitive implications** (closes a gap vs. a named competitor / answers a recurring objection) → **push + flag for battle-card update**.
- **Pricing / packaging change** (new SKU, price move, billing change, tier-eligibility change) → **push urgent** + escalate to channel leadership before broadcast.
- **Integration / API change** that affects partners building on the platform → **push to SI / ISV partners specifically**.
- **Compliance / security attestation update** (new SOC 2, ISO, FedRAMP, regional certs) → **push to vertical-specialist partners** (healthcare, financial services, public sector).
- **Bug fix / internal-only change** → **skip** (no partner value; clutters the channel).
- **Breaking change / deprecation** → **push urgent** with migration guidance — partners with affected customers need lead time.

### Step 3 — Segment + transform per audience
For each high-relevance item, generate partner-ready variants segmented by:
- **Tier** (Gold gets co-sell language; Bronze gets enablement-led).
- **Region / language** (DACH = compliance-forward; LATAM = use-case-forward).
- **Partner type** (SI = technical depth; reseller = transactional CTA; referral = warm-intro framing).
- **Vertical specialty** (healthcare partners get HIPAA-flavored framing).

Each variant should:
- Open with relevance to the partner ("As a healthcare-focused SI, here's what changed this week…").
- State the takeaway in 1–2 sentences (partners don't read filler).
- Provide the asset / next step (link, asset ID, deal-reg deep link).
- Carry a clear CTA (use the new battle card, register a deal, attend the webinar, share with prospects).

**Release-notes-specific transforms** — for each pushed release item, generate three derivatives, not just one:
- (a) **One-line "what's new" alert** per partner segment — a Slack-or-email-friendly headline that says what shipped, who it benefits, and the link to learn more.
- (b) **Talking points for partner sellers in active deals where the feature matters** — cross-check open deals via `Introw:search_crm_objects` and surface the partners with relevant pipeline; their version of the alert includes named deals and the specific positioning angle.
- (c) **Customer-ready outreach template** — a forward-able message the partner can lightly edit and send to prospects/customers in their pipeline. Frames the new capability as a reason to (re-)engage.

### Step 4 — Build segmentation context from Introw
- `Introw:search_partners` — current partner roster with tier/region/categories.
- `Introw:get_tier_information` — tier-specific entitlements that affect message framing.
- `Introw:search_partner_engagement` — last-touch saturation: skip recipients who got 2+ touches in the last 14 days.

### Step 5 — Distribute
For each variant × segment:
- Push via the partner's preferred channel (email, Slack, Teams, portal announcement).
- For high-priority items (product launch, competitive response), include a `share_lead_or_register_deal` deep link to convert reading into action.
- Use `Introw:add_comment` on the relevant partner records or campaign record for audit trail.

### Step 6 — Track engagement
- Use `Introw:search_partner_engagement` 7 / 14 / 30 days post-send to measure response (asset views, comments, registrations attributable to the campaign).
- Surface engagement asymmetry — if Variant A landed in DACH but Variant B died in NA, feed that back into the next radar cycle.
- Use `Introw:add_comment` to log the campaign performance summary on each campaign event.

## Output format
- **Radar digest**: scanned items with relevance score and disposition (publish / skip / route).
- **Release notes this cycle**: dedicated section listing every release item scanned + its disposition (push / skip / route) + variant set if pushed (alert, seller talking points, customer-ready template). Embargo flags called out.
- **Per-published-item**: segment list × variants drafted, with channel and send window.
- **Recipient counts** per variant.
- **Suppression list** for engagement-saturated partners.
- **Tracking plan**: when and how engagement gets measured.
- **Next-cycle improvements**: what worked, what to drop.

## Guardrails & PRM best practice
- **Relevance discipline.** A radar that publishes generic content trains partners to ignore the channel. Be aggressive about filtering — better 3 high-relevance items per week than 30 mediocre ones.
- **Segment, don't blast.** If a variant's recipient count is > 50% of total partners, the segment is too broad — push back and segment harder.
- **Source attribution.** When sharing competitor or industry content, link the source — partners trust attribution.
- **Localization is not translation.** Adapt tone and emphasis per region, don't just google-translate.
- **Don't auto-send launches or pricing comms.** Skill ends at draft + recipient list for those — human approval before broadcast.
- **Tier-fairness.** Don't strip the long tail; give them a tier-appropriate variant. Exclusion erodes trust.
- **Compliance scope.** Region-specific disclaimers, opt-out language, GDPR consent checks before sends to EU partners.
- **Track to revenue, not opens.** Tie campaigns to deal-registration uplift in targeted segments via `Introw:search_form_submissions` over the trailing 30 days.
- **Run on cadence.** Radar value compounds with frequency. Weekly default; daily for active competitive periods or product launches.
- **Don't pre-announce embargoed releases.** Some release entries are partner-NDA-only until GA — respect embargo and disclosure dates strictly. If the source includes embargo metadata, treat it as authoritative; if not, default to "internal partner-team only" until you confirm GA status.
- **Don't auto-push breaking changes / deprecations** without a coordinated migration plan — partners with affected customers need vendor-side support engagement, not just a notification.
- **Cross-skill handoff.**
  - Recurring objection-related features (a release that addresses a known closed-lost reason) → `vendor-microcourse-from-closed-lost` to author a targeted micro-course.
  - Release alerts feed the partner-side `partner-cross-vendor-content-calendar` view so partners see vendor activity on their own calendar.
  - Strategic content (major launches, exec posts) → `vendor-generate-segmented-campaign` for higher-effort treatment.
