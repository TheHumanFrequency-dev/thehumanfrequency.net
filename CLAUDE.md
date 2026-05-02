# CLAUDE.md — thehumanfrequency.net

You are working on the **public marketing site for The Human Frequency Inc.** Live at `https://thehumanfrequency.net`. Hosted on **Cloudflare Pages** with **Cloudflare Pages Functions** for serverless API routes.

This is the most audience-facing surface in the entire THF system. Strict brand voice applies. Strict visual system applies. Don't add a JS framework.

Read this file first. Read `llms.txt` for the structured brand reference (it's the source of truth for how AI agents — including you — should describe THF). Read `robots.txt` for crawler policy.

---

## What this repo is

**Stack:** **Vanilla HTML/CSS/JS output served by Cloudflare Pages.** The deployed site is plain static HTML — no JS framework, no client-side hydration. Pages are generated locally by a Python+Jinja2 build pipeline (`scripts/build.py`) from source templates in `_src/`. The `functions/` directory holds Cloudflare Pages Functions (server-side API routes).

**Why no JS framework:** Speed, SEO, AI-native vibe-codeability, and zero deploy-time build risk. Don't propose React, Next.js, Astro, or any client-side framework migration. The Python build pipeline is the source of truth; the HTML at root is the deploy artifact.

**Build flow:**

```
_src/pages/*.html      Jinja2 templates (extend base.html, define blocks)
_src/partials/*.html   Shared head_assets, announce_bar, nav, footer, back_to_top
_src/partials/*.js     Shared client JS (e.g. beehiiv_subscribe.js)
_src/base.html         Root layout with blocks: head_extra, page_styles, content, page_scripts
        ↓  python3 scripts/build.py
*.html at root         Plain HTML deployed by Cloudflare Pages
```

Run `python3 scripts/build.py` locally before commit. Run `python3 scripts/build.py --check` to render and diff without writing. Cloudflare Pages config is unchanged — it still deploys static HTML from the repo root.

**Pages (top-level HTML files generated from `_src/pages/`):**
| File | Purpose | Templated |
|---|---|---|
| `index.html` | Homepage | yes |
| `about.html` | Founder + brand story | yes |
| `thf-podcast.html` | Live show waitlist | yes |
| `thf-store.html` | Gumroad guide catalog | yes |
| `404.html` | Branded not-found page | yes |
| `human-os/index.html` | Wiki landing page | yes |
| `human-os/<topic>.html` × 28 | Individual wiki pages | not yet (Phase 2) |
| `success.html` | Post-signup confirmation | no — intentionally minimal |

**API functions:**
- `functions/api/subscribe.js` — Beehiiv newsletter signup proxy. Server-side keeps the API key off the client.

**`_src/` is committed for version control but blocked from public access** by `_redirects` (any `/_src/*` request returns 404). Same for `/scripts/*`.

---

## 🔒 LOCKED RULES — DO NOT VIOLATE

### 1. No JS frameworks. No deploy-time build. Static HTML output only.
The site is intentionally static at deploy time. Don't introduce React, Astro, Hugo, Eleventy, Vite, webpack, or any client-side or deploy-time JS framework. The Python+Jinja2 local build pipeline (`scripts/build.py`) is the only build step, and it produces vanilla HTML. If you find yourself wanting to add client-side hydration, an SSR runtime, or a framework adapter for Cloudflare, stop. Static output is the point.

### 2. Brand voice is non-negotiable
THF voice rules apply to every word visible to a reader:
- **Specific over abstract** — numbers, names, dates
- **Plain over clever** — never make a reader re-parse a sentence
- **Warm over neutral** — readers are real people, often in pain
- **Hard truths kindly** — don't hedge, don't pander
- **Empathy without flattery**

**Banned phrases — scrub every draft:**
- Em-dash overload (the AI cadence tell)
- "It's not just X — it's Y"
- "Buckle up," "let me cook"
- "Boasts," "robust," "dive into," "delve into," "elevate," "unlock"
- Generic motivational quotes
- Corporate hedging ("may potentially help")

### 3. Visual system locked
- **Colors:** Midnight Navy `#0A1628`, Orange `#F08C30`, Gold `#D4A847`, Magenta `#C73E5C`, Cream `#F5F0E1`
- **Typography:** Bebas Neue (display impact), Playfair Display (editorial), DM Sans (body/UI)
- Don't introduce off-palette colors. Don't swap fonts. Don't add gradients outside the established Orange→Magenta gradient.

### 4. Tagline is "Find Common Ground" — exact, never paraphrased
Don't write "find common ground," "finding common ground," or any other variation in headers or hero copy. The tagline appears as defined or it doesn't appear.

### 5. Three pillars are the editorial scope
Content lives within: **Understanding Yourself / Understanding Your Kids / Understanding Each Other.** Trading content (ScannrAI), creator content (SocialCortex), and other adjacent surfaces are NOT part of this site's editorial scope. Don't add them.

### 6. Secrets stay server-side
Beehiiv API key, any future API keys: Cloudflare Pages env vars only. **Never** put them in HTML, JS, or commit them to the repo. The `functions/api/` proxy pattern is how we handle every external API call.

### 7. SEO + AI discoverability are first-class
- `sitemap.xml` must list every published page
- `llms.txt` must stay accurate as products and services evolve
- `robots.txt` explicitly allows GPTBot, ClaudeBot, PerplexityBot, etc. — this is intentional. Don't disallow AI crawlers.
- Open Graph metadata on every page (`og-image.png` is the default)

### 8. "What THF is not" applies
From `llms.txt` — THF is **not** a self-help blog, motivational brand, influencer site, or productivity-hack publication. Don't write copy that drifts into those genres.

---

## Conventions

**File structure:**
- `_src/` — Jinja2 source templates (committed, blocked from deploy by `_redirects`)
- `_src/base.html` — root layout with blocks
- `_src/partials/` — shared `head_assets`, `announce_bar`, `nav`, `footer`, `back_to_top`, `beehiiv_subscribe.js`, `base_styles`
- `_src/pages/` — page-specific templates (extend `base.html`)
- `scripts/build.py` — single build entrypoint (run locally; outputs to root)
- `scripts/wiki-content/` — JSON content files for wiki pages (Phase 2)
- HTML pages at repo root — generated build output, deployed by Cloudflare
- Images: PNG/SVG at repo root or in subdirectories
- API: `functions/api/<route>.js` (Cloudflare Pages Functions)
- No `node_modules/`. No client-side JS framework.

**HTML patterns:**
- Page templates extend `base.html` and override blocks: `head_extra`, `page_styles`, `content`, `page_scripts`
- Page-specific styles go in `{% block page_styles %}` (rendered into the shared `<style>` block)
- Page-specific JS goes in `{% block page_scripts %}` (rendered after the shared subscribe + reveal scripts)
- Per-page metadata set via `{% set %}` at top of template: `title`, `description`, `canonical_url`, `og_*`, `active_page`, `tune_in_href`, `announce_link`, `noindex`, `footer_desc`
- Brand fonts loaded from CDN in `partials/head_assets.html`
- Newsletter signup form posts to `/api/subscribe` with `email`, `utm_source`, and a honeypot `bot_field`
- Active nav state: pass `active_page` ∈ `{"mission","show","store","wiki","about"}` (or `none` for utility pages like 404)

**Editing flow:**
- Editing a page → edit `_src/pages/<page>.html`, run `python3 scripts/build.py`, commit both source and generated output
- Editing nav, footer, announce bar, or shared CSS → edit the partial, run build, commit
- One-off content tweak inside a page → edit `_src/pages/<page>.html`, never the generated root file (it'll be overwritten next build)

**Newsletter signup sources** (pre-approved set in `functions/api/subscribe.js`):
- `source-homepage`
- `source-about`
- `source-store-newsletter`
- `source-podcast-notify`
- `source-podcast-waitlist`

If you add a new entry point, add the new source name to the `ALLOWED_SOURCES` set.

**Commits:**
- Author email: `jaredhmn@gmail.com`
- Push to `main` triggers Cloudflare Pages deploy automatically

---

## What NOT to do

- Don't add a JS framework (React, Astro, Hugo, Next, etc.)
- Don't add a deploy-time build step (CF Pages still deploys static HTML; build runs locally)
- Don't add npm or `node_modules/` (Python+Jinja2 only)
- Don't edit generated HTML at root directly — edit `_src/` and re-run build
- Don't put API keys in client HTML or JS
- Don't write motivational, self-help, or "tips & tricks" voice copy
- Don't break the visual system (colors, fonts)
- Don't drift outside the three editorial pillars
- Don't disallow AI crawlers
- Don't paraphrase "Find Common Ground"
- Don't promise a podcast launch date — say "coming soon, no firm date" (per `llms.txt`)
- Don't link guides to anywhere except their canonical Gumroad URLs

---

## Useful starting prompts

### Build a new Wiki page
> Create a new page `<topic>.html` for the THF Wiki at `_src/pages/human-os/<topic>.html` (or content JSON in `scripts/wiki-content/` if Phase 2 wiki templating is wired). Apply THF voice rules: specific over abstract, plain, warm, hard truths kindly. Use the brand color system. Include OG metadata via `{% set %}`, Beehiiv signup form (`source-<topic>`), and links to relevant Gumroad guides where appropriate. Add the new page to `sitemap.xml` and `_src/pages/human-os/index.html`. Update `llms.txt` if the page introduces a new product or service. Run `python3 scripts/build.py` and commit both source and generated output.

### Add a new newsletter signup form
> Add a signup form to `_src/pages/<page>.html`. Post to `/api/subscribe`. Include hidden `utm_source` field with value `source-<placement>`. Add `source-<placement>` to the `ALLOWED_SOURCES` set in `functions/api/subscribe.js`. Style with brand colors. Include a honeypot field named `bot-field`. Run build, commit.

### Update the store catalog
> A new guide is published. Update `_src/pages/thf-store.html` to feature it (and homepage `_src/pages/index.html` if it should appear in store-preview). Match the existing card pattern. Use the canonical Gumroad URL. Update `llms.txt` "Published guides" section. Update `sitemap.xml` if the guide gets a dedicated page. Run build, commit.

### Refresh the homepage hero
> Rewrite the hero in `_src/pages/index.html`. Keep "Find Common Ground" verbatim. Lead with a specific concrete claim about what THF publishes (operating systems, not motivation). Apply voice rules. Keep the section short — one-screen impact. Run build, commit.

### Update nav or footer
> Edit `_src/partials/nav.html` or `_src/partials/footer.html`. Run `python3 scripts/build.py`. All 6+ generated pages will be updated in one pass. Commit source + all changed root HTML.

---

## End

Default to: Jinja2-source-of-truth, vanilla HTML output, brand voice, brand visuals, server-side secrets, three-pillar scope, AI-friendly metadata.
