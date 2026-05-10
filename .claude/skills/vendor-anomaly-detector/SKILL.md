---
name: vendor-anomaly-detector
description: Use when a Channel Chief, RevOps, or PDM wants a continuous-monitoring scan across the partner ecosystem to surface unusual behaviors — sudden activity drops or spikes, atypical deal patterns, dormant-partner reactivations, register-then-stall sequences, abnormal goal pacing — before they show up as quarterly surprises. Trigger phrases include "anomaly check", "what's unusual this week", "weird partner behavior", "spot the outliers", "ecosystem anomalies", "what changed materially".
---

# Ecosystem Anomaly Detector (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP.
**Use case**: 14 — Ecosystem Performance.

## When to use this skill

Use when a Channel Chief, RevOps, or PDM wants a continuous-monitoring scan across the partner ecosystem to surface unusual behaviors — sudden activity drops or spikes, atypical deal patterns, dormant-partner reactivations, register-then-stall sequences, abnormal goal pacing — before they show up as quarterly surprises.

**Sample prompts that fire this skill:**
- "anomaly check"
- "what's unusual this week"
- "weird partner behavior"
- "spot the outliers"
- "ecosystem anomalies"
- "what changed materially"

## Why this matters
Ad-hoc analytics requests consume **30–50% of channel RevOps team capacity**. Most channel programs catch material changes weeks late — partner X went dark in week 2, nobody noticed until the QBR in week 12. Continuous anomaly detection makes the program **operationally responsive** instead of retrospective: when something unusual happens, somebody knows within days, not quarters.

The companion to `vendor-detect-at-risk-partners` (which scores per-partner risk) — anomaly detection works **ecosystem-wide**, finding patterns the per-partner view misses (cohort-level shifts, segment-wide engagement drops, unusual deal-size spikes).

## Anomaly classes to detect

1. **Activity drop**: partner whose 30-day engagement is below their trailing 90-day baseline by > 50%.
2. **Activity spike**: partner whose engagement is suddenly > 2× their baseline (worth understanding — opportunity or noise).
3. **Dormant reactivation**: partner who was inactive 60+ days and just registered a deal or logged in.
4. **Register-and-stall**: partner who registered a deal but no follow-up activity in 14+ days.
5. **Deal-size outlier**: registration with deal value > 3× the partner's historical average (legitimate big deal or data error).
6. **Stage-velocity anomaly**: deals stuck in stage > 2× the cohort median for that stage.
7. **Tier-pace divergence**: partner pacing materially above or below their tier's median run-rate.
8. **Goal-pace cliff**: partner who was on track for a goal and suddenly fell off-pace this week.
9. **Cohort-level shifts**: a whole segment (region, tier, partner type) showing aggregate unusual movement (e.g., DACH SI registrations halved this week).
10. **Concentration risk**: an unusual fraction of new pipeline coming from a single partner — celebrate but flag.

## Process

### Step 1 — Define the scope
- Default: full active partner base, trailing 7-day window vs. trailing 90-day baseline.
- Optional: scope to tier, region, partner type, or a specific cohort.
- Sensitivity setting: aggressive (flag > 1σ deviations) vs. conservative (> 2σ). Default conservative — false-positive fatigue is the enemy.

### Step 2 — Pull baseline + current state
- `Introw:search_partners` — base set with tier, lifecycle stage, region.
- `Introw:search_partner_engagement` — engagement over current window AND baseline window.
- `Introw:search_crm_objects` — deal stage / value / velocity over both windows.
- `Introw:search_form_submissions` — registration cadence.
- `Introw:get_goals` — goal pacing vs. expected run-rate.
- `Introw:search_commissions` — commission events as a performance proxy.

### Step 3 — Compute deviations per partner per signal
For each partner × signal:
- Compute current-window value.
- Compute trailing baseline (90-day median).
- Flag deviations beyond the configured sensitivity threshold.
- Annotate each flag with: signal name, current value, baseline, % deviation, plausible explanations.

### Step 4 — Cluster and classify
- **Per-partner**: how many signals are flagged for the same partner? Multi-signal flags (engagement drop + goal-pace cliff + register-and-stall) score higher than single-signal flags.
- **Per-cohort**: aggregate flags by tier / region / partner type to spot ecosystem-level shifts.
- **Per-class**: which anomaly classes are firing most this week?

### Step 5 — Filter for signal quality
- Suppress known-explainable: holidays, vendor-side outages, expected seasonality.
- Suppress noisy: very small partners where 1–2 events shift percentages dramatically.
- Suppress already-flagged: don't re-surface anomalies escalated last week unless they got worse.

### Step 6 — Surface for action
- **High-priority anomalies**: top 5–10, ranked by severity × revenue exposure.
- **Watch list**: 10–20 secondary flags worth knowing.
- **Cohort-level findings**: anything ecosystem-wide.
- **Recommended action** per high-priority item: who should look at it, what skill to run next (`vendor-detect-at-risk-partners`, `vendor-coach-partner-deal`, `vendor-activate-network-with-personalized-campaigns`, etc.).

## Output format
- **Top anomalies** table: partner, anomaly class, severity, revenue exposure, recommended next action, owner.
- **Watch list** (less urgent).
- **Cohort findings** (ecosystem-wide patterns).
- **Suppression log** — what was filtered out and why (transparency for trust calibration).
- **Comparison to last run** — what's new vs. what's been on the list.

## Guardrails & PRM best practice
- **Anomaly ≠ problem.** Some anomalies are good news (a dormant partner just registered a $500K deal). The skill flags unusual; the human decides if it's celebrate, intervene, or ignore.
- **Conservative defaults.** False positives erode trust faster than false negatives. Better 5 high-quality flags than 50 noisy ones.
- **Always state the window.** Anomalies are window-relative; without explicit windows, comparisons are meaningless.
- **Suppress small-N noise.** A partner with 3 lifetime registrations doesn't have a stable baseline; flag thresholds need minimum-sample-size guards.
- **Pair with explanation.** Don't surface a flag without context. "Engagement dropped 60%" is not actionable; "Engagement dropped 60% — last activity was 12 days ago, prior cadence was every 3 days, no recent CRM updates either" is.
- **Don't auto-act.** Surface, don't act. Anomaly-driven auto-actions risk over-correcting on noise.
- **Run on cadence.** Daily for active programs, weekly for smaller. Anomalies discovered three weeks late aren't anomalies anymore — they're confirmed problems.
- **Feed the digest.** This skill's output is the natural input for `vendor-slack-weekly-channel-digest`'s "Anomalies" section.
- **Capture decisions.** When an anomaly is investigated and resolved (or dismissed), log via `Introw:add_comment` on the relevant partner so the next run has context for suppression.
- **Cross-skill handoff.** Per-partner anomalies → `vendor-detect-at-risk-partners` for full risk-scoring; segment-wide drops → `vendor-activate-network-with-personalized-campaigns` for cohort intervention; deal-velocity issues → `vendor-coach-partner-deal` or `vendor-deal-coach-from-similar-wins`.
