// /api/subscribe — server-side proxy to Beehiiv
// Keeps the Beehiiv API key in Cloudflare env vars, never in client HTML.
//
// Required env vars (Pages → Settings → Environment variables → Production):
//   BEEHIIV_API_KEY  (Encrypted) — your Beehiiv API key
//   BEEHIIV_PUB_ID   (Plaintext) — e.g. pub_db92e432-ac6a-4d70-89dc-54e92192e84d
//
// Expected POST body (JSON):
//   { email: "user@example.com", utm_source: "source-homepage", bot_field: "" }

const ALLOWED_SOURCES = new Set([
  'source-homepage',
  'source-about',
  'source-store-newsletter',
  'source-podcast-notify',
  'source-podcast-waitlist',
]);

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    },
  });

export async function onRequestPost({ request, env }) {
  // 1. Parse body defensively
  let payload;
  try {
    payload = await request.json();
  } catch {
    return json({ ok: false, error: 'invalid_json' }, 400);
  }

  const email = (payload?.email || '').trim().toLowerCase();
  const utm_source = (payload?.utm_source || '').trim();
  const bot_field = (payload?.bot_field || '').trim();

  // 2. Honeypot — silent success so bots can't tell they were caught
  if (bot_field) {
    return json({ ok: true, status: 'queued' });
  }

  // 3. Validate email
  if (!email || !EMAIL_RE.test(email) || email.length > 254) {
    return json({ ok: false, error: 'invalid_email' }, 400);
  }

  // 4. Validate UTM source against allowlist (anti-tampering)
  if (!ALLOWED_SOURCES.has(utm_source)) {
    return json({ ok: false, error: 'invalid_source' }, 400);
  }

  // 5. Confirm env wired
  const apiKey = env.BEEHIIV_API_KEY;
  const pubId = env.BEEHIIV_PUB_ID;
  if (!apiKey || !pubId) {
    return json({ ok: false, error: 'server_misconfigured' }, 500);
  }

  // 6. Forward to Beehiiv
  try {
    const beehiivRes = await fetch(
      `https://api.beehiiv.com/v2/publications/${encodeURIComponent(pubId)}/subscriptions`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          email,
          reactivate_existing: true,
          send_welcome_email: true,
          utm_source,
        }),
      }
    );

    if (!beehiivRes.ok) {
      // Don't leak Beehiiv's response shape to the client
      return json({ ok: false, error: 'upstream_error' }, 502);
    }

    return json({ ok: true });
  } catch {
    return json({ ok: false, error: 'network_error' }, 502);
  }
}

// Reject non-POST requests cleanly. (onRequestPost above handles POST.)
export async function onRequestGet() {
  return new Response('Method Not Allowed', {
    status: 405,
    headers: { Allow: 'POST' },
  });
}
