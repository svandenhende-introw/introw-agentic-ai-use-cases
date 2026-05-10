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

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_SRC = ROOT / ".claude" / "skills"
SKILLS_OUT = ROOT / "blog" / "skills"
LOGO_URL = "https://assets.introw.io/introw-logo-square.png"

# ---- Skill → use case mapping (mirrors the SKILL_MAP in earlier work) ----
SKILL_TO_UC = {
    "vendor-acquisition-abm-orchestrator":
        ("01-partner-acquisition", "01", "Partner Acquisition"),
    "vendor-personalized-onboarding-from-transcripts":
        ("03-onboarding", "03", "Onboarding"),
    "vendor-activate-network-with-personalized-campaigns":
        ("04-activation", "04", "Activation"),
    "vendor-microcourse-from-closed-lost":
        ("05-training", "05", "Training"),
    "vendor-content-radar":
        ("07-campaigns-and-announcements", "07", "Campaigns & Announcements"),
    "vendor-email-deal-registration-watcher":
        ("08-deal-registration", "08", "Deal Registration"),
    "vendor-pipeline-partner-influence-scout":
        ("08-deal-registration", "08", "Deal Registration"),
    "partner-pipeline-influence-companion":
        ("08-deal-registration", "08", "Deal Registration"),
    "vendor-deal-coach-from-similar-wins":
        ("11-deal-coaching", "11", "Deal Coaching"),
    "vendor-qbr-prep":
        ("12-qbrs-meeting-prep", "12", "QBRs / Meeting Prep"),
}

# Display order on the index page — group by use case in numeric order
INDEX_ORDER = [
    "vendor-acquisition-abm-orchestrator",
    "vendor-personalized-onboarding-from-transcripts",
    "vendor-activate-network-with-personalized-campaigns",
    "vendor-microcourse-from-closed-lost",
    "vendor-content-radar",
    "vendor-email-deal-registration-watcher",
    "vendor-pipeline-partner-influence-scout",
    "partner-pipeline-influence-companion",
    "vendor-deal-coach-from-similar-wins",
    "vendor-qbr-prep",
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
    uc = SKILL_TO_UC.get(name)
    uc_link = ""
    if uc:
        slug, num, uc_name = uc
        uc_link = f' · <a href="../{slug}.html" style="color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-tint);">Use case {num}: {html_lib.escape(uc_name)}</a>'

    description = fm.get("description", "")
    download_path = f"../../.claude/skills/{name}/SKILL.md"

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
      <span>{audience}{uc_link}</span>
    </div>
    <h1>{html_lib.escape(title)}</h1>
    <div class="skill-id">
      <span class="skill-id-label">Skill ID</span>
      <code>{html_lib.escape(name)}</code>
    </div>
    <p class="lead">{html_lib.escape(description)}</p>
  </div>
</section>

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
        <a class="skill-source-btn skill-source-download" href="{download_path}" download="{name}.md">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>Download SKILL.md</span>
        </a>
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
    var btns = document.querySelectorAll('.skill-source-copy');
    btns.forEach(function(btn) {{
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
            cards.append(f"""        <a class="skill-card" href="./{name}.html">
          <div class="skill-card-top">
            <span class="audience-badge {audience_class}">{audience}</span>
            <code class="skill-card-id">{html_lib.escape(name)}</code>
          </div>
          <h3 class="skill-card-title">{html_lib.escape(all_skills[name]["title"])}</h3>
          <p class="skill-card-desc">{html_lib.escape(short_desc)}</p>
          <span class="article-card-link">Open skill →</span>
        </a>
""")
        grid_class = "two" if len(cards) == 2 else "three" if len(cards) == 3 else ""
        sections.append(f"""    <section class="phase">
      <div class="phase-meta">
        <div class="phase-num">Use case {num}</div>
        <h2 class="phase-name">{html_lib.escape(uc_name)}</h2>
        <p class="phase-blurb"><a href="../{slug}.html" style="color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-tint);">Read the article →</a></p>
      </div>
      <div class="article-grid skill-grid {grid_class}">
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
    <div class="blog-hero-stats">
      <div class="blog-hero-stat"><strong>{total_skills}</strong> skills</div>
      <div class="blog-hero-stat"><strong>9</strong> use cases covered</div>
      <div class="blog-hero-stat"><strong>2</strong> audiences (vendor &amp; partner)</div>
    </div>
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
