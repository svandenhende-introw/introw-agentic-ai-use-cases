---
name: vendor-personalized-onboarding-from-transcripts
description: Use when a CAM, PDM, or Channel Ops user wants to spin up a personalized onboarding plan for a new partner — using meeting transcripts (kickoff calls, intro meetings, partnership-fit conversations) plus existing partner context, then assigning every task with owner + due date in Introw and managing the project headlessly. Trigger phrases include "set up onboarding for [partner]", "personalized onboarding plan", "build onboarding from this transcript", "onboard [partner] based on our kickoff call", "headless onboarding project".
---

# Personalized Onboarding Orchestrator from Transcripts (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP (+ optional transcript MCP: Otter, Fathom, Gong, Read.ai, Granola, or transcript pasted into the conversation).
**Use case**: 03 — Onboarding.

## When to use this skill

Use when a CAM, PDM, or Channel Ops user wants to spin up a personalized onboarding plan for a new partner — using meeting transcripts (kickoff calls, intro meetings, partnership-fit conversations) plus existing partner context, then assigning every task with owner + due date in Introw and managing the project headlessly.

**Sample prompts that fire this skill:**
- "set up onboarding for [partner]"
- "personalized onboarding plan"
- "build onboarding from this transcript"
- "onboard [partner] based on our kickoff call"
- "headless onboarding project"

## Why this matters
Without structured onboarding, average channel partner time-to-productivity is **6–12 months** (Magentrix); structured programs compress this to **60–90 days**. Partners who close their first deal within 90 days are **3–4× more likely** to remain active at one year (Unifyr Channel Atlas). The first 90 days set the partner's belief about what working with this vendor *feels like*. A CAM responsible for 30 partners typically spends **6–8 hours/week** on routine onboarding chasing — **300–400 hours/year** that should be redirected to relationship work, not reminder-bot duty.

The differentiator of this skill: most onboarding plans are template-driven and ignore what the partner actually said in the kickoff call. This one starts from the transcript and personalizes the journey to the partner's stated commitments, capabilities, target verticals, tech stack, and constraints.

## Inputs to gather first
- **Partner identity** + portal/CRM record.
- **Source transcripts**: kickoff call, partnership-fit conversation, technical scoping call. Pasted text or transcript-MCP reference.
- **Partner type**: reseller, SI, referral, MSP, ISV, marketplace — drives default journey shape.
- **Target time-to-first-deal**: default 60–90 days.
- **Owner assignment defaults**: who's the CAM, who's the technical lead, who's the marketing buddy.

## Process

### Step 1 — Pull partner context
- `Introw:search_partners` — partner record (tier, categories, region, lifecycle stage).
- `Introw:search_crm_objects` — any pre-existing deals or pipeline.
- `Introw:get_tier_information` — what tier eligibility looks like; what onboarding completion unlocks.
- `Introw:get_goals` — any pre-set goals for this partner / cohort.

### Step 2 — Mine the transcripts
Extract structured signal from the meeting transcripts:
- **Stated commitments** — what the partner promised (cert by X date, first deal in Y verticals, attend Z webinar).
- **Capabilities** — current product knowledge, sales motion, tooling, certifications already held.
- **Target customer profile** — verticals, segments, regions they sell into.
- **Tech stack** — what they integrate, what they resell, what they avoid.
- **Constraints** — bandwidth, competing priorities, holiday windows, hiring plans.
- **Stakeholders** — who attends QBRs, who runs marketing, who closes deals.
- **Risks raised** — anything the partner flagged as friction-likely.

If transcripts are absent, surface that and ask the user for the most recent meeting notes — *don't fabricate context*.

### Step 3 — Generate the personalized onboarding plan
Build a journey with milestones, not just a task checklist:
- **Day 0–7**: orientation + portal access + first-90-days-orientation call.
- **Day 7–30**: product certification path (tailored to partner's stated capability gaps from transcripts).
- **Day 30–60**: enablement + first co-sell motion + first deal registration target.
- **Day 60–90**: first-deal close + first QBR rhythm established.

For each milestone, generate concrete tasks with:
- **Title** (specific to this partner — not "complete training", but "complete the security competency module — required for the healthcare deals you mentioned").
- **Owner** (vendor-side CAM/technical/marketing OR partner-side stakeholder named in the transcript).
- **Due date** (relative to onboarding start, with respect for stated constraints — don't due-date through Q4 freeze if the partner mentioned it).
- **Why-it-matters note** linking back to the partner's stated commitment from the transcript.
- **Unlock** — what completing it enables (deal protection, MDF eligibility, tier eligibility).

### Step 4 — Push tasks into Introw
For every task in the plan:
- `Introw:add_task` — create the task with owner, due date, partner association, description (including the why-it-matters note).
- `Introw:update_crm_object` — update the partner record with onboarding-start date, target time-to-first-deal, stage = onboarding.
- `Introw:add_comment` — log the personalization rationale on the partner record so future CAMs can see *why* the journey was shaped this way.

### Step 5 — Set up headless project management
The skill manages this onboarding project headlessly going forward:
- Define **status checkpoints** at day 14, 30, 45, 60, 75, 90 — these become standing prompts for the user / agent to re-run a progress audit (`vendor-onboarding-progress-audit`).
- Define **escalation triggers** — task > 7 days overdue → ping CAM; engagement decay → flip to at-risk; day 75 with no first deal → activate the activation campaign skill.
- Capture all of this as comments on the partner record so the project state is queryable later.

### Step 6 — Surface the plan to the partner
- Generate a partner-facing summary of the journey (what they'll experience, what unlocks at each milestone).
- This feeds the conversational `partner-my-onboarding-progress` skill on the partner side — when the partner asks "what's next?", they get the same plan.

## Output format
- **Personalization summary** — what was extracted from transcripts and how it shaped the plan.
- **The plan** — milestone-by-milestone, with all tasks, owners, due dates, and unlock notes.
- **Confirmations** — every Introw write recorded (task IDs, comment IDs).
- **Headless management config** — checkpoint dates and escalation triggers.
- **Partner-facing journey summary** — copy-pasteable for the welcome email or portal.

## Guardrails & PRM best practice
- **Personalization > template fidelity.** A 60-task generic plan ignored is worse than a 20-task plan the partner committed to. Cut tasks the transcripts suggest are noise for this partner type.
- **Respect stated constraints.** If the partner said Q4 is a freeze for them, don't due-date critical milestones into it.
- **Don't auto-execute irreversible actions.** Confirm with the user before pushing 20+ tasks to the partner — once tasks are visible to the partner, the relationship reads them as commitments.
- **Capture the "why" trail.** Every task should be traceable back to either a transcript quote or a program-rule rationale. If you can't articulate why this task exists for this partner, drop it.
- **Single source of truth.** The plan lives in Introw, not in a separate doc. All status, progress, and changes route through Introw tools so the partner-facing agent can answer "what's next?" with current state.
- **Owner clarity is non-negotiable.** Every task has a named owner — either vendor-side or partner-side. "TBD" owners create dropped balls. If you don't know, ask.
- **Channel preference.** If the transcripts surfaced a preference (Slack > email, weekly check-in > daily), encode it as the chasing-cadence default.
- **First-deal gravity.** Every plan must include a credible path to first deal by day 75–90. Onboarding without first-deal gravity is just enrollment.
