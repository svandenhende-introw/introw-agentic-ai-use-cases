---
name: vendor-qbr-recording-to-portal-followup
description: Use after a QBR / MBR / partner business review meeting when a PDM, CAM, or Channel Chief wants to turn the meeting recording or transcript into structured portal updates (tasks created, comments added, CRM objects updated, goals adjusted) and a polished follow-up email to attendees. Trigger phrases include "process this QBR transcript", "follow up from the partner meeting", "QBR portal update", "convert this transcript to tasks", "post-QBR action items", "send the QBR recap", "update Introw from the meeting".
---

# QBR Recording → Portal Updates + Follow-Up (Vendor)

**Audience**: Vendor — uses **claude.ai Introw** MCP + transcript MCP (Otter, Fathom, Gong, Read.ai, Granola — or a transcript pasted into the conversation).
**Use case**: 12 — QBRs / Meeting Prep (post-meeting companion to `vendor-qbr-prep`).

## When to use this skill

Use after a QBR / MBR / partner business review meeting when a PDM, CAM, or Channel Chief wants to turn the meeting recording or transcript into structured portal updates (tasks created, comments added, CRM objects updated, goals adjusted) and a polished follow-up email to attendees.

**Sample prompts that fire this skill:**
- "process this QBR transcript"
- "follow up from the partner meeting"
- "QBR portal update"
- "convert this transcript to tasks"
- "post-QBR action items"
- "send the QBR recap"
- "update Introw from the meeting"

## Why this matters
Most QBRs end with good intentions and zero follow-through. The PDM types up notes (sometimes), promises to update the portal "later," drafts an email (eventually), and three weeks later the partner is asking what was decided. The decisions made in the meeting age into ambiguity; commitments slip; the next QBR rehashes the same ground.

This skill closes the loop: meeting transcript → structured portal updates → attendee email — same day, automatically, with no PDM tax. It's the post-meeting half of the QBR motion that `vendor-qbr-prep` started. Pair the two and the QBR becomes an actual operating ritual instead of a slide deck.

## Inputs to gather first
- **Source**: meeting transcript (pasted text, transcript MCP reference, or a recording the user has already transcribed elsewhere).
- **Partner identity** + portal/CRM record.
- **Attendees** (pulled from transcript or supplied) — needed for the follow-up email.
- **Meeting type**: QBR (default), MBR, WBR, ad-hoc strategic review.
- **Action authorization**: write to portal directly, or surface drafts for PDM approval first?

## Process

### Step 1 — Extract structured signal from the transcript
Mine the transcript for:

- **Decisions made** — specific yes/no calls. ("We agreed to expand into healthcare in Q3.")
- **Commitments** — who promised what by when. Vendor commitments AND partner commitments.
- **Action items** — concrete tasks with owners.
- **Blockers / risks raised** — partner flagged something that needs attention.
- **Goal updates** — any commitments to revise or set new goals.
- **Pipeline changes** — deals discussed (new, in-flight, slipped, killed).
- **Tier / program asks** — partner asking for tier promotion, MDF, certification support.
- **Sentiment signals** — any major positive (advocacy moment) or negative (frustration, churn risk).
- **Next QBR / next-touch date.**

For each extraction, capture the source quote (with timestamp if available) — the audit trail.

### Step 2 — Pull current state for context
Before writing anything, pull current state to avoid duplicating or contradicting existing data:
- `Introw:search_partners` — partner record.
- `Introw:search_tasks` — open tasks already assigned (don't double-create).
- `Introw:search_crm_objects` — open deals that may need updating.
- `Introw:get_goals` — current goals before any revisions.

### Step 3 — Stage the writes (preview, don't execute yet)
Build a write plan, not a write. For each extracted item, prepare the corresponding portal action:

| Extracted | Portal action |
|---|---|
| Action item with owner + due date | `Introw:add_task` (with title, owner, due date, partner association, why-note linked to transcript timestamp) |
| Commitment, decision, or sentiment-worthy moment | `Introw:add_comment` on the partner record |
| Deal stage change / value update / new deal mentioned | `Introw:update_crm_object` (or `Introw:share_lead_or_register_deal` if new) |
| Goal revised or new goal committed | Comment + flag for human update (goal write-back may need approval) |
| Tier / MDF ask raised | Comment + task to relevant approver |
| Risk / churn signal | Comment with flag + task to PDM for follow-up |
| Next QBR date | Calendar task with the date |

### Step 4 — Surface the write plan
Show the user:
- **Tasks to create** — title, owner, due date, why.
- **Comments to add** — content + which record.
- **CRM updates** — what's changing, before/after.
- **Goals affected** — flagged for separate confirmation (goals carry economic weight).
- **Risks flagged** — anything that warrants escalation.

User approves, edits, or rejects per item. **Default mode: surface; auto-execute only when explicitly authorized.**

### Step 5 — Execute approved writes
- `Introw:add_task` for each approved task.
- `Introw:add_comment` for each comment, including the QBR summary as a comprehensive comment on the partner record (so the next QBR has the full thread).
- `Introw:update_crm_object` for each approved CRM update.
- For goal changes: capture as a comment + create a task for the goals-owner to confirm and apply (don't auto-write goal targets).

### Step 6 — Draft the follow-up email
Generate an email to the meeting attendees with this structure:

- **Subject**: "Recap & next steps — [Partner] x [Vendor] [QBR / MBR / Review] — [Date]"
- **Opening**: thank-you + 1-line meeting purpose recap.
- **What we agreed** (decisions — bulleted, concrete).
- **What we'll do** (vendor-side action items with owners + dates).
- **What you'll do** (partner-side action items with owners + dates).
- **What's next** (next-touch date, what'll be reviewed).
- **Attachments / links**: portal task IDs created, any decks shared, the recording (if attendee policy allows).

Tone: warm but specific. No hedging. The email should be the source of truth the partner can forward to their team. If something was discussed but not decided, say "to revisit next [touchpoint]" — don't fudge.

### Step 7 — Send (or stage for send)
- **Default**: surface the drafted email for PDM review and send via the PDM's regular email tool.
- If a Gmail/Outlook MCP is connected and the user authorizes auto-send: send directly.
- Capture the sent email body via `Introw:add_comment` on the partner record so the email is part of the audit trail.

## Output format
- **Extraction summary** — what was identified in the transcript, with source quotes.
- **Portal write plan** — tasks, comments, CRM updates, goal flags, risk flags. Each approved/rejected by the user.
- **Confirmation log** — for each executed write, the IDs created/updated.
- **Follow-up email draft** — copy-pasteable or sendable.
- **Open items requiring human follow-through** — anything ambiguous or sensitive flagged for the PDM.

## Guardrails & PRM best practice
- **Don't fabricate.** If the transcript is ambiguous on owner or date, ask the PDM rather than guess. Wrong owners and dates create more friction than no tasks.
- **Preserve nuance.** Some QBR moments aren't decisions — they're explorations. Don't capture an exploratory mention as a commitment. The bar: was there explicit agreement?
- **Sensitive content stays out of broad audiences.** If the meeting included confidential pricing discussion, churn-risk admissions, or competitor intel, scrub those from the follow-up email — capture in vendor-internal comments only.
- **Owners must be named.** "TBD" owners create dropped balls. Every task needs a name.
- **Don't update goals without authorization.** Goal targets carry economic weight (commission impact, tier eligibility). Goal changes get flagged for explicit confirmation, never auto-written.
- **Source quotes on every extraction.** The audit trail is the source quote + timestamp. When the partner disputes an action item six weeks later ("we never agreed to that"), the timestamp resolves it.
- **Don't auto-execute on first run.** First time the user runs this skill: preview everything. After the user has trusted the extraction quality on 2–3 meetings, auto-execution mode can be enabled for low-risk writes (tasks, comments) — never goal writes or tier moves.
- **Email tone is editable.** The drafted email is a starting point. The PDM's relationship voice matters; encourage edits. If the partner has a long history of formal English, don't ship a casual draft.
- **Privacy of recordings.** Some partners don't consent to recording, and some jurisdictions have specific rules. Confirm consent context before processing.
- **Escalate risks immediately.** Churn signals, legal flags, security issues — surface to channel leadership the same day, don't bury them in the digest.
- **Cross-skill handoff.** New deals identified → `partner-register-deal` flow or `vendor-pipeline-partner-influence-scout`. Coaching needs surfaced → `vendor-deal-coach-from-similar-wins`. Goal revisions → vendor goals-owner. Tier asks → `vendor-tier-promotion-batch-review` for next cycle. Pairs naturally with `vendor-qbr-prep`: prep generates the meeting, this skill closes the loop after.
