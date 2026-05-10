---
name: vendor-email-deal-registration-watcher
description: Use when a Channel Ops, RevOps, or PDM user wants to scan the vendor's Gmail or Outlook inbox for partner emails containing deal or lead registrations — auto-extract fields, validate, deduplicate against the CRM, and process the registration through Introw. Trigger phrases include "scan inbox for deal regs", "process partner emails", "watch inbox for registrations", "auto-process deal regs from email", "find off-portal deal regs", "convert email registrations".
---

# Email Deal Registration Watcher (Vendor)

**Audience**: Vendor — **claude.ai Introw** MCP + Gmail / Outlook MCP (whichever is installed for the vendor's mailbox).
**Use case**: 08 — Deal Registration.

## Why this matters
Deal registration is the foundational transaction of every channel program — but **forms with 7+ fields drop completion 34%** (Computer Market Research), and partner portal adoption falls below 30% when submission takes >2 minutes or approval exceeds 24h. The result: partners email AEs and channel ops directly with deal registrations, creating off-portal submissions that become Salesforce data hygiene projects, attribution gaps, and channel conflict. This skill flips that pattern — instead of forcing partners back into a portal, it **harvests the email submissions they already send** and processes them cleanly through Introw with proper attribution.

Every captured registration carries **10–15 points of additional margin** through deal protection plus access to MDF and pre-sales support.

## Process

### Step 1 — Scope the inbox scan
Confirm with the user:
- Which mailbox(es)? Channel-ops shared inbox, AE inboxes, dedicated dealreg@ alias?
- Which time window? Default trailing 7 days, configurable.
- Which sender filters? E.g., only partners (skip internal threads, customer-direct).

### Step 2 — Pull candidate emails
Via Gmail / Outlook MCP:
- Search trailing window with intent keywords (deal reg, register, opportunity, lead, prospect, account, lead share, please register, can you flag) plus partner-domain filters.
- Pull email bodies + threads + attachments.
- Skip auto-replies, internal forwards (unless they wrap a partner submission).

### Step 3 — Classify per email
For each candidate:
- **Is this a deal/lead registration?** Yes / No / Maybe.
- If Yes: **what fields are present?** (account, contact, value, close date, product, qualification context).
- If Maybe: flag for human review with rationale.
- If No: skip.

### Step 4 — Identify the partner
- Match sender domain against `Introw:search_partners` to identify the partner record.
- If domain isn't recognized, surface for human review — don't attribute to "unknown partner".
- Identify the specific contact at the partner (sender name + email).

### Step 5 — Extract structured fields
Pull from the email body:
- **Account** (company name, domain).
- **Primary customer contact** (name, role, email, phone).
- **Estimated deal value** + currency.
- **Estimated close date**.
- **Product / segment**.
- **Use case / pain** (1–2 lines from email body).
- **Stage / signal** (just identified, in conversations, evaluating, ready to buy).
- Any vendor-specific custom fields configured in the form schema.

### Step 6 — Pre-flight checks
- **Required-field completeness.** If a required field is missing, draft a follow-up reply to the partner asking for it (don't submit incomplete).
- **Duplicate detection.** `Introw:search_form_submissions` and `Introw:search_crm_objects` against account name + domain. If already registered (same partner) → reply with the existing reference rather than creating a duplicate.
- **Channel conflict check.** Cross-check the account against direct pipeline + other partner registrations. If conflict, flag for human review with conflict context (don't auto-submit a contested registration).
- **Tier / eligibility.** Confirm submitting partner's tier/cert covers the product/segment per vendor rules; if not, route for human review.

### Step 7 — Submit
For clean, complete, conflict-free, eligible submissions:
- `Introw:share_lead_or_register_deal` — submit with all extracted fields and partner attribution.
- `Introw:add_comment` on the resulting deal record — capture the email source (subject, sender, timestamp) and the qualifying language from the email body so reviewers have full context.

### Step 8 — Notify the partner
- Auto-reply (or draft for human send) to the partner email confirming:
  - "Received and processed. Reference: #XYZ. Vendor SLA: 24h."
  - Deal-protection benefit reminder (10–15 pts margin).
  - Link to track status in their portal.
- For incomplete submissions, draft the targeted follow-up question.

### Step 9 — Audit trail
- `Introw:add_comment` on the partner record summarizing the processed registration.
- Mark the email read / labeled "processed" so the next sweep doesn't reprocess.
- Track exceptions (incomplete, duplicate, conflict, ineligible) in a digest for the user.

## Output format
- **Inbox sweep summary**: emails scanned, classified counts, processed counts, exceptions.
- **Per-processed**: email source, partner, account, value, submission ID, comment ID.
- **Exceptions list**: incomplete (with drafted follow-up), duplicates (with existing ref), conflicts (with context), ineligibles (with reason).
- **Suggested next actions** — e.g., human review queue.

## Guardrails & PRM best practice
- **Never silent-submit.** Echo the captured fields back in the partner-facing confirmation reply so they can correct mistakes immediately.
- **Confirm the partner identity** by domain match — never guess attribution. "Unknown partner" goes to human review.
- **Channel conflict at intake is non-negotiable.** Don't auto-submit contested registrations — that's exactly the trust-eroding miss the registration process is supposed to prevent.
- **Don't auto-approve.** This skill submits; vendor rules and `vendor-process-approval-queue` decide approval. Frame partner-facing confirmation as "received, in review per SLA," not "approved."
- **Capture the source.** Every submission's audit trail includes the email subject, sender, and timestamp via `add_comment` — auditors will ask.
- **No silent rejections.** If a submission can't be processed (duplicate, ineligible), reply to the partner with reason — silence destroys trust faster than rejection.
- **Don't reply with sensitive context.** Auto-replies confirm receipt; they don't disclose other partners' or vendor-internal data.
- **Idempotency.** Mark processed emails so a second sweep doesn't double-submit. If the inbox lacks labeling, maintain an internal seen-list.
- **Cross-skill handoff.** Conflicts feed `vendor-detect-channel-conflict`; clean submissions feed `vendor-review-deal-registrations` and `vendor-process-approval-queue`.
- **Privacy.** Customer PII in emails is processed for registration only; don't surface it in summaries that travel outside the channel ops scope.
- **Margin reminder in the confirmation reply.** Partners forget what registration earns them; the 10–15 pts deal-protection margin is the lever that drives them to register again next time.
