"""Skill workflow visualization specs + renderer."""
import html as html_lib

# Per-skill workflow specs.
# Each stage tuple: (label, node_type, title, [(tool_id, tool_label), ...])
# node_type: trigger | agent | system | decision | human | outcome
SKILL_VISUALS = {
    # ========= UC01 — Partner Acquisition =========
    "vendor-acquisition-abm-orchestrator": {
        "title": "Top performers + ecosystem reach → joint-value ABM",
        "stages": [
            ("Inputs", "trigger", "Top performers + strategic goals + ICP playbook",
             [("salesforce", "Salesforce"), ("hubspot", "HubSpot"), ("introw", "Introw goals"), ("notion", "Notion")]),
            ("Agent + signals", "agent", "Pattern + ecosystem reach",
             [("introw", "Introw"), ("crossbeam", "Crossbeam")]),
            ("Sourcing", "system", "Net-new lookalike targets",
             [("clay", "Clay"), ("zoominfo", "ZoomInfo"), ("apollo", "Apollo")]),
            ("Outcome", "outcome", "ABM outreach + portal pre-config",
             [("introw", "Introw Portal"), ("gmail", "Gmail / Outlook")]),
        ],
    },
    # ========= UC02 — Partner Segmentation =========
    "vendor-tier-promotion-batch-review": {
        "title": "Quarterly tier review · evidence-grounded · drafted comms",
        "stages": [
            ("Whole partner base", "trigger", "Tier · revenue · certs · goals · engagement + tier rules",
             [("introw", "Introw"), ("salesforce", "CRM"), ("hubspot", "CRM"), ("notion", "Notion")]),
            ("Score", "agent", "Eligibility per criterion · sustained-quarter bar",
             [("introw", "Introw")]),
            ("Bucket", "decision", "Promote · Hold · Demote · Watch",
             [("introw", "Introw")]),
            ("Comms + exec sign-off", "outcome", "Drafted per-partner messages · tier writes",
             [("gmail", "Email"), ("introw", "Introw")]),
        ],
    },
    "vendor-crossbeam-cosell-finder": {
        "title": "Target accounts → warmest partner overlap → drafted intro",
        "stages": [
            ("Target list", "trigger", "Open opps · ABM · expansion candidates",
             [("salesforce", "Salesforce"), ("hubspot", "HubSpot")]),
            ("Pull overlaps", "system", "Customer · opp · champion · lapsed",
             [("crossbeam", "Crossbeam")]),
            ("Score partner-fit", "agent", "Overlap × engagement × prior wins",
             [("introw", "Introw")]),
            ("Outcome", "outcome", "Drafted intro · pre-filled registration",
             [("introw", "Introw"), ("gmail", "Email"), ("slack", "Slack")]),
        ],
    },
    # ========= UC03 — Onboarding =========
    "vendor-personalized-onboarding-from-transcripts": {
        "title": "Kickoff transcript → personalized 90-day plan, headlessly managed",
        "stages": [
            ("Kickoff context", "trigger", "Transcript + existing partner data",
             [("otter", "Otter"), ("fathom", "Fathom"), ("gong", "Gong"), ("salesforce", "CRM")]),
            ("Mine + plan", "agent", "Commitments · capabilities · constraints (templates from playbook)",
             [("introw", "Introw"), ("notion", "Notion")]),
            ("Push tasks", "system", "Owners · due dates · why-notes",
             [("introw", "Introw")]),
            ("Headless run", "outcome", "Multi-channel chase + checkpoints",
             [("slack", "Slack"), ("teams", "Teams"), ("gmail", "Email")]),
        ],
    },
    "partner-cross-vendor-onboarding-tracker": {
        "title": "Every open onboarding across every vendor in one view",
        "stages": [
            ("All portals", "trigger", "Enumerate vendor portals",
             [("introw-connect", "Introw Connect")]),
            ("Pull state", "system", "Tasks · goals · engagement · first-deal status",
             [("introw-connect", "Introw Connect")]),
            ("Compute", "agent", "% complete · 90-day cliff · risk · unlocks",
             [("introw-connect", "Introw Connect")]),
            ("Scoreboard", "outcome", "Cross-vendor view + next-move recos",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    "partner-onboarding-prioritizer": {
        "title": "Which onboarding to advance today · ROI-ranked",
        "stages": [
            ("Active onboardings", "trigger", "Filter to in-flight only",
             [("introw-connect", "Introw Connect")]),
            ("Score", "agent", "Urgency × upside × sunk effort × momentum",
             [("introw-connect", "Introw Connect")]),
            ("ROI of next action", "decision", "Marginal value per hour spent",
             [("introw-connect", "Introw Connect")]),
            ("Today's focus", "outcome", "Top 1–3 moves with effort + payoff",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    # ========= UC04 — Activation =========
    "vendor-activate-network-with-personalized-campaigns": {
        "title": "Network audit → goal-driven activation campaigns",
        "stages": [
            ("Audit", "trigger", "Goals · engagement · pipeline · tasks",
             [("introw", "Introw"), ("salesforce", "Salesforce"), ("hubspot", "HubSpot")]),
            ("Diagnose", "decision", "Per-partner blocker",
             [("introw", "Introw")]),
            ("Personalized message", "agent", "Mapped to goal + blocker (templates from playbook)",
             [("introw", "Introw"), ("notion", "Notion")]),
            ("Distribute + measure", "outcome", "Right channel · re-audit at 14 days",
             [("slack", "Slack"), ("teams", "Teams"), ("gmail", "Email")]),
        ],
    },
    "partner-renewal-and-expansion-coordinator": {
        "title": "Every customer · every vendor · one renewal calendar",
        "stages": [
            ("All portals", "trigger", "Enumerate vendor portals",
             [("introw-connect", "Introw Connect")]),
            ("Pull contracts", "system", "Renewal dates + expansion signals",
             [("introw-connect", "Introw Connect")]),
            ("Score plays", "agent", "Health × adjacent fit × multi-vendor coordination",
             [("introw-connect", "Introw Connect")]),
            ("Outreach plan", "outcome", "Drafted customer + CAM pings",
             [("gmail", "Email"), ("slack", "Slack")]),
        ],
    },
    # ========= UC05 — Training =========
    "vendor-microcourse-from-closed-lost": {
        "title": "Loss patterns OR a knowledge base → micro-courses, deployable in under an hour",
        "stages": [
            ("Source", "trigger", "Closed-lost partner deals + lost-reasons",
             [("salesforce", "Salesforce"), ("hubspot", "HubSpot"), ("introw", "Introw")],
             [("trigger", "Or: existing knowledge-base content directly",
               [("notion", "Notion"), ("confluence", "Confluence"), ("gdrive", "Drive"), ("box", "Box")])]),
            ("Cluster + diagnose", "agent", "Failure patterns → underlying gap (when loss-driven)",
             [("introw", "Introw")]),
            ("Generate course", "system", "Outline · worked example · open-question rubric",
             [("introw", "Introw")]),
            ("Distribute", "outcome", "Targeted to partners working similar pipeline",
             [("introw", "Introw tasks"), ("gmail", "Email"), ("slack", "Slack")]),
        ],
    },
    "partner-cross-vendor-cert-tracker": {
        "title": "20–50 active certs across vendors · ranked by economic stakes",
        "stages": [
            ("All portals", "trigger", "Enumerate vendor portals",
             [("introw-connect", "Introw Connect")]),
            ("Pull cert state", "system", "Held · expiring · gating SKUs · tier-promo",
             [("introw-connect", "Introw Connect")]),
            ("Score stakes", "agent", "Cost of expiry × tier leverage × renewal effort",
             [("introw-connect", "Introw Connect")]),
            ("Calendar + study plan", "outcome", "Action queue · skip list · tier bridges",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    # ========= UC06 — Enablement Support =========
    "vendor-support-content-gap-detector": {
        "title": "What partners actually ask · vs · what your KB answers",
        "stages": [
            ("Support events", "trigger", "Tickets · comments · form intake",
             [("introw", "Introw"), ("intercom", "Intercom"), ("slack", "Slack")]),
            ("Cluster by intent", "agent", "Pricing · how-to · battle card · compliance · …",
             [("introw", "Introw")]),
            ("Cross-check KB", "system", "Strong / partial / weak / missing per cluster",
             [("notion", "Notion"), ("confluence", "Confluence"), ("box", "Box"), ("gdrive", "Drive")]),
            ("Roadmap", "outcome", "Top 3–5 content investments ranked by ROI",
             [("introw", "Introw")]),
        ],
    },
    "partner-helpdesk": {
        "title": "Partner question → cited answer or scoped action — single vendor",
        "stages": [
            ("Trigger", "trigger", "Partner asks in their flow",
             [("claude", "Claude"), ("slack", "Slack"), ("teams", "Teams"), ("portal", "Portal")]),
            ("Triage", "decision", "Knowledge · lookup · scoped action",
             [("introw-connect", "Introw Connect")]),
            ("Resolve", "system", "KB · CRM · capability matrix",
             [("notion", "Notion"), ("confluence", "Confluence"), ("introw-connect", "Introw Connect")]),
            ("Outcome", "outcome", "Cited answer · scoped action · audit log",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    # ========= UC07 — Campaigns =========
    "vendor-content-radar": {
        "title": "Source scan → partner-ready outreach · including release notes",
        "stages": [
            ("Sources", "trigger", "Release notes · LinkedIn · blog · Loom",
             [("notion", "Release notes"), ("linkedin", "LinkedIn"), ("loom", "Loom")]),
            ("Filter + transform", "agent", "Relevance · 3 derivatives per item",
             [("introw", "Introw")]),
            ("Segment", "system", "Tier · region · vertical · type",
             [("introw", "Introw")]),
            ("Distribute + track", "outcome", "Right channel · engagement-tracked",
             [("gmail", "Email"), ("slack", "Slack"), ("teams", "Teams"), ("portal", "Portal")]),
        ],
    },
    "partner-cross-vendor-content-calendar": {
        "title": "Every vendor's launches · MDF · webinars · in one calendar",
        "stages": [
            ("All portals", "trigger", "Enumerate vendor portals",
             [("introw-connect", "Introw Connect")]),
            ("Pull activity", "system", "Launches · MDF windows · webinars · tier reviews",
             [("introw-connect", "Introw Connect")]),
            ("Score relevance", "agent", "Customer-base fit × motion fit × leverage",
             [("introw-connect", "Introw Connect")]),
            ("Calendar + plan", "outcome", "Weekly action queue + drafted outreach",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    # ========= UC08 — Deal Registration =========
    "vendor-email-deal-registration-watcher": {
        "title": "Off-portal email submissions captured cleanly",
        "stages": [
            ("Inbox scan", "trigger", "Vendor mailbox sweep",
             [("gmail", "Gmail"), ("outlook", "Outlook")]),
            ("Classify + extract", "agent", "Detect intent · pull fields · attribute",
             [("introw", "Introw")]),
            ("Pre-flight", "decision", "Duplicate · conflict · eligibility",
             [("introw", "Introw"), ("salesforce", "CRM")]),
            ("Submit + confirm", "outcome", "Clean submission · partner notified",
             [("introw", "Introw"), ("gmail", "Email")]),
        ],
    },
    "vendor-pipeline-partner-influence-scout": {
        "title": "Direct-deal rescue: Crossbeam overlap → partner placement",
        "stages": [
            ("Open pipeline", "trigger", "Direct-sales deals + accounts",
             [("salesforce", "Salesforce"), ("hubspot", "HubSpot")]),
            ("Score leverage", "agent", "Vertical · geo · services · stalled · stack",
             [("introw", "Introw")]),
            ("Match partner", "system", "Existing customer (Crossbeam) + prior wins",
             [("introw", "Introw"), ("crossbeam", "Crossbeam")]),
            ("Place + comment", "outcome", "Registration · context-rich comment · AE task",
             [("introw", "Introw"), ("slack", "Slack")]),
        ],
    },
    "partner-pipeline-influence-companion": {
        "title": "Partner sees vendor accounts where they have unique influence",
        "stages": [
            ("Accessible pipeline", "trigger", "Vendor accounts visible to partner",
             [("introw-connect", "Introw Connect")]),
            ("Identify fit", "agent", "Existing customer · vertical · geo · prior wins",
             [("introw-connect", "Introw Connect")]),
            ("Frame value", "system", "Why-you-fit + what registration unlocks",
             [("introw-connect", "Introw Connect")]),
            ("Act", "outcome", "Register · place-me-on · context comment",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    "partner-prospect-to-vendor-fit-finder": {
        "title": "New prospect → which vendor first · pre-staged registrations",
        "stages": [
            ("Prospect", "trigger", "Stack · segment · vertical · pain",
             [("claude", "Claude"), ("slack", "Slack")]),
            ("Score per vendor", "agent", "Vertical · segment · stack · track record · tier",
             [("introw-connect", "Introw Connect")]),
            ("Sequence", "decision", "Lead · Attach · Hold · Skip",
             [("introw-connect", "Introw Connect")]),
            ("Pre-stage", "outcome", "Registration payloads ready to file",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    "partner-registration-status-tracker": {
        "title": "Every registration across vendors · sorted by urgency",
        "stages": [
            ("All portals", "trigger", "Enumerate vendor portals",
             [("introw-connect", "Introw Connect")]),
            ("Pull state", "system", "Pending · approved · conflict · expiring",
             [("introw-connect", "Introw Connect")]),
            ("Classify urgency", "decision", "Red · yellow · green",
             [("introw-connect", "Introw Connect")]),
            ("Action queue", "outcome", "Drafted CAM pings · conflict responses",
             [("introw-connect", "Introw Connect"), ("gmail", "Email")]),
        ],
    },
    # ========= UC11 — Deal Coaching =========
    "vendor-deal-coach-from-similar-wins": {
        "title": "This specific partner deal · coached from your past wins",
        "stages": [
            ("The specific deal", "trigger", "The active partner deal in flight",
             [("salesforce", "Deal record"), ("hubspot", "Deal record")],
             [("trigger", "Stage · activity · objections · stakeholders",
               [("introw", "Introw"), ("slack", "Last comments")])]),
            ("Find comparables", "system", "Similar vertical · size · product · partner type",
             [("introw", "Introw"), ("notion", "Notion"), ("gong", "Gong"), ("chorus", "Chorus")]),
            ("Extract pattern", "agent", "What worked · per stage · objection lines · assets",
             [("introw", "Introw")]),
            ("Deliver", "outcome", "Persona-aware · in workspace · captured to deal",
             [("slack", "Slack"), ("teams", "Teams"), ("salesforce", "CRM")]),
        ],
    },
    "partner-deal-war-room": {
        "title": "Partner's specific deal · coaching packet in seconds",
        "stages": [
            ("The specific deal", "trigger", "The partner's deal in flight",
             [("introw-connect", "Deal record")],
             [("trigger", "Recent activity · last comments · open tasks",
               [("salesforce", "CRM"), ("slack", "Slack")])]),
            ("Pull assets", "system", "Vendor playbook · battle cards · similar wins · calls",
             [("notion", "Notion"), ("confluence", "Confluence"), ("gong", "Gong")]),
            ("Stage-aware coach", "agent", "Top 3 moves · objection lines · drafted message",
             [("introw-connect", "Introw Connect")]),
            ("Deliver in workspace", "outcome", "Captured to deal + tracked",
             [("slack", "Slack"), ("teams", "Teams"), ("gmail", "Email")]),
        ],
    },
    # ========= UC12 — QBRs =========
    "vendor-qbr-prep": {
        "title": "Full QBR draft in ~10s · 100% partner coverage feasible",
        "stages": [
            ("Pull connected systems", "trigger", "Pipeline · goals · engagement · commissions",
             [("salesforce", "Salesforce"), ("hubspot", "HubSpot"), ("introw", "Introw"), ("finance", "Finance")]),
            ("Generate", "agent", "Full draft · risks at top · agenda (template from playbook)",
             [("introw", "Introw"), ("notion", "Notion")]),
            ("Coverage sweep", "system", "Single partner OR book-wide",
             [("introw", "Introw")]),
            ("PDM 15-min edit", "outcome", "Strategic refinement · ship",
             [("introw", "Introw")]),
        ],
    },
    "vendor-qbr-recording-to-portal-followup": {
        "title": "Meeting → tasks · comments · CRM updates · email — same day",
        "stages": [
            ("Recording", "trigger", "QBR transcript / recording",
             [("otter", "Otter"), ("fathom", "Fathom"), ("gong", "Gong"), ("zoom", "Zoom")]),
            ("Extract", "agent", "Decisions · commitments · risks · next-touch",
             [("introw", "Introw")]),
            ("Stage writes", "decision", "Tasks · comments · CRM updates · goal flags",
             [("introw", "Introw")]),
            ("Close the loop", "outcome", "Approved writes + drafted attendee email",
             [("introw", "Introw"), ("gmail", "Gmail / Outlook")]),
        ],
    },
    "partner-pre-qbr-self-prep": {
        "title": "Partner walks in with their own data · vendor scorecard · asks",
        "stages": [
            ("Pull partner data", "trigger", "Sourced · closed · engagement · commissions",
             [("introw-connect", "Introw Connect")]),
            ("Compute", "agent", "Performance + vendor-as-partner scorecard",
             [("introw-connect", "Introw Connect")]),
            ("Surface asks", "decision", "Tier · MDF · deal protection · field support",
             [("introw-connect", "Introw Connect")]),
            ("Drafted opening", "outcome", "Narrative + agenda + watch-outs",
             [("introw-connect", "Introw Connect")]),
        ],
    },
    # ========= UC13 — Commissions =========
    "partner-incentive-maximizer": {
        "title": "Transparency × prescription · highest-leverage actions ranked",
        "stages": [
            ("Pull context", "trigger", "Goals · commissions · pacing · open deals",
             [("introw-connect", "Introw Connect")]),
            ("Earnings impact", "agent", "Per plausible action · in € or %",
             [("introw-connect", "Introw Connect")]),
            ("Rank", "decision", "Impact × probability ÷ effort",
             [("introw-connect", "Introw Connect")]),
            ("Top 3 moves", "outcome", "Concrete actions · drafted asks · unblocks",
             [("introw-connect", "Introw Connect"), ("slack", "Slack")]),
        ],
    },
    # ========= UC14 — Ecosystem Performance =========
    "vendor-slack-weekly-channel-digest": {
        "title": "Weekly partner-team digest · auto-posted to #channel-team",
        "stages": [
            ("Pull data", "trigger", "Trailing 7 days across systems",
             [("introw", "Introw"), ("salesforce", "CRM"), ("finance", "Finance")]),
            ("Compose", "agent", "Wins · regs · at-risk · queue · KPI deltas · anomalies",
             [("introw", "Introw")]),
            ("Approve · auto-post", "decision", "First run preview · then auto-post",
             [("slack", "Slack")]),
            ("Posted", "outcome", "Channel-team Slack · message link logged",
             [("slack", "Slack")]),
        ],
    },
    "vendor-anomaly-detector": {
        "title": "Continuous scan · unusual behaviors flagged before quarterly surprise",
        "stages": [
            ("Network signals", "trigger", "Engagement · deals · goals · commissions",
             [("introw", "Introw"), ("salesforce", "Salesforce"), ("hubspot", "HubSpot")]),
            ("Compute deviations", "agent", "vs. trailing-90-day baseline · per partner",
             [("introw", "Introw")]),
            ("Cluster + filter", "decision", "Suppress noise · multi-signal first",
             [("introw", "Introw")]),
            ("Surface top anomalies", "outcome", "Recommended next skill per item",
             [("introw", "Introw"), ("slack", "Slack")]),
        ],
    },
}


def _tool_pill(tool_id, label):
    return f'<span class="tool-pill tool-pill--{tool_id}">{html_lib.escape(label)}</span>'


def _node_inner(ntype, title, tools):
    tools_html = "".join(_tool_pill(t, lbl) for t, lbl in tools)
    return (
        f'<div class="uc-visual-node uc-visual-node--{ntype}">'
        f'<div class="uc-visual-node-title">{html_lib.escape(title)}</div>'
        f'<div class="uc-visual-node-tools">{tools_html}</div>'
        f'</div>'
    )


def _stage_html(stage_tuple):
    # 4-tuple: (label, ntype, title, tools) — single node
    # 5-tuple: (label, ntype, title, tools, [(ntype, title, tools), ...]) — primary + extras
    if len(stage_tuple) == 5:
        label, ntype, title, tools, extras = stage_tuple
    else:
        label, ntype, title, tools = stage_tuple
        extras = []
    nodes = [_node_inner(ntype, title, tools)]
    for e_ntype, e_title, e_tools in extras:
        nodes.append(_node_inner(e_ntype, e_title, e_tools))
    return (
        f'<div class="uc-visual-stage">'
        f'<span class="uc-visual-stage-label">{html_lib.escape(label)}</span>'
        f'{"".join(nodes)}'
        f'</div>'
    )


def render_skill_visual(skill_name):
    """Render workflow visualization for a skill, or empty string if no spec."""
    spec = SKILL_VISUALS.get(skill_name)
    if not spec:
        return ""
    stages = spec["stages"]
    n = len(stages)
    parts = [
        '<aside class="uc-visual uc-visual--compact">',
        '<div class="uc-visual-header">',
        '<span class="uc-visual-eyebrow">Workflow</span>',
        f'<span class="uc-visual-title">{html_lib.escape(spec["title"])}</span>',
        '</div>',
        f'<div class="uc-visual-flow cols-{n}">',
    ]
    for i, stage_tuple in enumerate(stages):
        parts.append(_stage_html(stage_tuple))
        if i < n - 1:
            parts.append('<div class="uc-visual-arrow" aria-hidden="true">→</div>')
    parts.append('</div>')
    parts.append('</aside>')
    return "\n".join(parts)
