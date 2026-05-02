"""
Build thehumanfrequency.net from Jinja2 templates in _src/ → vanilla HTML at root.

Usage:
    python3 scripts/build.py            # build everything
    python3 scripts/build.py --check    # build to /tmp and diff against current root, no writes
    python3 scripts/build.py --pages    # only top-level pages (Phase 1 scope)
    python3 scripts/build.py --wiki     # only wiki pages (Phase 2 scope, not yet wired)

Output is plain HTML with no Jinja syntax. Safe for Cloudflare Pages to serve directly.

The site keeps deploying as a static site; this build runs locally before commit.
No CF Pages config changes required.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, ChainableUndefined
except ImportError:
    sys.stderr.write(
        "ERROR: Jinja2 not installed. Run:\n"
        "  pip install Jinja2\n"
    )
    sys.exit(1)

# Windows console defaults to cp1252; force UTF-8 so unicode in template
# titles, log lines, etc. doesn't crash the build.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# --- Paths ---------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
PAGES_DIR = SRC / "pages"
WIKI_CONTENT_DIR = ROOT / "scripts" / "wiki-content"


# --- Page manifest -------------------------------------------------------
# Each entry: (template_path_under_pages, output_path_under_root)
TOP_LEVEL_PAGES: list[tuple[str, str]] = [
    ("index.html",          "index.html"),
    ("about.html",          "about.html"),
    ("thf-store.html",      "thf-store.html"),
    ("thf-podcast.html",    "thf-podcast.html"),
    ("work-with-me.html",   "work-with-me.html"),
    ("404.html",            "404.html"),
    ("human-os/index.html", "human-os/index.html"),
]
# success.html intentionally not templated — minimal post-signup confirmation,
# no nav/footer, would gain nothing from sharing partials.


# Wiki pages — 28 pages with rich hand-edited content. The Phase 2 strategy
# is "patch chrome only" rather than "re-render from JSON" because the JSON
# files in scripts/wiki-content/ are skeletal and the real content lives in
# the HTML. The build patches the main nav of each wiki page to keep it in
# sync with _src/partials/nav.html, then leaves everything else alone.
WIKI_PAGES: list[str] = [
    # Pillar 01 — Understanding Yourself
    "fawn-response", "cyclic-sighing", "diving-reflex",
    "diaphragmatic-breathing", "humming-protocol",
    "five-non-negotiables", "state-matched-decision-tree",
    "pre-bet-audit", "tilt-taxonomy", "mental-hand-history",
    "executive-function-scaffolding",
    # Pillar 02 — Understanding Your Kids
    "transition-protocol", "meltdown-early-warning",
    "five-task-reframe", "validate-then-redirect",
    "co-parent-alignment", "school-advocacy-letter",
    "medication-decision", "rsd-recognition",
    "rsd-de-escalation", "eight-magic-keys",
    # Pillar 03 — Understanding Each Other
    "scarf-threat-audit", "polyvagal-repair",
    "harvard-method", "gottman-repair",
    "termination-conversation", "salary-negotiation",
    "partner-guide-rsd",
]


# Display title for each wiki page — used in the "Continue the wiki" section
# inserted at the bottom of every wiki page.
WIKI_TITLES: dict[str, str] = {
    "fawn-response": "Fawn Response",
    "cyclic-sighing": "Cyclic Sighing OS",
    "diving-reflex": "Diving Reflex Protocol",
    "diaphragmatic-breathing": "Diaphragmatic Breathing OS",
    "humming-protocol": "Humming and OM Protocol",
    "five-non-negotiables": "The Five Non-Negotiables",
    "state-matched-decision-tree": "State-Matched Decision Tree",
    "pre-bet-audit": "5-Question Pre-Bet Audit",
    "tilt-taxonomy": "Tendler 7-Tilt OS",
    "mental-hand-history": "Mental Hand History OS",
    "executive-function-scaffolding": "Executive Function Scaffolding",
    "transition-protocol": "Transition Protocol OS",
    "meltdown-early-warning": "Meltdown Early-Warning System",
    "five-task-reframe": "The 5-Task Reframe",
    "validate-then-redirect": "Validate-Then-Redirect OS",
    "co-parent-alignment": "Co-Parent Alignment Meeting",
    "school-advocacy-letter": "School Advocacy Letter OS",
    "medication-decision": "Medication Decision Framework",
    "rsd-recognition": "RSD Recognition OS",
    "rsd-de-escalation": "RSD De-Escalation OS",
    "eight-magic-keys": "The 8 Magic Keys (FASD)",
    "scarf-threat-audit": "SCARF Threat Audit OS",
    "polyvagal-repair": "Polyvagal Repair OS",
    "harvard-method": "Harvard Method 4-Step OS",
    "gottman-repair": "Gottman Repair Phrases OS",
    "termination-conversation": "Termination Conversation OS",
    "salary-negotiation": "Salary Negotiation OS",
    "partner-guide-rsd": "Partner's Guide to RSD",
}


# 12-word teaser shown in the "Continue the wiki" cards. Specific over abstract.
WIKI_BLURBS: dict[str, str] = {
    "fawn-response": "The fourth trauma response. Five-stage protocol to stop running it.",
    "cyclic-sighing": "Five minutes a day. Strongest evidence in any 2023 anxiety RCT.",
    "diving-reflex": "Cold water on the face, 15-30 seconds. Heart rate drops 10-25%.",
    "diaphragmatic-breathing": "Eight breaths a minute for parasympathetic dominance. Hopper et al. 2019.",
    "humming-protocol": "Lower stress index than sleep, in a Holter monitoring study.",
    "five-non-negotiables": "Minimum-viable nervous-system maintenance. None more than five minutes.",
    "state-matched-decision-tree": "67% improvement matched vs. 28% generic. Pick the right tool.",
    "pre-bet-audit": "Five questions before any high-stakes choice. Wired to Win Ch. 14.",
    "tilt-taxonomy": "Seven types of tilt, seven cognitive injections. Treat each separately.",
    "mental-hand-history": "Five-step structured writing. Externalize the tilt. Compound the learning.",
    "executive-function-scaffolding": "Externalize what the brain can't internalize. Permanent accommodation, not training wheel.",
    "transition-protocol": "10/5/2 minute warnings, triple-redundant. ~70% reduction in transition meltdowns.",
    "meltdown-early-warning": "Four stages of an ND meltdown. Catch it in Stage 1.",
    "five-task-reframe": "\"Get ready for bed\" is five tasks. The micro-command fix.",
    "validate-then-redirect": "Order matters. Reverse it and you produce escalation. SB Ch. 1+6.",
    "co-parent-alignment": "30 minutes a month. Six items. Prevent slow drift into misalignment.",
    "school-advocacy-letter": "The accommodation request schools can't ignore. Triggers a 30-day evaluation.",
    "medication-decision": "Eight questions for the prescriber. Thirty-day measurable trial framework.",
    "rsd-recognition": "Ten-sign checklist. RSD affects up to 99% of ADHD individuals.",
    "rsd-de-escalation": "Don't argue with the emotion. The 6-step First Aid Protocol.",
    "eight-magic-keys": "The foundational FASD framework. Environment compensates for the brain.",
    "scarf-threat-audit": "Status, Certainty, Autonomy, Relatedness, Fairness. Five-minute audit. Rock 2008.",
    "polyvagal-repair": "When words don't fix it, the body does. Three steps in order.",
    "harvard-method": "The framework that ended Apple-Samsung. Plus BATNA. Fisher and Ury.",
    "gottman-repair": "The Four Horsemen and their antidotes. Three repair phrases.",
    "termination-conversation": "The hardest conversation. Dignity, clarity, legal precision.",
    "salary-negotiation": "Three scripted frameworks plus five non-salary asks.",
    "partner-guide-rsd": "RSD doesn't end at 18. Adult relationship protocol.",
}


# Three thematically related wiki pages for each. Hand-curated, biased toward
# the strongest within-pillar pairings, with a few cross-pillar bridges where
# the topic overlap is real (e.g. RSD <-> Fawn, SCARF <-> Polyvagal).
WIKI_RELATED: dict[str, list[str]] = {
    # Pillar 01
    "fawn-response":                 ["polyvagal-repair", "scarf-threat-audit", "partner-guide-rsd"],
    "cyclic-sighing":                ["diaphragmatic-breathing", "humming-protocol", "diving-reflex"],
    "diving-reflex":                 ["cyclic-sighing", "diaphragmatic-breathing", "polyvagal-repair"],
    "diaphragmatic-breathing":       ["cyclic-sighing", "humming-protocol", "polyvagal-repair"],
    "humming-protocol":              ["cyclic-sighing", "diaphragmatic-breathing", "diving-reflex"],
    "five-non-negotiables":          ["cyclic-sighing", "diaphragmatic-breathing", "executive-function-scaffolding"],
    "state-matched-decision-tree":   ["fawn-response", "scarf-threat-audit", "polyvagal-repair"],
    "pre-bet-audit":                 ["tilt-taxonomy", "mental-hand-history", "state-matched-decision-tree"],
    "tilt-taxonomy":                 ["mental-hand-history", "pre-bet-audit", "polyvagal-repair"],
    "mental-hand-history":           ["tilt-taxonomy", "pre-bet-audit", "state-matched-decision-tree"],
    "executive-function-scaffolding":["eight-magic-keys", "five-non-negotiables", "transition-protocol"],
    # Pillar 02
    "transition-protocol":           ["meltdown-early-warning", "five-task-reframe", "executive-function-scaffolding"],
    "meltdown-early-warning":        ["validate-then-redirect", "transition-protocol", "polyvagal-repair"],
    "five-task-reframe":             ["executive-function-scaffolding", "validate-then-redirect", "transition-protocol"],
    "validate-then-redirect":        ["meltdown-early-warning", "gottman-repair", "scarf-threat-audit"],
    "co-parent-alignment":           ["school-advocacy-letter", "medication-decision", "harvard-method"],
    "school-advocacy-letter":        ["eight-magic-keys", "medication-decision", "co-parent-alignment"],
    "medication-decision":           ["eight-magic-keys", "rsd-recognition", "school-advocacy-letter"],
    "rsd-recognition":               ["rsd-de-escalation", "partner-guide-rsd", "fawn-response"],
    "rsd-de-escalation":             ["rsd-recognition", "partner-guide-rsd", "validate-then-redirect"],
    "eight-magic-keys":              ["executive-function-scaffolding", "school-advocacy-letter", "transition-protocol"],
    # Pillar 03
    "scarf-threat-audit":            ["polyvagal-repair", "harvard-method", "gottman-repair"],
    "polyvagal-repair":              ["scarf-threat-audit", "cyclic-sighing", "gottman-repair"],
    "harvard-method":                ["gottman-repair", "salary-negotiation", "scarf-threat-audit"],
    "gottman-repair":                ["harvard-method", "scarf-threat-audit", "validate-then-redirect"],
    "termination-conversation":      ["harvard-method", "scarf-threat-audit", "salary-negotiation"],
    "salary-negotiation":            ["harvard-method", "termination-conversation", "scarf-threat-audit"],
    "partner-guide-rsd":             ["rsd-recognition", "rsd-de-escalation", "fawn-response"],
}


# --- Jinja env -----------------------------------------------------------
def make_env() -> Environment:
    # ChainableUndefined: undefined vars render as empty string and don't error
    # on attribute access, but typos still produce visible empty output we can spot
    # in the diff. Stricter than default Undefined; less brittle than StrictUndefined.
    env = Environment(
        loader=FileSystemLoader(str(SRC)),
        autoescape=False,                 # we write trusted HTML; escape manually where needed
        undefined=ChainableUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )
    return env


# --- Renderers -----------------------------------------------------------
def render_top_level(env: Environment, check: bool = False) -> list[tuple[Path, str, str]]:
    """Render top-level pages. Returns [(out_path, new_html, old_html)]."""
    results: list[tuple[Path, str, str]] = []
    for template_rel, out_rel in TOP_LEVEL_PAGES:
        template = env.get_template(f"pages/{template_rel}")
        new_html = template.render()
        out_path = ROOT / out_rel
        old_html = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        results.append((out_path, new_html, old_html))
    return results


# Anchors for wiki page chrome patching. The breadcrumb uses
# <nav class="crumb">; the bare `<nav>` opener picks the main nav. The
# <a class='nav-logo'> tag inside is an extra anchor to confirm the match.
WIKI_NAV_RE = re.compile(
    r"<nav>\s*\n\s*<a class='nav-logo'.*?</nav>",
    re.DOTALL,
)
WIKI_FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.DOTALL)
# 4-col → 5-col grid + matching gap value
WIKI_FOOTER_GRID_RE = re.compile(
    r"\.footer-grid \{ max-width: 1200px; margin: 0 auto; display: grid; "
    r"grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; margin-bottom: 48px; \}"
)
WIKI_FOOTER_GRID_NEW = (
    ".footer-grid { max-width: 1200px; margin: 0 auto; display: grid; "
    "grid-template-columns: 2fr 1fr 1fr 1fr 1fr; gap: 36px; margin-bottom: 48px; }"
)

# Related-OS section: idempotent block insertion just before the newsletter
# section on each wiki page. The HTML comment markers let re-runs replace the
# block in place rather than duplicate it.
RELATED_BLOCK_RE = re.compile(
    r"\s*<!-- BUILD:related-start -->.*?<!-- BUILD:related-end -->\s*\n",
    re.DOTALL,
)
NEWSLETTER_ANCHOR_RE = re.compile(r"<section class=\"newsletter")


def _strip_partial_comment(html: str, marker: str) -> str:
    """Drop a leading "<!-- MARKER -->\\n" comment so partial inserts don't
    introduce visible noise when patched into existing pages."""
    return re.sub(rf"^<!-- {marker} -->\s*\n", "", html).rstrip()


def render_related_block(slug: str) -> str:
    """Render the 'Continue the wiki' section that links to 3 related pages."""
    related = WIKI_RELATED.get(slug, [])
    cards: list[str] = []
    for rel in related:
        title = WIKI_TITLES.get(rel, rel)
        blurb = WIKI_BLURBS.get(rel, "")
        cards.append(
            f'      <a class="exit-card reveal" href="/human-os/{rel}">\n'
            f'        <span class="exit-tag community">RELATED OS</span>\n'
            f'        <h4>{title}</h4>\n'
            f'        <p>{blurb}</p>\n'
            f'        <span class="exit-arrow">Read &rarr;</span>\n'
            f'      </a>'
        )
    cards_html = "\n".join(cards)
    return (
        '<!-- BUILD:related-start -->\n'
        '<article class="reading">\n'
        '  <h2>Continue the wiki</h2>\n'
        '  <p>Three more operating systems most readers of this page also need.</p>\n'
        '  <div class="exits">\n'
        f'{cards_html}\n'
        '  </div>\n'
        '</article>\n'
        '<!-- BUILD:related-end -->\n\n'
    )


def render_wiki(env: Environment, check: bool = False) -> list[tuple[Path, str, str]]:
    """Patch the main nav, footer, and footer-grid CSS of each wiki HTML
    page so they stay in sync with _src/partials/. Page content untouched.

    Solves the "chrome change = 28 edits" maintenance pain without forcing
    a content re-render from the (skeletal) JSON files."""
    nav_template    = env.get_template("partials/nav.html")
    footer_template = env.get_template("partials/footer.html")

    nav_rendered    = nav_template.render(active_page="wiki", tune_in_href="/#newsletter")
    footer_rendered = footer_template.render()

    nav_clean    = _strip_partial_comment(nav_rendered,    "NAV")
    footer_clean = _strip_partial_comment(footer_rendered, "FOOTER")

    results: list[tuple[Path, str, str]] = []
    missing: list[str] = []
    unmatched_nav: list[str] = []
    unmatched_footer: list[str] = []
    unmatched_related: list[str] = []

    for slug in WIKI_PAGES:
        path = ROOT / "human-os" / f"{slug}.html"
        if not path.exists():
            missing.append(slug)
            continue

        old_html = path.read_text(encoding="utf-8")
        new_html = old_html

        # 1. Patch main nav
        new_html, n_nav = WIKI_NAV_RE.subn(nav_clean, new_html, count=1)
        if n_nav == 0:
            unmatched_nav.append(slug)

        # 2. Patch footer (the whole <footer>...</footer> block)
        new_html, n_foot = WIKI_FOOTER_RE.subn(footer_clean, new_html, count=1)
        if n_foot == 0:
            unmatched_footer.append(slug)

        # 3. Patch the footer-grid CSS rule from 4-col → 5-col
        new_html = WIKI_FOOTER_GRID_RE.sub(WIKI_FOOTER_GRID_NEW, new_html, count=1)

        # 4. Insert / replace the "Continue the wiki" related-OS block.
        # Strip any prior block first (idempotency), then insert before
        # the newsletter section.
        new_html = RELATED_BLOCK_RE.sub("\n", new_html)
        related_block = render_related_block(slug)
        new_html, n_rel = NEWSLETTER_ANCHOR_RE.subn(
            f"{related_block}<section class=\"newsletter",
            new_html,
            count=1,
        )
        if n_rel == 0:
            unmatched_related.append(slug)

        results.append((path, new_html, old_html))

    if missing:
        print(f"  ! missing files:           {', '.join(missing)}")
    if unmatched_nav:
        print(f"  ! nav not matched in:       {', '.join(unmatched_nav)}")
    if unmatched_footer:
        print(f"  ! footer not matched in:    {', '.join(unmatched_footer)}")
    if unmatched_related:
        print(f"  ! newsletter anchor missing: {', '.join(unmatched_related)}")

    return results


# --- Sitemap generator ---------------------------------------------------
SITEMAP_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
SITEMAP_FOOTER = "</urlset>\n"


def render_sitemap(today: str | None = None) -> tuple[Path, str, str]:
    """Generate sitemap.xml from the page manifests. Returns (path, new, old)."""
    from datetime import date as _date
    today = today or _date.today().isoformat()

    entries: list[tuple[str, str, str, str]] = [
        # (loc, lastmod, changefreq, priority)
        ("https://thehumanfrequency.net/",              today, "weekly",  "1.0"),
        ("https://thehumanfrequency.net/about",         today, "monthly", "0.9"),
        ("https://thehumanfrequency.net/thf-store",     today, "weekly",  "0.9"),
        ("https://thehumanfrequency.net/thf-podcast",   today, "weekly",  "0.8"),
        ("https://thehumanfrequency.net/work-with-me",  today, "monthly", "0.7"),
        ("https://thehumanfrequency.net/human-os/",     today, "weekly",  "0.85"),
    ]
    for slug in WIKI_PAGES:
        entries.append((f"https://thehumanfrequency.net/human-os/{slug}", today, "monthly", "0.8"))

    body = ""
    for loc, lastmod, changefreq, priority in entries:
        body += (
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>\n"
        )

    new_xml = SITEMAP_HEADER + body + SITEMAP_FOOTER
    path = ROOT / "sitemap.xml"
    old_xml = path.read_text(encoding="utf-8") if path.exists() else ""
    return path, new_xml, old_xml


# --- Diff helpers --------------------------------------------------------
def diff_summary(old: str, new: str) -> str:
    if old == new:
        return "identical"
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    delta = len(new_lines) - len(old_lines)
    sign = "+" if delta >= 0 else ""
    return f"changed ({sign}{delta} lines, {len(old)} -> {len(new)} bytes)"


def write_results(results: list[tuple[Path, str, str]], dry_run: bool) -> None:
    changed = 0
    for out_path, new_html, old_html in results:
        rel = out_path.relative_to(ROOT)
        status = diff_summary(old_html, new_html)
        marker = "  " if old_html == new_html else "* "
        print(f"  {marker}{str(rel):40s} {status}")
        if not dry_run and old_html != new_html:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(new_html, encoding="utf-8")
            changed += 1
    if not dry_run:
        print(f"\nWrote {changed} changed file(s).")


# --- Entrypoint ----------------------------------------------------------
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="Render and diff but do not write")
    p.add_argument("--pages", action="store_true", help="Only build top-level pages")
    p.add_argument("--wiki",  action="store_true", help="Only build wiki pages (chrome patch)")
    p.add_argument("--sitemap", action="store_true", help="Only regenerate sitemap.xml")
    args = p.parse_args()

    only_one = args.pages or args.wiki or args.sitemap
    do_pages   = args.pages   or not only_one
    do_wiki    = args.wiki    or not only_one
    do_sitemap = args.sitemap or not only_one

    env = make_env()
    all_results: list[tuple[Path, str, str]] = []

    if do_pages:
        print("=== Top-level pages ===")
        all_results += render_top_level(env, check=args.check)
    if do_wiki:
        print("=== Wiki pages ===")
        all_results += render_wiki(env, check=args.check)
    if do_sitemap:
        print("=== Sitemap ===")
        all_results.append(render_sitemap())

    write_results(all_results, dry_run=args.check)
    return 0


if __name__ == "__main__":
    sys.exit(main())
