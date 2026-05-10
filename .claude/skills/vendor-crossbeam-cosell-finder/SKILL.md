---
name: vendor-crossbeam-cosell-finder
description: Use when a Channel Chief, RevOps, AE-aligned Channel Manager, or PDM wants to find the best partner(s) to bring into a target account list — by combining Crossbeam (or Reveal) overlap data with Introw partner performance signals. Trigger phrases include "find partners that overlap with these accounts", "Crossbeam co-sell", "ELG partner match", "who already has the customer", "ecosystem-led match", "best partner for this target list", "warmest overlap on Account X".
---

# Crossbeam Co-Sell Partner Finder (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP + **claude.ai Crossbeam** MCP (works with Reveal too if installed).
**Use case**: 02 — Partner Segmentation (with strong cross-cut to 08 Deal Registration / 11 Coaching).

## When to use this skill

Use when a Channel Chief, RevOps, AE-aligned Channel Manager, or PDM wants to find the best partner(s) to bring into a target account list — by combining Crossbeam (or Reveal) overlap data with Introw partner performance signals.

**Sample prompts that fire this skill:**
- "find partners that overlap with these accounts"
- "Crossbeam co-sell"
- "ELG partner match"
- "who already has the customer"
- "ecosystem-led match"
- "best partner for this target list"
- "warmest overlap on Account X"

## Why this matters
Ecosystem-Led Growth (ELG) only works when the ecosystem data is operationalized. Most channel teams have Crossbeam (or Reveal) producing overlap data weekly — and most of that data dies in a spreadsheet because no one has time to translate "Partner X has a customer relationship with Account Y" into a concrete co-sell motion. This skill closes that gap: it cross-checks a target account list against partner overlap data, scores partner-account fit using Introw performance signals (engagement, prior similar wins, certifications), and drafts the partner intro request.

For partners involved in deals: industry research consistently shows partner-influenced deals close at materially higher win rates and larger ACVs than vendor-direct equivalents in the same segment — but only when the *right* partner is matched to the *right* deal.

## Inputs to gather first
- **Target account list**: open opportunities, ABM target accounts, expansion candidates, churned-customer reactivation list, or a stage-filter on the CRM.
- **Motion intent**: warm intro from partner / co-sell / channel-led full ownership / referral / customer reference.
- **Partner constraints**: tier eligibility, region, vertical, partner type (SI, reseller, referral, MSP).

## Process

### Step 1 — Pull the target account list
- `Introw:search_crm_objects` — open deals in scope, or filter by stage / segment / region.
- Or accept the account list pasted in by the user.
- Capture each target's domain, segment, vertical, deal value, stage.

### Step 2 — Pull overlap data from Crossbeam
- `Crossbeam:*` — for each target account, identify which partners have a customer relationship, opp, or evaluation in flight on that account.
- Capture overlap *type* (customer / opp / champion / lapsed) — not just presence. A partner whose customer is your target is much warmer than a partner whose lapsed prospect is your target.
- Capture overlap *recency* — fresh overlaps beat stale ones.

### Step 3 — Enrich with Introw partner performance
For each candidate partner-account match:
- `Introw:search_partners` — partner record (tier, region, vertical specialization, partner type).
- `Introw:search_crm_objects` — has this partner closed similar deals before (vertical × deal size × product)?
- `Introw:search_partner_engagement` — recent engagement intensity. A partner with the right overlap who's been silent for 90 days is a different play than one who's actively engaged.
- `Introw:get_tier_information` — tier eligibility for the product/segment.

### Step 4 — Score partner-account fit
For each candidate match, combine:
- **Overlap strength** (customer > opp > champion > lapsed)
- **Overlap recency** (last 90 days > older)
- **Partner-deal historical fit** (vertical × deal size × product match)
- **Current engagement** (active vs. dormant)
- **Tier / certification eligibility** (hard pass if not eligible)
- **Channel-conflict cleanliness** — cross-check existing registrations to avoid placing partners on contested accounts.

### Step 5 — Match the right partner per account
For each target account, select 1–3 partner candidates with the strongest case. For each, articulate the *why* in one sentence:
- "Partner A — has a 3-year customer relationship at Globex; recent engagement; closed 5 similar healthcare deals; Gold-tier and certified on relevant product."

### Step 6 — Draft the motion
- For warm intro: draft a partner-facing message with the specific account, why we're asking, what's in it for them (margin, MDF eligibility, deal protection).
- For co-sell registration: pre-fill `share_lead_or_register_deal` payload and surface for vendor approval.
- For full handoff: draft the AE-to-partner handoff email with prospect context.

### Step 7 — Capture and queue
- `Introw:add_comment` on the deal record with the matched partner + rationale.
- `Introw:add_task` for the AE or PDM to make the intro by a target date.
- If auto-action is enabled and conflict is clean: submit the registration via `share_lead_or_register_deal` with the captured context.

## Output format
- **Account-by-account match table**: account, value, stage, top-1/top-3 partner candidates, overlap type, overlap recency, fit score, why.
- **Drafted partner-facing messages** per match, copy-pasteable.
- **Registration payloads** for clean matches, ready for approval.
- **Conflict flags** — accounts with existing registrations or direct claims, surfaced not auto-actioned.
- **Aggregate insight**: which partners had the most matchable overlaps (informs future ABM/recruitment targeting).

## Guardrails & PRM best practice
- **Overlap data has lag.** Crossbeam refreshes typically run nightly or weekly; flag stale data and avoid acting on overlaps > 30 days old without confirmation.
- **Privacy & data sharing rules.** Crossbeam-shared data is scoped to your population groups; only surface overlaps within authorized data-sharing agreements. Never surface partner customer names outside the vendor-internal scope.
- **Channel conflict before action.** Always run conflict detection (existing registrations, direct claim, named-account list) before recommending placement. Crossbeam overlap doesn't override rules of engagement.
- **Don't poach.** Overlap with another partner's customer doesn't mean the second partner gets the deal — surface the existing relationship as context, not as a takeover signal.
- **Why beats overlap.** A weak overlap with strong fit (vertical, prior wins) often beats a strong overlap with weak fit. Don't let raw overlap count dominate scoring.
- **Tier-aware match.** Strategic deals to top-tier partners with proven enterprise motion; transactional deals to volume partners. Mismatching destroys margin and partner energy.
- **No auto-execution on first run.** Surface matches and rationale; let the human approve the first batch. Once the user has validated the matching logic, auto-action mode (auto-registration on clean matches) can be enabled.
- **Capture decisions** via `Introw:add_comment` on each deal — the AE/CAM picking it up next week needs to see why this partner was placed.
- **Respect dormant partners' state.** A perfect-overlap partner who's silent for 90+ days needs an activation play (`vendor-activate-network-with-personalized-campaigns`) before placement — not a deal handoff cold.
- **Cross-skill handoff.** Clean placements that need coaching → `vendor-deal-coach-from-similar-wins`. Conflicts → conflict-resolution flow. Coverage gaps revealed by the analysis → `vendor-acquisition-abm-orchestrator` (we should be recruiting partners for these segments).
