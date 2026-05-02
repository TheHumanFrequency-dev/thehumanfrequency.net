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


# Match the top-level <nav>...</nav> on a wiki page. The breadcrumb uses
# <nav class="crumb"> which has a class attribute, so the bare `<nav>` opener
# distinguishes the main nav. The `<a class='nav-logo'` inside is an extra
# anchor to make sure we caught the right block.
WIKI_NAV_RE = re.compile(
    r"<nav>\s*\n\s*<a class='nav-logo'.*?</nav>",
    re.DOTALL,
)


def render_wiki(env: Environment, check: bool = False) -> list[tuple[Path, str, str]]:
    """Patch the main nav block of each wiki HTML page with the rendered
    nav.html partial (active_page=wiki). Content stays untouched.

    This solves the "nav change = 28 edits" maintenance pain without forcing
    a content re-render from the (skeletal) JSON files."""
    nav_template = env.get_template("partials/nav.html")
    nav_rendered = nav_template.render(active_page="wiki", tune_in_href="/#newsletter")
    # Drop the leading "<!-- NAV -->\n" comment from the partial so the
    # in-place patch doesn't introduce visible noise.
    nav_clean = re.sub(r"^<!-- NAV -->\s*\n", "", nav_rendered).rstrip()

    results: list[tuple[Path, str, str]] = []
    missing: list[str] = []
    unmatched: list[str] = []

    for slug in WIKI_PAGES:
        path = ROOT / "human-os" / f"{slug}.html"
        if not path.exists():
            missing.append(slug)
            continue
        old_html = path.read_text(encoding="utf-8")
        new_html, n = WIKI_NAV_RE.subn(nav_clean, old_html, count=1)
        if n == 0:
            unmatched.append(slug)
            continue
        results.append((path, new_html, old_html))

    if missing:
        print(f"  ! missing files: {', '.join(missing)}")
    if unmatched:
        print(f"  ! nav anchor not matched in: {', '.join(unmatched)}")

    return results


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
    p.add_argument("--wiki",  action="store_true", help="Only build wiki pages (Phase 2)")
    args = p.parse_args()

    do_pages = args.pages or not args.wiki
    do_wiki  = args.wiki  or not args.pages

    env = make_env()
    all_results: list[tuple[Path, str, str]] = []

    if do_pages:
        print("=== Top-level pages ===")
        all_results += render_top_level(env, check=args.check)
    if do_wiki:
        print("=== Wiki pages ===")
        all_results += render_wiki(env, check=args.check)

    write_results(all_results, dry_run=args.check)
    return 0


if __name__ == "__main__":
    sys.exit(main())
