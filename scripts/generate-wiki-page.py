#!/usr/bin/env python3
"""
generate-wiki-page.py — Wiki page generator for The Human OS Wiki.

Takes a JSON content file, outputs a self-contained HTML page that matches
the locked human-os-wiki-v1 template (validated against Page 1 Fawn Response
and Page 2 Cyclic Sighing).

Usage:
    python3 generate-wiki-page.py <content.json> <output.html>

Schema for content JSON: see SCHEMA below.

This runs at AUTHORING time, not at request time. The output is vanilla HTML
that Cloudflare Pages serves statically. CLAUDE.md "no build step" rule is
about deploy-time, not authoring tools.
"""
import json
import sys
from pathlib import Path

SCHEMA = """
{
  "slug": "diving-reflex",
  "page_num": "03",
  "title": "Diving Reflex Protocol",
  "title_grad_word": "REFLEX",
  "title_pre_words": "DIVING",
  "pillar": "UNDERSTANDING YOURSELF",
  "thesis": "...",
  "reading_time": "7 min read",
  "last_updated": "May 2026",
  "source_chapter": "Self-Care, Ch. 3",
  "meta_description": "...",
  "og_description": "...",
  "twitter_description": "...",
  "schema_keywords": "comma, separated",
  "date_published": "2026-05-01",
  "pull_quote": {"text": "...", "cite": "..."},
  "sections": [
    {"type": "h2", "title": "The problem", "no_rule": true},
    {"type": "p", "text": "..."},
    {"type": "ul", "items": ["...", "..."]},
    {"type": "h2", "title": "The mechanism"},
    {"type": "stat_box", "label": "...", "figure": "...", "cite": "..."},
    {"type": "p_bold_lead", "lead": "Top-off inhale.", "rest": "..."},
    {"type": "h2", "title": "The protocol"},
    {"type": "p", "text": "..."}
  ],
  "steps": [
    {"name": "Settle", "body": "...", "tip": "..."},
    ...
  ],
  "after_steps_h2": "The printable: a wallet card",
  "after_steps_p": "Print this. Fold it once. ...",
  "printable_card": {
    "title": "CYCLIC SIGHING · 5 MINUTES",
    "subtitle": "Stanford 2023 — Balban et al.",
    "items": [
      {"num": "01 · SETTLE", "text": "...", "help": "..."},
      ...
    ]
  },
  "exits": [
    {"tag": "Full chapter · $27", "tag_class": "", "url": "https://thehumanfrequency.gumroad.com/l/lwawbf",
     "title": "The Self-Care You Were Never Taught", "body": "...", "cta": "Read the book →"}
  ],
  "subscribe_form_name": "wiki-diving-reflex-newsletter",
  "subscribe_source": "source-wiki-diving-reflex",
  "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapter 3. Primary sources:",
  "sources_list": ["Author (year). Title. Journal."],
  "sources_outro": ""
}
"""

def html_escape(s):
    """Minimal HTML escape — assumes input is plain text. Allows specific tags via raw HTML in inputs."""
    # Inputs may contain inline <em>, <strong> deliberately — don't escape those.
    return s

def render_section(sec):
    t = sec["type"]
    if t == "h2":
        cls = ' class="no-rule"' if sec.get("no_rule") else ""
        return f'  <h2{cls}>{sec["title"]}</h2>'
    if t == "p":
        return f'  <p>{sec["text"]}</p>'
    if t == "p_bold_lead":
        return f'  <p><strong>{sec["lead"]}</strong> {sec["rest"]}</p>'
    if t == "ul":
        items = "\n".join(f"    <li>{i}</li>" for i in sec["items"])
        return f"  <ul>\n{items}\n  </ul>"
    if t == "stat_box":
        return (
            f'  <div class="stat-box reveal">\n'
            f'    <div class="stat-label">{sec["label"]}</div>\n'
            f'    <div class="stat-figure">{sec["figure"]}</div>\n'
            f'    <div class="stat-cite">{sec["cite"]}</div>\n'
            f'  </div>'
        )
    if t == "blockquote":
        return f'  <blockquote class="inline-quote">{sec["text"]}<cite>{sec.get("cite", "")}</cite></blockquote>'
    raise ValueError(f"Unknown section type: {t}")

def render_step(step, idx):
    num = f"STEP {idx+1:02d}"
    tip_html = f'\n      <div class="step-tip">{step["tip"]}</div>' if step.get("tip") else ""
    return (
        f'    <div class="step reveal">\n'
        f'      <div class="step-num">{num}</div>\n'
        f'      <h3>{step["name"]}</h3>\n'
        f'      <p>{step["body"]}</p>{tip_html}\n'
        f'    </div>'
    )

def render_printable_item(item):
    return (
        f'    <div class="pc-q">\n'
        f'      <div class="pc-q-num">{item["num"]}</div>\n'
        f'      <div class="pc-q-text">{item["text"]}</div>\n'
        f'      <div class="pc-q-help">{item["help"]}</div>\n'
        f'    </div>'
    )

def render_exit(exit_data):
    cls = exit_data.get("tag_class", "")
    rel_attr = ' rel="noopener"' if exit_data["url"].startswith("http") else ""
    tag_class = (" " + cls) if cls else ""
    url = exit_data["url"]
    tag = exit_data["tag"]
    title = exit_data["title"]
    body = exit_data["body"]
    cta = exit_data["cta"]
    return (
        f'    <a class="exit-card reveal" href="{url}"{rel_attr}>\n'
        f'      <span class="exit-tag{tag_class}">{tag}</span>\n'
        f'      <h4>{title}</h4>\n'
        f'      <p>{body}</p>\n'
        f'      <span class="exit-arrow">{cta}</span>\n'
        f'    </a>'
    )

CSS_BLOCK = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy: #0a0e1a; --navy2: #0d1426; --navy3: #111827;
  --orange: #ff4500; --orange2: #ff6b35; --gold: #c9a84c; --magenta: #e91e8c;
  --cream: #f5f0e8; --text: #e8e8e8; --muted: #8892a4; --border: rgba(255,255,255,0.08);
}
html { scroll-behavior: smooth; }
body { background: var(--navy); color: var(--text); font-family: 'DM Sans', sans-serif; overflow-x: hidden; line-height: 1.7; }

.reveal { opacity: 0; transform: translateY(28px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal.visible { opacity: 1; transform: translateY(0); }

.announce-bar { background: linear-gradient(90deg, var(--orange), var(--magenta)); text-align: center; padding: 10px 24px; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.12em; color: white; }
.announce-bar a { color: white; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.4); }

nav { display: flex; align-items: center; justify-content: space-between; padding: 14px 40px; background: var(--navy); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--border); }
.nav-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; }
.nav-logo-icon { width: 46px; height: 46px; border-radius: 50%; flex-shrink: 0; background: linear-gradient(135deg, #0d1426, #1a0e20); border: 1.5px solid rgba(255,69,0,0.5); display: flex; align-items: center; justify-content: center; }
.nav-logo-icon svg { width: 26px; height: 26px; }
.nav-logo-text .brand { font-family: 'Bebas Neue', sans-serif; font-size: 1.05rem; letter-spacing: 0.08em; color: white; line-height: 1; }
.nav-logo-text .brand span { color: var(--orange); }
.nav-logo-text .tagline { font-size: 0.58rem; letter-spacing: 0.2em; color: var(--muted); text-transform: uppercase; }
.nav-links { display: flex; align-items: center; gap: 32px; list-style: none; }
.nav-links a { color: var(--text); text-decoration: none; font-size: 0.78rem; letter-spacing: 0.12em; font-weight: 500; transition: color 0.2s; }
.nav-links a:hover { color: var(--orange); }
.btn-nav { background: linear-gradient(135deg, var(--orange), var(--magenta)); color: white !important; padding: 10px 22px; border-radius: 50px; font-weight: 600 !important; }

.crumb { max-width: 760px; margin: 32px auto 0; padding: 0 24px; font-size: 0.72rem; letter-spacing: 0.18em; color: var(--muted); text-transform: uppercase; }
.crumb a { color: var(--muted); text-decoration: none; transition: color 0.2s; }
.crumb a:hover { color: var(--orange); }
.crumb .sep { margin: 0 10px; color: rgba(255,255,255,0.2); }

.hero { max-width: 760px; margin: 0 auto; padding: 48px 24px 40px; text-align: left; }
.hero-eyebrow { font-size: 0.7rem; letter-spacing: 0.25em; color: var(--orange); font-weight: 700; margin-bottom: 22px; text-transform: uppercase; display: inline-flex; align-items: center; gap: 12px; }
.hero-eyebrow::before { content: ''; width: 28px; height: 1px; background: var(--orange); opacity: 0.6; }
.hero h1 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(56px, 9vw, 104px); line-height: 0.94; letter-spacing: 0.01em; color: white; margin-bottom: 22px; }
.hero h1 .grad { background: linear-gradient(135deg, #ff4500, #ff6b35, #e91e8c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-thesis { font-family: 'Playfair Display', serif; font-style: italic; font-size: clamp(1.15rem, 2.1vw, 1.45rem); color: var(--text); line-height: 1.55; max-width: 660px; margin-bottom: 22px; }
.hero-meta { display: flex; gap: 22px; align-items: center; flex-wrap: wrap; font-size: 0.74rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); }
.hero-meta span::before { content: '·'; margin-right: 22px; color: rgba(255,255,255,0.2); }
.hero-meta span:first-child::before { content: ''; margin: 0; }

.pullquote { max-width: 760px; margin: 0 auto; padding: 0 24px 56px; }
.pullquote-inner { font-family: 'Playfair Display', serif; font-style: italic; font-size: clamp(1.15rem, 2vw, 1.4rem); color: var(--orange); border-left: 3px solid var(--orange); padding: 8px 0 8px 28px; line-height: 1.55; }
.pullquote-cite { display: block; margin-top: 14px; font-family: 'DM Sans', sans-serif; font-style: normal; font-size: 0.78rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); }

.reading { max-width: 760px; margin: 0 auto; padding: 24px 24px 80px; }
.reading h2 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(34px, 4.5vw, 52px); letter-spacing: 0.02em; color: white; line-height: 1.05; margin: 64px 0 24px; padding-top: 12px; border-top: 1px solid var(--border); }
.reading h2.no-rule { border: none; padding-top: 0; }
.reading h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.06em; font-size: 1.45rem; color: white; margin: 36px 0 14px; }
.reading p { font-size: 1.04rem; line-height: 1.85; margin-bottom: 22px; color: var(--text); }
.reading p strong { color: white; font-weight: 600; }
.reading ul { margin: 0 0 26px 0; padding-left: 22px; }
.reading ul li { font-size: 1.02rem; line-height: 1.75; margin-bottom: 10px; color: var(--text); }

.stat-box { background: var(--navy3); border: 1px solid rgba(255,69,0,0.3); border-radius: 14px; padding: 26px 28px; margin: 28px 0; }
.stat-box .stat-label { font-family: 'Bebas Neue', sans-serif; font-size: 0.86rem; letter-spacing: 0.16em; color: var(--orange); margin-bottom: 8px; }
.stat-box .stat-figure { font-family: 'Bebas Neue', sans-serif; font-size: clamp(28px, 3.8vw, 38px); color: white; line-height: 1.15; margin-bottom: 8px; }
.stat-box .stat-cite { font-size: 0.84rem; color: var(--muted); line-height: 1.55; }

.steps { display: flex; flex-direction: column; gap: 16px; margin: 28px 0 8px; }
.step { background: var(--navy3); border: 1px solid var(--border); border-radius: 14px; padding: 26px 28px; transition: border-color 0.25s; }
.step:hover { border-color: rgba(255,69,0,0.3); }
.step-num { font-family: 'Bebas Neue', sans-serif; font-size: 0.86rem; letter-spacing: 0.16em; color: var(--orange); margin-bottom: 8px; }
.step h3 { margin: 0 0 12px; font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 0.04em; color: white; }
.step p { font-size: 0.98rem; line-height: 1.75; color: var(--text); margin-bottom: 0; }
.step p + p { margin-top: 10px; }
.step .step-tip { font-size: 0.88rem; color: var(--muted); font-style: italic; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }

.printable { max-width: 760px; margin: 24px auto 0; padding: 0 24px; }
.printable-card { background: var(--cream); color: #1a1a1a; border-radius: 18px; padding: 44px 40px; position: relative; overflow: hidden; }
.printable-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--orange), var(--magenta)); }
.printable-card .pc-title { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.18em; font-size: 1.05rem; color: #1a1a1a; text-align: center; margin-bottom: 6px; }
.printable-card .pc-sub { font-size: 0.78rem; letter-spacing: 0.08em; color: #555; text-align: center; margin-bottom: 28px; font-family: 'DM Sans', sans-serif; }
.printable-card .pc-rule { border: none; border-top: 1.5px solid #1a1a1a; margin: 0 0 24px; opacity: 0.4; }
.printable-card .pc-q { margin-bottom: 22px; }
.printable-card .pc-q-num { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.14em; color: var(--orange); font-size: 0.92rem; margin-bottom: 4px; }
.printable-card .pc-q-text { font-family: 'DM Sans', sans-serif; font-weight: 600; color: #1a1a1a; font-size: 1rem; margin-bottom: 4px; line-height: 1.4; }
.printable-card .pc-q-help { font-family: 'DM Sans', sans-serif; font-style: italic; color: #555; font-size: 0.88rem; line-height: 1.5; }
.printable-card .pc-foot { text-align: center; margin-top: 18px; font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.16em; font-size: 0.78rem; color: #555; }

.exits { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 30px; }
.exit-card { background: var(--navy3); border: 1px solid var(--border); border-radius: 14px; padding: 26px 24px; text-decoration: none; color: inherit; display: flex; flex-direction: column; transition: border-color 0.25s, transform 0.25s; }
.exit-card:hover { border-color: rgba(255,69,0,0.4); transform: translateY(-3px); }
.exit-tag { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.18em; padding: 3px 10px; border-radius: 50px; align-self: flex-start; margin-bottom: 12px; text-transform: uppercase; background: rgba(255,69,0,0.12); color: var(--orange); border: 1px solid rgba(255,69,0,0.25); }
.exit-tag.free { background: rgba(201,168,76,0.12); color: var(--gold); border-color: rgba(201,168,76,0.25); }
.exit-tag.community { background: rgba(233,30,140,0.12); color: var(--magenta); border-color: rgba(233,30,140,0.25); }
.exit-card h4 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.04em; font-size: 1.18rem; color: white; margin-bottom: 8px; line-height: 1.2; }
.exit-card p { font-size: 0.86rem; color: var(--muted); line-height: 1.6; margin-bottom: 12px; flex-grow: 1; }
.exit-card .exit-arrow { font-size: 0.78rem; color: var(--orange); font-weight: 600; }

.newsletter { background: var(--navy2); padding: 80px 24px; margin-top: 64px; }
.newsletter-card { max-width: 700px; margin: 0 auto; background: linear-gradient(135deg, #111827, #0d1426); border: 1px solid var(--border); border-radius: 24px; padding: 56px 48px; text-align: center; position: relative; overflow: hidden; }
.newsletter-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--orange), var(--magenta)); }
.nl-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; color: var(--orange); font-weight: 600; text-transform: uppercase; margin-bottom: 16px; }
.nl-title { font-family: 'Bebas Neue', sans-serif; font-size: clamp(34px, 4.5vw, 48px); color: white; margin-bottom: 10px; line-height: 1.05; }
.nl-sub { font-family: 'Playfair Display', serif; font-style: italic; color: var(--muted); margin-bottom: 28px; font-size: 1rem; line-height: 1.55; }
.nl-form { display: flex; gap: 10px; max-width: 460px; margin: 0 auto 16px; }
.nl-form input { flex: 1; background: var(--navy3); border: 1px solid var(--border); border-radius: 50px; padding: 14px 20px; color: var(--text); font-size: 0.88rem; font-family: 'DM Sans', sans-serif; outline: none; }
.nl-form input:focus { border-color: rgba(255,69,0,0.4); }
.btn-primary { background: linear-gradient(135deg, var(--orange), var(--magenta)); color: white; padding: 14px 28px; border-radius: 50px; font-weight: 700; font-size: 0.88rem; border: none; cursor: pointer; white-space: nowrap; transition: opacity 0.2s; font-family: 'DM Sans', sans-serif; }
.btn-primary:hover { opacity: 0.9; }
.nl-note { font-size: 0.72rem; color: var(--muted); }

.sources { max-width: 760px; margin: 0 auto; padding: 56px 24px 40px; }
.sources-toggle { width: 100%; background: transparent; border: 1px solid var(--border); border-radius: 12px; padding: 16px 22px; color: var(--text); font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.14em; font-size: 0.92rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: border-color 0.2s; list-style: none; }
.sources-toggle::-webkit-details-marker { display: none; }
.sources-toggle:hover { border-color: rgba(255,69,0,0.4); }
.sources-toggle .arrow { transition: transform 0.25s; color: var(--orange); }
.sources[open] .sources-toggle .arrow { transform: rotate(180deg); }
.sources-body { padding: 22px 4px 6px; font-size: 0.86rem; line-height: 1.75; color: var(--muted); }
.sources-body ul { margin-top: 12px; padding-left: 22px; }
.sources-body li { margin-bottom: 6px; }

footer { background: var(--navy2); border-top: 1px solid var(--border); padding: 60px 40px 32px; }
.footer-grid { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; margin-bottom: 48px; }
.footer-brand-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.25rem; letter-spacing: 0.08em; color: white; margin-bottom: 4px; }
.footer-brand-name span { color: var(--orange); }
.footer-tagline { font-size: 0.58rem; letter-spacing: 0.2em; color: var(--orange); font-weight: 600; text-transform: uppercase; margin-bottom: 14px; }
.footer-desc { font-size: 0.83rem; color: var(--muted); line-height: 1.65; margin-bottom: 20px; }
.footer-socials { display: flex; gap: 10px; flex-wrap: wrap; }
.social-btn { width: 36px; height: 36px; background: var(--navy3); border: 1px solid var(--border); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--muted); text-decoration: none; font-size: 0.85rem; transition: border-color 0.2s, color 0.2s; }
.social-btn:hover { border-color: var(--orange); color: var(--orange); }
.footer-col h4 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 0.12em; font-size: 0.88rem; color: white; margin-bottom: 16px; }
.footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.footer-col ul li a { color: var(--muted); text-decoration: none; font-size: 0.83rem; transition: color 0.2s; }
.footer-col ul li a:hover { color: var(--orange); }
.footer-bottom { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid var(--border); padding-top: 24px; font-size: 0.73rem; color: var(--muted); }

@media (max-width: 900px) { .exits { grid-template-columns: 1fr; gap: 14px; } }
@media (max-width: 768px) {
  nav { padding: 12px 18px; }
  .nav-logo-icon { width: 38px; height: 38px; }
  .nav-logo-icon svg { width: 20px; height: 20px; }
  .nav-logo-text .tagline { display: none; }
  .nav-links { gap: 14px; }
  .nav-links li:nth-child(1), .nav-links li:nth-child(2), .nav-links li:nth-child(3) { display: none; }
  .btn-nav { padding: 8px 14px; font-size: 0.68rem !important; }
  .announce-bar { font-size: 0.68rem; letter-spacing: 0.06em; padding: 8px 16px; }
  .hero { padding: 32px 20px 28px; }
  .crumb { padding: 0 20px; margin-top: 22px; }
  .pullquote { padding: 0 20px 40px; }
  .reading { padding: 16px 20px 56px; }
  .printable { padding: 0 16px; }
  .printable-card { padding: 32px 22px; }
  .newsletter { padding: 56px 20px; }
  .newsletter-card { padding: 36px 24px; }
  .nl-form { flex-direction: column; gap: 12px; }
  .nl-form input { border-radius: 12px; }
  .nl-form .btn-primary { border-radius: 12px; width: 100%; }
  .sources { padding: 40px 20px 24px; }
  footer { padding: 48px 20px 24px; }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
  .footer-bottom { flex-direction: column; gap: 8px; text-align: center; }
}
@media (max-width: 480px) { .footer-grid { grid-template-columns: 1fr; gap: 28px; } }
""".strip()

NAV_BLOCK = """
<div class="announce-bar">
  🎙 A LIVE CALL-IN SHOW IS COMING — <a href='/thf-podcast'>JOIN THE WAITLIST →</a>
</div>

<nav>
  <a class='nav-logo' href='/'>
    <div class="nav-logo-icon">
      <svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M2 13 Q5 7, 8 13 Q11 19, 13 13 Q15 7, 18 13 Q21 19, 24 13" stroke="url(#lg)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <defs><linearGradient id="lg" x1="2" y1="13" x2="24" y2="13" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#ff4500"/><stop offset="100%" stop-color="#e91e8c"/></linearGradient></defs>
      </svg>
    </div>
    <div class="nav-logo-text">
      <span class="brand">THE HUMAN <span>FREQUENCY</span></span>
      <span class="tagline">Find Common Ground</span>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href='/#mission'>MISSION</a></li>
    <li><a href='/thf-podcast'>THE SHOW</a></li>
    <li><a href='/thf-store'>THE STORE</a></li>
    <li><a href='/about'>ABOUT</a></li>
    <li><a href="/#newsletter" class="btn-nav">TUNE IN</a></li>
  </ul>
</nav>
""".strip()

FOOTER_BLOCK = """
<footer>
  <div class="footer-grid">
    <div>
      <div class="footer-brand-name">THE HUMAN <span>FREQUENCY</span></div>
      <div class="footer-tagline">FIND COMMON GROUND</div>
      <p class="footer-desc">A behavioral science brand publishing operating systems for being human. Evidence-based guides, AI tools, and a live show.</p>
      <div class="footer-socials">
        <a class="social-btn" href="https://www.instagram.com/thehumanfrequency" rel="noopener">IG</a>
        <a class="social-btn" href="https://www.youtube.com/@TheHumanFrequency" rel="noopener">YT</a>
        <a class="social-btn" href="https://www.tiktok.com/@thehumanfrequency" rel="noopener">TT</a>
      </div>
    </div>
    <div class="footer-col">
      <h4>EXPLORE</h4>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/thf-store">The Store</a></li>
        <li><a href="/thf-podcast">The Show</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>HUMAN OS WIKI</h4>
      <ul>
        <li><a href="/human-os/">All wiki pages</a></li>
        <li><a href="/human-os/fawn-response">Fawn Response</a></li>
        <li><a href="/human-os/cyclic-sighing">Cyclic Sighing OS</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>CONTACT</h4>
      <ul>
        <li><a href="mailto:jaredhmn@gmail.com">jaredhmn@gmail.com</a></li>
        <li><a href="https://thehumanfrequency.gumroad.com" rel="noopener">Gumroad store</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 The Human Frequency Inc. — All rights reserved.</span>
    <span>Built with empathy.</span>
  </div>
</footer>
""".strip()

SCRIPT_BLOCK = """
<script>
async function beehiivSubscribe(form, tag) {
  const input = form.querySelector('input[type="email"]');
  const btn = form.querySelector('button');
  const honeypot = form.querySelector('input[name="bot-field"]');
  const email = input ? input.value.trim() : '';
  if (!email || !email.includes('@')) {
    if (input) { input.style.borderColor = 'rgba(255,69,0,0.7)'; input.placeholder = 'Enter a valid email'; }
    return;
  }
  btn.textContent = 'Joining...';
  btn.disabled = true;
  input.disabled = true;
  try {
    const res = await fetch('/api/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, utm_source: tag, bot_field: honeypot ? honeypot.value : '' })
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data && data.ok) {
      btn.textContent = "\\u2713 You're In!";
      btn.style.opacity = '0.8';
    } else { throw new Error('subscribe failed'); }
  } catch(err) {
    btn.textContent = 'Try Again';
    btn.disabled = false;
    input.disabled = false;
  }
}
const revealEls = document.querySelectorAll('.reveal');
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }});
}, { threshold: 0.1 });
revealEls.forEach(el => obs.observe(el));
</script>
""".strip()


def render_page(c):
    """Render the full HTML page given a content dict."""
    sections_html = "\n".join(render_section(s) for s in c["sections"])
    steps_html = "\n".join(render_step(s, i) for i, s in enumerate(c["steps"]))
    printable_items = "\n".join(render_printable_item(i) for i in c["printable_card"]["items"])
    exits_html = "\n".join(render_exit(e) for e in c["exits"])
    sources_list_html = "\n".join(f"      <li>{s}</li>" for s in c["sources_list"])
    sources_outro = c.get("sources_outro", "")
    sources_outro_html = f'\n    <p style="margin-top: 14px;">{sources_outro}</p>' if sources_outro else ""

    title_html = f'{c["title_pre_words"]} <span class="grad">{c["title_grad_word"]}</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{c["title"]} — The Human OS Wiki | The Human Frequency</title>
<meta name="description" content="{c["meta_description"]}">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<meta name="theme-color" content="#0a0e1a">

<meta property="og:type" content="article">
<meta property="og:url" content="https://thehumanfrequency.net/human-os/{c["slug"]}">
<meta property="og:title" content="{c["title"]} — The Human OS Wiki">
<meta property="og:description" content="{c["og_description"]}">
<meta property="og:image" content="https://thehumanfrequency.net/og-image.png">
<meta property="og:site_name" content="The Human Frequency">
<meta property="article:section" content="Understanding Yourself">
<meta property="article:published_time" content="{c["date_published"]}">
<meta property="article:modified_time" content="{c["date_published"]}">
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:title" content="{c["title"]} — The Human OS Wiki">
<meta property="twitter:description" content="{c["twitter_description"]}">
<meta property="twitter:image" content="https://thehumanfrequency.net/og-image.png">
<link rel="canonical" href="https://thehumanfrequency.net/human-os/{c["slug"]}">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{c["title"]}",
  "description": "{c["meta_description"]}",
  "author": {{ "@type": "Person", "name": "Jared Ohman" }},
  "publisher": {{
    "@type": "Organization",
    "name": "The Human Frequency",
    "logo": {{ "@type": "ImageObject", "url": "https://thehumanfrequency.net/og-image.png" }}
  }},
  "datePublished": "{c["date_published"]}",
  "dateModified": "{c["date_published"]}",
  "mainEntityOfPage": "https://thehumanfrequency.net/human-os/{c["slug"]}",
  "image": "https://thehumanfrequency.net/og-image.png",
  "articleSection": "{c["pillar"].title()}",
  "keywords": "{c["schema_keywords"]}"
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">

<style>
{CSS_BLOCK}
</style>
</head>
<body>

{NAV_BLOCK}

<nav class="crumb" aria-label="breadcrumb">
  <a href="/">Home</a><span class="sep">/</span><a href="/human-os/">The Human OS Wiki</a><span class="sep">/</span>{c["title"]}
</nav>

<header class="hero">
  <div class="hero-eyebrow">HUMAN OS WIKI · {c["page_num"]} · {c["pillar"]}</div>
  <h1>{title_html}</h1>
  <p class="hero-thesis">{c["thesis"]}</p>
  <div class="hero-meta">
    <span>{c["reading_time"]}</span>
    <span>Last updated {c["last_updated"]}</span>
    <span>Source: {c["source_chapter"]}</span>
  </div>
</header>

<section class="pullquote reveal">
  <div class="pullquote-inner">
    {c["pull_quote"]["text"]}
    <span class="pullquote-cite">{c["pull_quote"]["cite"]}</span>
  </div>
</section>

<article class="reading">

{sections_html}

  <div class="steps">
{steps_html}
  </div>

  <h2>{c["after_steps_h2"]}</h2>
  <p>{c["after_steps_p"]}</p>
</article>

<section class="printable reveal">
  <div class="printable-card">
    <div class="pc-title">{c["printable_card"]["title"]}</div>
    <div class="pc-sub">{c["printable_card"]["subtitle"]}</div>
    <hr class="pc-rule">

{printable_items}

    <hr class="pc-rule">
    <div class="pc-foot">THE HUMAN FREQUENCY · FIND COMMON GROUND</div>
  </div>
</section>

<article class="reading">
  <h2>Go deeper</h2>
  <p>This page is the surface. Each layer below goes further.</p>

  <div class="exits">
{exits_html}
  </div>
</article>

<section class="newsletter reveal" id="newsletter">
  <div class="newsletter-card">
    <div class="nl-eyebrow">THE HUMAN OS WIKI · WEEKLY</div>
    <h2 class="nl-title">Get the next page in your inbox</h2>
    <p class="nl-sub">One operating system per week. Sourced from the books. Plain language, real citations. Unsubscribe in one click.</p>
    <form class='nl-form' name='{c["subscribe_form_name"]}' onsubmit="event.preventDefault(); beehiivSubscribe(this, '{c["subscribe_source"]}');">
      <input type="hidden" name="bot-field" style="display:none">
      <input type="email" name="email" placeholder="your@email.com" required>
      <button class="btn-primary" type="submit">Send me the wiki</button>
    </form>
    <p class="nl-note">No spam, ever. We send the wiki, the newsletter, and nothing else.</p>
  </div>
</section>

<details class="sources">
  <summary class="sources-toggle">
    <span>SOURCES &amp; CITATIONS</span><span class="arrow">▾</span>
  </summary>
  <div class="sources-body">
    <p>{c["sources_intro"]}</p>
    <ul>
{sources_list_html}
    </ul>{sources_outro_html}
  </div>
</details>

{FOOTER_BLOCK}

{SCRIPT_BLOCK}

</body>
</html>
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate-wiki-page.py <content.json> <output.html>")
        print("\nSchema:")
        print(SCHEMA)
        sys.exit(1)

    content_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    content = json.loads(content_path.read_text(encoding="utf-8"))
    html = render_page(content)
    output_path.write_text(html, encoding="utf-8")

    lines = html.count("\n") + 1
    bytes_ = len(html.encode("utf-8"))
    print(f"  Wrote {output_path}  ({lines} lines, {bytes_:,} bytes)")


if __name__ == "__main__":
    main()
