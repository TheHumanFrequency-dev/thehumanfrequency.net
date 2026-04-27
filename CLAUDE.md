# CLAUDE.md — thehumanfrequency.net

You are working on the **public marketing site for The Human Frequency Inc.** Live at `https://thehumanfrequency.net`. Hosted on **Cloudflare Pages** with **Cloudflare Pages Functions** for serverless API routes.

This is the most audience-facing surface in the entire THF system. Strict brand voice applies. Strict visual system applies. Don't add a framework.

Read this file first. Read `llms.txt` for the structured brand reference (it's the source of truth for how AI agents — including you — should describe THF). Read `robots.txt` for crawler policy.

---

## What this repo is

**Stack:** **Vanilla HTML/CSS/JS — no framework, no build step.** Just static files served from the repo root by Cloudflare Pages. The `functions/` directory holds Cloudflare Pages Functions (server-side API routes).

**Why no framework:** Speed, simplicity, and the founder can hand-edit any page in 30 seconds. Don't propose React, Next.js, Astro, or any framework migration. Keep it static.

**Pages (top-level HTML files):**
| File | Purpose |
|---|---|
| `index.html` | Homepage |
| `about.html` | Founder + brand story |
| `thf-podcast.html` | Live show waitlist |
| `thf-store.html` | Gumroad guide catalog |
| `success.html` | Generic post-signup confirmation |
| `404.html` (if exists) | Not found |

**API functions:**
- `functions/api/subscribe.js` — Beehiiv newsletter signup proxy. Server-side keeps the API key off the client.

**Future pages (planned):** evergreen "Wiki" pages on operating-system topics (Fawn Response, RSD, ND Meltdown, Difficult Conversations, Self-Care, Transition Checklist, Executive Function). When you're asked to build one, follow the existing page patterns.

---

## 🔒 LOCKED RULES — DO NOT VIOLATE

### 1. No frameworks. No build step. Vanilla HTML/CSS/JS only.
This site is intentionally static. Don't introduce React, Astro, Hugo, Eleventy, Vite, webpack, npm scripts, or any build pipeline. If you find yourself wanting to "modernize" the stack, stop. The simplicity is the point.

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
- HTML pages at repo root
- Images: PNG/SVG at repo root or in subdirectories
- API: `functions/api/<route>.js` (Cloudflare Pages Functions)
- No `src/`, no `dist/`, no `node_modules/`

**HTML patterns:**
- Each page is self-contained — no shared header/footer template engine
- Inline `<style>` blocks for page-specific CSS, OR a shared `<link>` to a global stylesheet (check existing pages for which is used)
- Brand fonts loaded from CDN in `<head>`
- Social/OG meta tags in every page
- Newsletter signup form posts to `/api/subscribe` with `email`, `utm_source`, and a honeypot `bot_field`

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

- Don't add a framework (React, Astro, Hugo, etc.)
- Don't add a build step or npm dependency
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
> Create a new page `<topic>.html` for the THF Wiki. Topic: <topic>. Follow the layout of existing pages (`about.html` is a good reference for long-form). Apply THF voice rules: specific over abstract, plain, warm, hard truths kindly. Use the brand color system. Include OG metadata, Beehiiv signup form (`source-<topic>`), and links to relevant Gumroad guides where appropriate. Add the new page to `sitemap.xml`. Update `llms.txt` if the page introduces a new product or service.

### Add a new newsletter signup form
> Add a signup form to `<page>.html`. Post to `/api/subscribe`. Include hidden `utm_source` field with value `source-<placement>`. Add `source-<placement>` to the `ALLOWED_SOURCES` set in `functions/api/subscribe.js`. Style with brand colors. Include a honeypot field named `bot_field`.

### Update the store catalog
> A new guide is published. Update `thf-store.html` to feature it. Match the existing card pattern. Use the canonical Gumroad URL. Update `llms.txt` "Published guides" section. Update `sitemap.xml` if the guide gets a dedicated page.

### Refresh the homepage hero
> Rewrite the homepage hero in `index.html`. Keep "Find Common Ground" verbatim. Lead with a specific concrete claim about what THF publishes (operating systems, not motivation). Apply voice rules. Keep the section short — one-screen impact.

---

## End

Default to: vanilla, brand voice, brand visuals, server-side secrets, three-pillar scope, AI-friendly metadata.
