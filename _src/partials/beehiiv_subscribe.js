// ===== BEEHIIV SUBSCRIBE (proxied via /api/subscribe — no key in client) =====
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
      btn.textContent = "✓ You're In!";
      btn.style.opacity = '0.8';
    } else {
      throw new Error('subscribe failed');
    }
  } catch(err) {
    btn.textContent = 'Try Again';
    btn.disabled = false;
    input.disabled = false;
  }
}

// ===== SHARED SCROLL REVEAL =====
(function() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.1 });
  els.forEach(el => obs.observe(el));
})();

// ===== SHARED BACK TO TOP =====
window.addEventListener('scroll', () => {
  const bt = document.getElementById('back-top');
  if (bt) bt.style.opacity = window.scrollY > 400 ? '1' : '0';
});
