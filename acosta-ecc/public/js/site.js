(() => {
  const PHONE_TEL = '+34669768659';
  const WA = 'https://wa.me/34669768659';

  document.getElementById('year').textContent = new Date().getFullYear();

  // menú móvil
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });

  // aparición al hacer scroll
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { threshold: 0.12 });
    els.forEach((el) => io.observe(el));
  } else els.forEach((el) => el.classList.add('in'));

  // formulario
  const form = document.getElementById('quote');
  const msg = document.getElementById('formMsg');
  const btn = document.getElementById('submit');

  const show = (kind, html) => { msg.className = `form-msg show ${kind}`; msg.replaceChildren(...html); msg.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); };
  const text = (t) => { const p = document.createElement('pre'); p.textContent = t; return p; };
  const actions = (waText) => {
    const row = document.createElement('div'); row.className = 'cta-row';
    const call = Object.assign(document.createElement('a'), { className: 'btn btn-fire', href: `tel:${PHONE_TEL}`, textContent: 'Llamar al 669 76 86 59' });
    const wa = Object.assign(document.createElement('a'), { className: 'btn btn-wa', href: `${WA}?text=${encodeURIComponent(waText)}`, target: '_blank', rel: 'noopener', textContent: 'Seguir por WhatsApp' });
    row.append(call, wa); return row;
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form));
    const missing = !d.nombre?.trim() || !d.telefono?.trim() || !d.municipio || !d.tipo;
    if (missing) return show('err', [text('Por favor, rellena nombre, teléfono, municipio y qué necesitas.')]);
    if (!/^[+\d][\d\s.-]{8,15}$/.test(d.telefono.trim())) return show('err', [text('El teléfono no parece válido. Ejemplo: 669 76 86 59')]);
    if (!d.privacidad) return show('err', [text('Para enviar la solicitud debes aceptar la política de privacidad.')]);

    btn.disabled = true; btn.textContent = 'Enviando…';
    const waText = `Hola, soy ${d.nombre.trim()}. Necesito ${form.tipo.selectedOptions[0].text.toLowerCase()} en ${d.municipio}.`;
    try {
      const res = await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...d, privacidad: true }) });
      const j = await res.json();
      if (!res.ok) throw new Error(j.error || 'Error');
      show('ok', [text(j.message), actions(waText)]);
      if (j.received) form.reset();
    } catch (err) {
      show('err', [text('No hemos podido enviar la solicitud desde la web. Puedes llamarnos o escribirnos por WhatsApp y te atendemos enseguida.'), actions(waText)]);
    } finally { btn.disabled = false; btn.textContent = 'Enviar solicitud'; }
  });
})();
