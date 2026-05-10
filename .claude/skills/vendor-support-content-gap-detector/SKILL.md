---
name: vendor-support-content-gap-detector
description: Use when a Partner Enablement lead, Channel Ops, or Vendor IT user wants to analyze recurring partner support questions over a window — clustering by intent and cross-checking against the existing knowledge base — to identify the gaps where partners repeatedly ask but no clean answer exists. Outputs ranked content recommendations (battle cards, FAQs, micro-courses) with scope and target partners. Trigger phrases include "support content gaps", "what should we write next", "knowledge base gaps", "partners keep asking the same thing", "where's the content missing", "support deflection roadmap".
---

# Support Content Gap Detector (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP.
**Use case**: 06 — Enablement Support.

## When to use this skill

Use when a Partner Enablement lead, Channel Ops, or Vendor IT user wants to analyze recurring partner support questions over a window — clustering by intent and cross-checking against the existing knowledge base — to identify the gaps where partners repeatedly ask but no clean answer exists. Outputs ranked content recommendations (battle cards, FAQs, micro-courses) with scope and target partners.

**Sample prompts that fire this skill:**
- "support content gaps"
- "what should we write next"
- "knowledge base gaps"
- "partners keep asking the same thing"
- "where's the content missing"
- "support deflection roadmap"

## Why this matters
AI deflects **40–60% of routine partner support tickets** (Gartner / Pylon benchmarks); best-in-class hits 70–80%. The gap between current and best-in-class is almost always the same shape: **partners are asking specific questions the knowledge base doesn't have a clean answer to.** The agent then either improvises (risky) or routes to humans (slow). Either way, the deflection rate stalls.

This skill closes that gap by inverting the analysis: instead of asking "what content do we have?", it asks "**what are partners actually asking that we don't answer well?**" — then prescribes the next 3–5 content investments. The output is a content roadmap that's grounded in actual demand, not assumptions.

## Process

### Step 1 — Define the analysis window
- Default: trailing 90 days. Long enough for pattern detection, recent enough for relevance.
- Optional scoping: by partner type, region, product line, or tier (Bronze partners often have different questions than Gold).

### Step 2 — Pull partner support events
- `Introw:search_crm_objects` (object type = ticket) — formal support tickets in window, with category, status, resolution time.
- `Introw:search_partner_engagement` — comments and conversational support events on partner records.
- `Introw:search_tasks` — task-style support items if program uses them.
- `Introw:search_form_submissions` — questions raised through forms (e.g., "ask my CAM" intake).
- Capture: question text (anonymized), product/category, resolver, time-to-resolve, partner tier, partner type.

### Step 3 — Cluster by intent
Group questions into intent clusters. Common partner-support clusters:

- **Pricing / quoting / config** ("what's the price for 50 seats with annual billing?")
- **Product / feature how-to** ("how do I set up SSO with Okta?")
- **Provisioning / sandbox** ("can I get a 14-day demo tenant?")
- **Account / license lookup** ("is account X already a customer?")
- **Deal status / commission** (often deflectable to `partner-my-commissions`)
- **Marketing assets** ("where's the latest healthcare battle card?")
- **Compliance** ("are we SOC 2 / HIPAA / GDPR compliant for prospect X?")
- **Integration / API** ("does the API support batch operations?")
- **Competitive positioning** ("how do I respond when prospect mentions Competitor Y?")
- **Bug / outage / escalation** (rarely deflectable; route to engineering).

For each cluster: count, top sample questions, partners affected, average time-to-resolve, top resolvers.

### Step 4 — Cross-check against existing knowledge base
For each cluster, score knowledge-base coverage:
- **Strong**: clean, current, easily findable answer exists.
- **Partial**: answer exists but is buried, outdated, or too generic.
- **Weak**: only fragments exist; the support agent is improvising.
- **Missing**: no usable content at all.

Score requires connecting to the vendor's content systems. Use whatever knowledge MCP is installed (Notion, Confluence, Google Drive, Box, Intercom, etc.). If no knowledge MCP is connected, fall back to user input on coverage estimate per cluster.

### Step 5 — Score gap priority
For each cluster:
- **Volume** — how many tickets/comments?
- **MTTR** — how long does resolution take currently?
- **Resolver cost** — who's resolving (CAM time? Engineering? Legal review?)
- **Coverage gap** (Step 4 score)
- **Compliance sensitivity** — does the cluster touch SOC 2 / GDPR / pricing exceptions? (Higher sensitivity = more careful content authoring required.)

Priority score = (volume × MTTR × resolver-cost) ÷ compliance-risk × coverage-gap-severity.

### Step 6 — Recommend content per top cluster
For each top-priority cluster, prescribe a specific content asset:
- **Battle card** for competitive / pricing-objection clusters.
- **Step-by-step how-to doc** for product/feature/integration clusters.
- **FAQ entry** for short, repeated questions.
- **Micro-course** for clusters that involve a workflow with multiple steps (hand-off to `vendor-microcourse-from-closed-lost`).
- **Asset library entry** for marketing / collateral clusters.
- **Self-service portal action** for clusters that should be a button rather than a question (e.g., sandbox provisioning).

Each recommendation includes:
- Asset type and rough scope.
- Target audience (which partner types/tiers benefit most).
- Estimated deflection impact (volume reclaimed × time saved).
- Source material the agent can use to draft a first version (existing fragments, similar past tickets, internal docs).

### Step 7 — Output the roadmap
- Top 3–5 content recommendations, ranked by priority score.
- Aggregate summary: how much support load could be deflected if all top recommendations shipped.
- "Quick wins" (high volume × low authoring effort) called out separately.

## Output format
- **Cluster table**: cluster name, volume, MTTR, current coverage, gap severity, priority score, sample questions.
- **Top content recommendations**: type, scope, target audience, est. deflection impact, source material.
- **Quick wins** flagged.
- **Compliance flags** for clusters needing legal/security review.
- **Capability-matrix recommendation**: which clusters should the support agent execute autonomously vs. route for approval (compliance-sensitive clusters stay human-approved).

## Guardrails & PRM best practice
- **Demand-driven, not catalog-driven.** Don't recommend content because there's a gap *in theory*; recommend because partners are *actually asking*. The volume column is the discipline.
- **Authoring cost matters.** A high-priority cluster that requires legal review on every word is not a quick win. Surface effort estimates honestly.
- **Anonymize before clustering.** Sample questions surfaced in the output should not contain partner-confidential data (account names, deal sizes). Replace specifics with placeholders.
- **Compliance-sensitive content** (SOC 2 attestations, pricing exceptions, contract terms) requires legal/security review before shipping. Flag, don't draft.
- **Don't deflect what should be human.** Some clusters (escalations, dispute handling, strategic-account discussions) shouldn't be deflected — humans handle them by design. Don't recommend content for those.
- **Pair with measurement.** When a content asset ships, measure the cluster's volume + MTTR over the following 60 days. If the asset doesn't move the metric, it's wrong content (not a deflection failure). Iterate.
- **Tier-aware content.** Bronze partners often ask different questions than Gold (Bronze: how to use the product; Gold: how to position against Competitor Z). Tier the content recommendations.
- **Multilingual scope.** If partners span regions, the content needs language coverage. Flag clusters where the volume is concentrated in non-English markets — translation needs to be in scope.
- **Cross-skill handoff.** Workflow-style clusters → `vendor-microcourse-from-closed-lost` to author. Compliance clusters → flag for legal. Sales-positioning clusters → battle card authoring (often handed off to product marketing). Once content ships, `vendor-support-deflection-audit` (if installed) measures the impact.
