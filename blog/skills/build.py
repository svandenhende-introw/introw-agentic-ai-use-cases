#!/usr/bin/env python3
"""
Generate the skill hosting pages from .claude/skills/<name>/SKILL.md.
Output:
  blog/skills/index.html       — landing page listing all skills
  blog/skills/<name>.html      — one per skill (rendered markdown)
"""
import re
import math
import html as html_lib
from pathlib import Path

import markdown

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals import render_skill_visual

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_SRC = ROOT / ".claude" / "skills"
SKILLS_OUT = ROOT / "blog" / "skills"
LOGO_URL = "https://assets.introw.io/introw-logo-square.png"

# ---- Personas served by each skill ----
# Standardized to industry-canonical role names. Top 10 channel/partnership roles
# in the market (vendor-side) — all covered across the skill set:
#   1. Partner Program Manager             (owns the partner program; aka Channel Chief / Head of Partner Programs)
#   2. VP Partnerships                     (strategic owner; sometimes ≡ Channel Chief)
#   3. Partner Development Manager (PDM)   (drives partner growth & activation)
#   4. Channel Account Manager (CAM)       (manages individual partner relationships)
#   5. Partner Marketing Manager           (partner-facing marketing)
#   6. Partner Enablement Manager          (training & certifications)
#   7. Channel Ops Manager                 (tooling, governance, processes)
#   8. Channel RevOps                      (analytics, attribution, forecasting)
#   9. Alliance Manager                    (strategic / ELG / co-sell partnerships)
#  10. Partner Recruiter                   (sources new partners; aka Partner Acquisition Mgr)
# Adjacent roles that touch the channel team: Account Executive (direct sales co-sell),
# Vendor Marketing (corp marketing producing partner-relevant content),
# Vendor IT (capability-matrix governance for the partner-support agent).
# Partner-side roles (top 5): Partner Seller, Partnerships Lead (manages vendor relationships
# at the partner org), Partner Operations, Customer Success Manager, Partner Finance.
PERSONA_MAP = {
    # Vendor
    "vendor-acquisition-abm-orchestrator":
        ["Partner Program Manager", "VP Partnerships", "Partner Recruiter"],
    "vendor-tier-promotion-batch-review":
        ["Partner Program Manager", "Channel RevOps", "Partner Development Manager"],
    "vendor-crossbeam-cosell-finder":
        ["Alliance Manager", "Channel RevOps", "Partner Development Manager"],
    "vendor-personalized-onboarding-from-transcripts":
        ["Channel Account Manager", "Partner Development Manager", "Channel Ops Manager"],
    "vendor-activate-network-with-personalized-campaigns":
        ["Partner Program Manager", "Partner Development Manager", "Channel RevOps"],
    "vendor-microcourse-from-closed-lost":
        ["Partner Enablement Manager", "Partner Program Manager", "Channel RevOps"],
    "vendor-support-content-gap-detector":
        ["Partner Enablement Manager", "Channel Ops Manager", "Vendor IT"],
    "vendor-content-radar":
        ["Partner Marketing Manager", "Vendor Marketing"],
    "vendor-email-deal-registration-watcher":
        ["Channel Ops Manager", "Channel RevOps", "Partner Development Manager"],
    "vendor-pipeline-partner-influence-scout":
        ["Partner Program Manager", "Channel RevOps", "Account Executive"],
    "vendor-deal-coach-from-similar-wins":
        ["Channel Account Manager", "Partner Development Manager"],
    "vendor-qbr-prep":
        ["Partner Development Manager", "Channel Account Manager", "Partner Program Manager"],
    "vendor-qbr-recording-to-portal-followup":
        ["Partner Development Manager", "Channel Account Manager", "Channel Ops Manager"],
    "vendor-slack-weekly-channel-digest":
        ["Partner Program Manager", "Channel Ops Manager", "Channel RevOps"],
    "vendor-anomaly-detector":
        ["Partner Program Manager", "Channel RevOps", "Partner Development Manager"],
    # Partner-side
    "partner-pipeline-influence-companion":
        ["Partner Seller", "Partnerships Lead"],
    "partner-cross-vendor-onboarding-tracker":
        ["Partnerships Lead", "Partner Operations", "Partner Seller"],
    "partner-onboarding-prioritizer":
        ["Partnerships Lead", "Partner Operations"],
    "partner-renewal-and-expansion-coordinator":
        ["Partnerships Lead", "Partner Seller", "Customer Success Manager"],
    "partner-cross-vendor-cert-tracker":
        ["Partner Enablement", "Partner Operations", "Partner Seller"],
    "partner-helpdesk":
        ["Partner Seller", "Partner Operations"],
    "partner-cross-vendor-content-calendar":
        ["Partner Marketing", "Partnerships Lead"],
    "partner-prospect-to-vendor-fit-finder":
        ["Partner Seller", "Partnerships Lead"],
    "partner-registration-status-tracker":
        ["Partner Operations", "Partnerships Lead"],
    "partner-deal-war-room":
        ["Partner Seller"],
    "partner-pre-qbr-self-prep":
        ["Partnerships Lead", "Partner Operations"],
    "partner-incentive-maximizer":
        ["Partner Seller", "Partner Finance"],
}

# ---- Skill → use case mapping (mirrors the SKILL_MAP in earlier work) ----
SKILL_TO_UC = {
    "vendor-acquisition-abm-orchestrator":
        ("01-partner-acquisition", "01", "Partner Acquisition"),
    "vendor-tier-promotion-batch-review":
        ("02-partner-segmentation", "02", "Partner Segmentation"),
    "vendor-crossbeam-cosell-finder":
        ("02-partner-segmentation", "02", "Partner Segmentation"),
    "vendor-personalized-onboarding-from-transcripts":
        ("03-onboarding", "03", "Onboarding"),
    "partner-cross-vendor-onboarding-tracker":
        ("03-onboarding", "03", "Onboarding"),
    "partner-onboarding-prioritizer":
        ("03-onboarding", "03", "Onboarding"),
    "vendor-activate-network-with-personalized-campaigns":
        ("04-activation", "04", "Activation"),
    "partner-renewal-and-expansion-coordinator":
        ("04-activation", "04", "Activation"),
    "vendor-microcourse-from-closed-lost":
        ("05-training", "05", "Training"),
    "partner-cross-vendor-cert-tracker":
        ("05-training", "05", "Training"),
    "vendor-support-content-gap-detector":
        ("06-enablement-support", "06", "Enablement Support"),
    "partner-helpdesk":
        ("06-enablement-support", "06", "Enablement Support"),
    "vendor-content-radar":
        ("07-campaigns-and-announcements", "07", "Campaigns & Announcements"),
    "partner-cross-vendor-content-calendar":
        ("07-campaigns-and-announcements", "07", "Campaigns & Announcements"),
    "vendor-email-deal-registration-watcher":
        ("08-deal-registration", "08", "Deal Registration"),
    "vendor-pipeline-partner-influence-scout":
        ("08-deal-registration", "08", "Deal Registration"),
    "partner-pipeline-influence-companion":
        ("08-deal-registration", "08", "Deal Registration"),
    "partner-prospect-to-vendor-fit-finder":
        ("08-deal-registration", "08", "Deal Registration"),
    "partner-registration-status-tracker":
        ("08-deal-registration", "08", "Deal Registration"),
    "vendor-deal-coach-from-similar-wins":
        ("11-deal-coaching", "11", "Deal Coaching"),
    "partner-deal-war-room":
        ("11-deal-coaching", "11", "Deal Coaching"),
    "vendor-qbr-prep":
        ("12-qbrs-meeting-prep", "12", "QBRs / Meeting Prep"),
    "vendor-qbr-recording-to-portal-followup":
        ("12-qbrs-meeting-prep", "12", "QBRs / Meeting Prep"),
    "partner-pre-qbr-self-prep":
        ("12-qbrs-meeting-prep", "12", "QBRs / Meeting Prep"),
    "partner-incentive-maximizer":
        ("13-commissions-and-incentives", "13", "Commissions & Incentives"),
    "vendor-slack-weekly-channel-digest":
        ("14-ecosystem-performance", "14", "Ecosystem Performance"),
    "vendor-anomaly-detector":
        ("14-ecosystem-performance", "14", "Ecosystem Performance"),
}

# Display order on the index page — group by use case in numeric order
INDEX_ORDER = [
    "vendor-acquisition-abm-orchestrator",
    "vendor-tier-promotion-batch-review",
    "vendor-crossbeam-cosell-finder",
    "vendor-personalized-onboarding-from-transcripts",
    "partner-cross-vendor-onboarding-tracker",
    "partner-onboarding-prioritizer",
    "vendor-activate-network-with-personalized-campaigns",
    "partner-renewal-and-expansion-coordinator",
    "vendor-microcourse-from-closed-lost",
    "partner-cross-vendor-cert-tracker",
    "vendor-support-content-gap-detector",
    "partner-helpdesk",
    "vendor-content-radar",
    "partner-cross-vendor-content-calendar",
    "vendor-email-deal-registration-watcher",
    "vendor-pipeline-partner-influence-scout",
    "partner-pipeline-influence-companion",
    "partner-prospect-to-vendor-fit-finder",
    "partner-registration-status-tracker",
    "vendor-deal-coach-from-similar-wins",
    "partner-deal-war-room",
    "vendor-qbr-prep",
    "vendor-qbr-recording-to-portal-followup",
    "partner-pre-qbr-self-prep",
    "partner-incentive-maximizer",
    "vendor-slack-weekly-channel-digest",
    "vendor-anomaly-detector",
]


def parse_skill(path: Path):
    raw = path.read_text()
    fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', raw)
    if not fm_match:
        raise ValueError(f"No frontmatter in {path}")
    fm_text = fm_match.group(1)
    body = raw[fm_match.end():]

    fm = {}
    # very small YAML parser (only handles key: value, multi-line values join)
    for line in fm_text.splitlines():
        m = re.match(r'^(\w+):\s*(.+)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    # Extract first H1 from body for friendly title (skip leading whitespace after frontmatter)
    body_stripped = body.lstrip()
    h1 = re.match(r'^# (.+)$', body_stripped, re.MULTILINE)
    title = h1.group(1).strip() if h1 else fm.get("name", "Skill")
    # Strip trailing "(Vendor)" / "(Partner)" suffix — audience is shown via the pill, not in the title
    title = re.sub(r'\s*\((?:Vendor|Partner)\)\s*$', '', title).strip()
    return fm, title, body


def render_md(md_text):
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists", "fenced_code"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    body_html = md.convert(md_text)
    toc = []
    for tok in md.toc_tokens:
        toc.append(("h2", tok["id"], tok["name"]))
        for child in tok.get("children", []):
            toc.append(("h3", child["id"], child["name"]))
    return body_html, toc


def reading_time(text):
    return max(1, math.ceil(len(re.findall(r"\w+", text)) / 230))


HEADER_HTML = f"""<header class="site-header">
  <div class="header-inner">
    <a href="../../index.html" class="brand">
      <img class="brand-logo" src="{LOGO_URL}" alt="Introw" loading="eager">
      Introw <span class="brand-suffix">/ skills</span>
    </a>
    <nav class="primary-nav">
      <a href="../index.html">All articles</a>
      <a href="./index.html">All skills</a>
      <a href="../../index.html#integrations">Integrations</a>
    </nav>
    <a href="../../index.html" class="header-cta">
      Back to Introw
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
    </a>
  </div>
</header>
"""

FOOTER_HTML = """<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-top">
      <div>
        <div class="footer-brand">Introw</div>
        <div class="footer-tagline">Headless PRM, connected to your CRM. Beyond the portal — into the tools your team and partners already use.</div>
      </div>
      <div class="footer-links">
        <a href="../index.html">All articles</a>
        <a href="./index.html">All skills</a>
        <a href="../../index.html#use-cases">Use cases</a>
        <a href="../../index.html#integrations">Integrations</a>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© Introw — Agentic PRM</div>
      <div>Built for partner teams who'd rather build than configure portals.</div>
    </div>
  </div>
</footer>
"""


def toc_html(toc):
    if not toc:
        return ""
    items = []
    for level, anchor, text in toc:
        cls = "h2" if level == "h2" else "h3"
        items.append(f'<li class="{cls}"><a href="#{anchor}">{html_lib.escape(text)}</a></li>')
    return f"""    <aside class="article-toc" aria-label="Table of contents">
      <div class="article-toc-label">On this page</div>
      <ul>
{chr(10).join(items)}
      </ul>
    </aside>
"""


def build_skill_page(skill_dir: Path):
    name = skill_dir.name
    md_path = skill_dir / "SKILL.md"
    if not md_path.exists():
        return None

    fm, title, _ = parse_skill(md_path)
    raw_md = md_path.read_text()                     # full file incl. frontmatter
    md_escaped = html_lib.escape(raw_md)
    line_count = raw_md.count("\n") + 1
    word_count = len(re.findall(r"\w+", raw_md))

    audience = "Partner" if name.startswith("partner-") else "Vendor"
    audience_class = "audience-partner" if audience == "Partner" else "audience-vendor"
    uc = SKILL_TO_UC.get(name)
    uc_link = ""
    if uc:
        slug, num, uc_name = uc
        uc_link = f' <span class="dot"></span> <a href="../{slug}.html" style="color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-tint);">Use case {num}: {html_lib.escape(uc_name)}</a>'

    description = fm.get("description", "")

    personas = PERSONA_MAP.get(name, [])
    persona_html = ""
    if personas:
        pills = "".join(
            f'<span class="persona-badge">{html_lib.escape(p)}</span>'
            for p in personas
        )
        persona_html = (
            '    <div class="persona-row">\n'
            '      <span class="persona-row-label">Built for</span>\n'
            f'      <div class="persona-badges">{pills}</div>\n'
            '    </div>\n'
        )

    visual_html = render_skill_visual(name)
    visual_section = (
        f'<section class="skill-visual-wrap">\n'
        f'  <div class="skill-visual-inner">\n{visual_html}\n  </div>\n'
        f'</section>'
    ) if visual_html else ""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(title)} — Introw Skill</title>
<meta name="description" content="{html_lib.escape(description[:280])}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:opsz,wght,SOFT,WONK@9..144,300..900,0..100,0..1&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="../assets/blog.css">
</head>
<body>

{HEADER_HTML}

<section class="article-hero">
  <div class="article-hero-bg"></div>
  <div class="article-hero-inner">
    <a href="./index.html" class="breadcrumb">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
      All skills
    </a>
    <div class="article-hero-eyebrow">
      <span class="uc-num">Claude Code skill</span>
      <span class="dot"></span>
      <span class="audience-badge {audience_class}">{audience}</span>{uc_link}
    </div>
    <h1>{html_lib.escape(title)}</h1>
    <div class="skill-id">
      <span class="skill-id-label">Skill ID</span>
      <code>{html_lib.escape(name)}</code>
    </div>
    <p class="lead">{html_lib.escape(description)}</p>
{persona_html}  </div>
</section>

{visual_section}

<main class="skill-source-wrap">
  <div class="skill-source-card">
    <div class="skill-source-header">
      <div class="skill-source-filename">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <code>SKILL.md</code>
        <span class="skill-source-stats">{line_count} lines · {word_count} words</span>
      </div>
      <div class="skill-source-actions">
        <button type="button" class="skill-source-btn skill-source-copy" data-target="skill-md-{name}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span>Copy</span>
        </button>
        <button type="button" class="skill-source-btn skill-source-download" data-target="skill-md-{name}" data-filename="{name}.md">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>Download SKILL.md</span>
        </button>
      </div>
    </div>
    <pre class="skill-source-pre"><code id="skill-md-{name}">{md_escaped}</code></pre>
  </div>
  <p class="skill-install-hint">
    Drop this file into <code>.claude/skills/{name}/SKILL.md</code> in your repo. Claude Code triggers the skill on the prompts described in the <code>description</code> field.
  </p>
</main>

<script>
  (function() {{
    // Copy button — copies the embedded markdown to clipboard
    document.querySelectorAll('.skill-source-copy').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        var target = document.getElementById(btn.dataset.target);
        if (!target) return;
        var text = target.innerText;
        navigator.clipboard.writeText(text).then(function() {{
          var label = btn.querySelector('span');
          var prev = label.textContent;
          label.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(function() {{
            label.textContent = prev;
            btn.classList.remove('copied');
          }}, 1600);
        }});
      }});
    }});

    // Download button — generates a Blob from the embedded markdown and triggers download.
    // This avoids serving the file from the .claude/ path, which many static hosts block.
    document.querySelectorAll('.skill-source-download').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        var target = document.getElementById(btn.dataset.target);
        if (!target) return;
        var text = target.innerText;
        var filename = btn.dataset.filename || 'SKILL.md';
        var blob = new Blob([text], {{ type: 'text/markdown;charset=utf-8' }});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function() {{ URL.revokeObjectURL(url); }}, 0);
      }});
    }});
  }})();
</script>

{FOOTER_HTML}

</body>
</html>
"""
    out = SKILLS_OUT / f"{name}.html"
    out.write_text(page)
    return out


def build_index(all_skills):
    """Build skills landing page grouped by use case."""
    # Group by UC
    groups = {}
    for name in INDEX_ORDER:
        if name not in all_skills:
            continue
        uc = SKILL_TO_UC.get(name)
        if uc is None:
            continue
        slug, num, uc_name = uc
        groups.setdefault((num, slug, uc_name), []).append(name)

    sections = []
    for (num, slug, uc_name), skills in sorted(groups.items()):
        cards = []
        for name in skills:
            fm = all_skills[name]["fm"]
            audience = "Partner" if name.startswith("partner-") else "Vendor"
            description = fm.get("description", "")
            # Truncate description to fit card
            short_desc = description if len(description) <= 260 else description[:257] + "…"
            audience_class = "audience-partner" if audience == "Partner" else "audience-vendor"
            personas = PERSONA_MAP.get(name, [])
            persona_pills = "".join(
                f'<span class="persona-badge">{html_lib.escape(p)}</span>'
                for p in personas
            )
            persona_block = (
                f'\n          <div class="persona-badges">{persona_pills}</div>'
                if persona_pills else ""
            )
            cards.append(f"""        <a class="skill-card" href="./{name}.html">
          <div class="skill-card-top">
            <span class="audience-badge {audience_class}">{audience}</span>
            <code class="skill-card-id">{html_lib.escape(name)}</code>
          </div>
          <h3 class="skill-card-title">{html_lib.escape(all_skills[name]["title"])}</h3>
          <p class="skill-card-desc">{html_lib.escape(short_desc)}</p>{persona_block}
          <span class="article-card-link">Open skill →</span>
        </a>
""")
        # Always 2-up on the skill index — odd last card spans full width via CSS.
        sections.append(f"""    <section class="phase">
      <div class="phase-meta">
        <div class="phase-num">Use case {num}</div>
        <h2 class="phase-name">{html_lib.escape(uc_name)}</h2>
        <p class="phase-blurb"><a href="../{slug}.html" style="color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-tint);">Read the article →</a></p>
      </div>
      <div class="article-grid skill-grid">
{''.join(cards)}      </div>
    </section>
""")

    total_skills = len(all_skills)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Claude Code Skills — Introw</title>
<meta name="description" content="Drop-in skills for Claude Code that run partner-program workflows: acquisition, onboarding, activation, deal coaching, QBR prep, and more.">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:opsz,wght,SOFT,WONK@9..144,300..900,0..100,0..1&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="../assets/blog.css">
</head>
<body>

{HEADER_HTML}

<section class="blog-hero">
  <div class="blog-hero-bg"></div>
  <div class="blog-hero-grain"></div>
  <div class="blog-hero-inner">
    <div class="blog-eyebrow">
      <span class="blog-eyebrow-tag" style="background: var(--warn);">Skills</span>
      Claude Code skills for partner programs
    </div>
    <h1>Drop-in <em>workflows</em> that run inside Claude Code.</h1>
    <p class="lead">Each skill is a <code>SKILL.md</code> file with structured trigger phrases, MCP tool calls, and PRM guardrails. Drop into <code>.claude/skills/&lt;name&gt;/</code> in your repo and Claude Code triggers the right one when the prompt matches.</p>
  </div>
</section>

<main class="phases-wrap">
{''.join(sections)}
</main>

{FOOTER_HTML}

</body>
</html>
"""
    out = SKILLS_OUT / "index.html"
    out.write_text(page)
    return out


def main():
    SKILLS_OUT.mkdir(parents=True, exist_ok=True)
    all_skills = {}
    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if not skill_dir.is_dir():
            continue
        md_path = skill_dir / "SKILL.md"
        if not md_path.exists():
            continue
        fm, title, body = parse_skill(md_path)
        all_skills[skill_dir.name] = {"fm": fm, "title": title, "body": body}
        out = build_skill_page(skill_dir)
        if out:
            print(f"Skill: {out.relative_to(ROOT)}")

    landing = build_index(all_skills)
    print(f"Index: {landing.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
