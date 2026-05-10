---
name: vendor-microcourse-from-closed-lost
description: Use when a Partner Enablement lead, Channel Chief, or RevOps user wants to detect patterns in closed-lost partner deals — clustering by lost-reason and customer context — and generate / suggest targeted micro-courses that address the specific gaps the losses reveal. Trigger phrases include "what are we losing on", "closed-lost patterns", "training from losses", "micro-courses from lost deals", "what should we train on next", "closed-lost driven enablement".
---

# Micro-Courses from Closed-Lost Patterns (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP.
**Use case**: 05 — Training.

## Why this matters
Up to **70% of training content is forgotten within 24 hours, 87% within a week** without reinforcement (Ebbinghaus / industry consensus). Static training catalogs accumulate content nobody uses while real, current losses go un-addressed. The signal that matters most: **partners losing deals tells you exactly what they need to learn**.

Introw can generate and push a 15-minute micro-course to all enabled resellers in **under one hour** — vs. the typical multi-week instructional design cycle. SalesHood / Whatfix research shows AI-coaching delivers **38% skill improvement, 40% faster time to readiness, and 32% win-rate lift** within six months. The leverage move: drive the next micro-course from the gap a closed-lost cluster just exposed.

## Process

### Step 1 — Define the loss cohort
Default: closed-lost partner-sourced deals over the trailing 90 days. Confirm with the user. Optional scoping: by partner type, region, product, or specific competitor.

### Step 2 — Pull the data
- `Introw:search_crm_objects` — closed-lost deals in scope, with full record (vertical, deal size, products, stage at loss, lost-reason, competitor, key contacts, last activity).
- `Introw:search_partner_engagement` — engagement on those deals (was the partner active or absent in the late stages?).
- `Introw:search_partners` — partner profile for each lost deal (tier, certifications held).
- `Introw:search_tasks` — task history (was anything stuck or skipped?).
- Comment history on each deal via `Introw:search_crm_objects` notes for objection / blocker context.

### Step 3 — Cluster by failure pattern
Group losses into patterns rather than treating each as one-off. Common clusters:
- **Pricing / packaging objection** — partner couldn't defend price or pitched wrong SKU.
- **Competitor positioning** — partner lost head-to-head against a specific competitor.
- **Technical-fit / capability** — buyer concluded the product didn't fit; partner couldn't address technical objection.
- **Implementation / timeline** — buyer concerned about deployment risk; partner lacked services answer.
- **Champion loss / power gap** — internal champion left or never emerged.
- **No decision** — buyer stalled; partner couldn't drive urgency.
- **Compliance / security** — buyer concern partner couldn't address (HIPAA, SOC 2, GDPR).
- **Late-stage discovery gap** — discovery wasn't deep enough early on.

For each cluster, capture:
- **Volume** (how many deals).
- **Aggregate value lost.**
- **Affected partners** (which partners lost most often in this pattern; which partner types).
- **Affected verticals / regions / products.**
- **Sample evidence** — 2–3 representative deals with quotes from the lost-reason notes.

### Step 4 — Diagnose the underlying gap per cluster
What knowledge / skill / asset / motion would have changed the outcome? Examples:
- Pricing objection cluster → partner needs ROI-calculator competency + pricing-defense talk-track.
- Competitor cluster → partner needs current battle card + 2–3 fresh competitive case studies.
- Technical-fit cluster → partner needs deeper product-architecture training for that vertical.
- Implementation cluster → partner needs deployment-services-positioning training.
- Champion-loss cluster → partner needs MEDDIC-style champion-development coaching.
- Compliance cluster → partner needs vertical-specific compliance positioning.

### Step 5 — Generate the micro-course outline per gap
For each high-priority cluster, draft a micro-course that meets Introw's training model:
- **Length**: 15–30 min, deployable in under 1 hour.
- **Pulls from**: vendor's existing knowledge base (Notion, Confluence, product docs, asset library) — don't fabricate content.
- **Structure**:
  - 2-min framing: the pattern that's costing us deals.
  - 5-min content: the gap and how to close it.
  - 5-min worked example: walk through a real (or anonymized) lost deal and the alternate path.
  - **Open-question assessment** (not multiple choice) — partner answers a real scenario in their own words; rubric grades response.
  - Inline AI tutoring hook — partner can ask follow-ups during the course.
- **Asset bundle** — battle card / ROI calculator / case study / objection-handling cheat sheet attached.

### Step 6 — Target the right partners
Per cluster, identify which partners benefit most:
- Partners with high concentration of losses in this pattern.
- Partners working pipeline that fits this profile (use `search_crm_objects` to find current active deals in the same vertical/competitive context).
- Partner-type-aware tailoring (the SI version vs. the reseller version).
- Tier-aware delivery (top tier may get a live walkthrough; long tail gets the async micro-course).

### Step 7 — Distribute and track
- Push the course assignment via `Introw:add_task` per partner, with due-date.
- `Introw:add_comment` on each partner record explaining why this course was sent (refers to the loss cluster).
- Establish measurement: re-pull win-rate on similar deals 60 / 90 days post-deployment to validate impact (target: 32%+ win-rate lift on the addressed pattern, per Whatfix benchmarks).

## Output format
- **Loss cohort summary** — total deals, aggregate value, period.
- **Cluster table**: pattern, volume, value, affected partners/verticals, diagnosed gap.
- **Micro-course outlines** per priority cluster — title, learning objective, content sections, assessment scenario, asset bundle.
- **Distribution plan** — partner targets, channel, due-dates.
- **Measurement plan** — what to track, when, with what comparison.

## Guardrails & PRM best practice
- **Evidence-grounded.** Every micro-course traces to a specific cluster with sample lost-deal evidence. Generic "let's train on objection handling" without evidence misallocates effort.
- **Don't over-fragment.** If there's a dominant cluster (>40% of losses), focus there before fragmenting into 6 minor courses. Triage matters.
- **Open-question assessments only.** Multiple-choice quizzes get gamed (industry consensus); rubric-graded open-question assessments measure actual understanding.
- **Knowledge-base sourced.** Course content draws from existing vendor docs over MCP — not fabricated. Cite the source for every section.
- **Don't blame partners for ambiguous losses.** Some losses (no-decision, competitor pre-empted, customer reorg) aren't training gaps. Filter cleanly before clustering.
- **Tier and persona awareness.** A reseller and an SI losing the same way may need different versions of the course — generate variants.
- **Compliance-cluster sensitivity.** Compliance losses (HIPAA, SOC 2, GDPR) may need legal-team review of the course content before distribution — flag it.
- **Don't auto-distribute without human sign-off on first cycle.** Surface the courses + targets; get user approval before pushing tasks.
- **Measure impact.** Pair every course deployment with a post-period win-rate measurement on the addressed pattern. If the pattern's win-rate doesn't improve, the diagnosis or course was wrong — surface that loop.
- **Cross-skill handoff.** Pattern reveals a coaching gap on live deals → `vendor-deal-coach-from-similar-wins`. Pattern reveals a partner-fit issue → `vendor-training-gap-analysis` for tier-coverage view.
