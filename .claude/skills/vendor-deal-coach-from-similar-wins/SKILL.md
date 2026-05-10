---
name: vendor-deal-coach-from-similar-wins
description: Use when a CAM, PDM, or Channel Account Manager wants to coach a specific partner deal by first finding similar past won deals (same vertical, deal size, product mix, partner type), extracting the success patterns from those wins, and producing replication coaching for the live deal. Trigger phrases include "coach this deal from similar wins", "what worked on similar deals", "replicate past success", "find comparable wins for this deal", "how did we close deals like this before".
---

# Deal Coach from Similar Wins (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP.
**Use case**: 11 — Deal Coaching.

## When to use this skill

Use when a CAM, PDM, or Channel Account Manager wants to coach a specific partner deal by first finding similar past won deals (same vertical, deal size, product mix, partner type), extracting the success patterns from those wins, and producing replication coaching for the live deal.

**Sample prompts that fire this skill:**
- "coach this deal from similar wins"
- "what worked on similar deals"
- "replicate past success"
- "find comparable wins for this deal"
- "how did we close deals like this before"

## Why this matters
AI coaching tools improve win rates by **34% within six months** (Whatfix); structured coaching delivers **32% higher win rates and 28% higher quota attainment** (Korn Ferry); coached reps navigate objections **61% more effectively** (Careertrainer.ai). Partner-sourced deals historically close at lower rates than direct because partner sellers haven't received the structured coaching their direct counterparts get weekly.

This skill's defining property: **coaching is grounded in this vendor's actual past wins, not generic playbook**. For every active partner deal, it finds the most analogous closed-won deals, extracts what worked at each stage, and prescribes how the partner can replicate that pattern. The customer-specific context, the objection-handling patterns, the asset usage, the time-to-close — all surfaced as evidence the partner can act on.

## Inputs to gather first
- **The active deal** (ID or named).
- **Specific concern** if any (objection, stalled stage, competitive pressure, close motion). If unspecified, run a full review.
- **Comparable scope**: trailing 12 months default; expand if signal is thin.

## Process

### Step 1 — Pull the active deal context
- `Introw:search_crm_objects` — full deal record: stage, value, products, key contacts, last activity, close date, competitor mentions, recent comments.
- `Introw:search_partners` — submitting partner: tier, type (SI / reseller / referral / MSP), certifications, historical win rate.
- `Introw:search_partner_engagement` — recent activity on this deal (comments, asset views, registrations).
- `Introw:search_tasks` — open tasks tied to the deal.

Profile the active deal across the matching dimensions:
- Vertical / industry
- Deal size band
- Product mix
- Customer segment / size
- Geographic region
- Partner type
- Stage and stage-age
- Competitor named (if any)
- Stakeholder roles known

### Step 2 — Find the comparable past wins
- `Introw:search_crm_objects` — closed-won deals in the trailing 12 months, filter to similar vertical / deal size / product / customer segment / region.
- Rank by similarity — the closer the customer profile and product mix, the higher the signal.
- Aim for 3–7 high-similarity wins; if fewer exist, expand the window or surface the thin-signal caveat.

If no similar wins exist (e.g., new vertical, new product), say so plainly — fabricated patterns are worse than honest absence.

### Step 3 — Extract the success pattern across the wins
For each comparable win, mine the record:
- **Stage progression cadence** — how long in each stage; what signaled readiness to advance.
- **Champion / power dynamics** — who became the champion; how was economic buyer engaged.
- **Objections raised + how handled** — pull from `add_comment` history on those deals.
- **Asset usage** — which battle cards, case studies, ROI calculators were referenced.
- **Pricing motion** — how was deal protection / discounting handled.
- **Close motion** — what was the actual close-step sequence.
- **Time-to-close** distribution.

Synthesize across the wins: what's the *shared* pattern? Which patterns are vertical-specific vs. universal? Which partner-type-specific vs. transferable?

### Step 4 — Map pattern to active deal
For the active deal, prescribe:
- **Stage-specific next moves** — what the comparable wins did at this stage age.
- **Champion-development play** — if the analogous wins had executive sponsor at this stage, surface that as a gap-or-confirmed.
- **Objection prep** — recurring objections from the comparables, with the actual handling lines that worked.
- **Asset suggestions** — the specific assets used in comparables, retrievable from the partner's enablement library.
- **Reference customers** — name the comparable closed-won customers (where appropriate to share) as reference candidates.
- **Risk flags** — patterns from comparable lost-or-stalled deals to actively avoid.
- **Close timeline** — realistic close estimate based on comparable cycle length.

### Step 5 — Persona-aware delivery
Tailor the coaching by partner type:
- **SI** — emphasize multi-product attach, services revenue, deployment roadmap, executive stakeholder mapping.
- **Reseller** — emphasize margin protection, deal-protection registration, fast quote, transactional close.
- **Referral** — emphasize warm-intro quality, handoff cleanliness, attribution.
- **MSP** — emphasize recurring-revenue framing, multi-tenant fit.
- **Marketplace** — emphasize procurement velocity, billing motion.

### Step 6 — Capture and hand off
- `Introw:add_comment` on the active deal — log the comparable wins referenced and the coaching delivered. The next CAM picking up this deal sees the coaching trail.
- `Introw:add_task` for the partner — convert the top 3 next actions into trackable tasks with due dates.
- If the partner is on the `partner-coach-my-deal` flow, this coaching is visible to them via the comment.

## Output format
- **Active deal snapshot** — 2 lines.
- **Comparable wins** — 3–7 most similar closed-won deals with similarity rationale.
- **Extracted pattern** — what worked at each stage, with evidence references.
- **Prescription for this deal** — top 3 next actions, objection-handling lines, assets to use, reference customers, risk flags, close estimate.
- **Logged artifacts** — comment IDs and task IDs created.

## Guardrails & PRM best practice
- **Evidence over generic.** Every coaching point traces to a specific past won deal or pattern across them. "Generic playbook" coaching loses to evidence-grounded coaching every time.
- **Honest signal density.** If comparable wins are thin (< 3), say so. Don't extrapolate from one comparable as if it were a pattern.
- **Persona match is non-negotiable.** Coaching an SI like a transactional reseller breaks both the deal and the relationship.
- **Don't share confidential customer data inappropriately.** Reference customers by name only where the partner is authorized to discuss them; otherwise share the pattern without disclosing the comparable customer's identity.
- **Surface, don't seize.** PDM coaches the partner; the partner runs the deal. Never propose direct outreach from the vendor that bypasses the partner's relationship.
- **Capture the coaching.** `Introw:add_comment` on the deal so the QBR has the trail and the partner can see what was discussed.
- **Time-to-close honesty.** If the comparables suggest a longer cycle than the partner's stated close date, surface the gap — false hope on close dates corrupts the forecast.
- **Risk flags, not just success patterns.** Comparable *lost* deals carry as much signal as comparable wins — surface the avoidance patterns explicitly.
- **Cross-skill handoff.** Coaching reveals a training gap → `vendor-microcourse-from-closed-lost` or `vendor-training-gap-analysis`. Coaching reveals a partner-fit issue → `vendor-pipeline-partner-influence-scout` to consider re-placement.
- **Don't over-coach.** A partner who gets 8 coaching nudges per deal will tune them all out. Top 3 next actions; if the partner needs more, schedule a CAM call.
