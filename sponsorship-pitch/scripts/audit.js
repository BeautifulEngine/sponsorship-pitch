// Evaluated inside the rendered document by render.cjs / render.py.
// Returns: which fonts actually loaded, and every text element (outside the cover)
// whose contrast against its real background is under 4.5:1.
(() => {
  const css = getComputedStyle(document.documentElement);
  const v = (n) => css.getPropertyValue(n).trim();
  const fam = (n) => v(n).split(',')[0].replace(/["']/g, '').trim();
  const loaded = (f) => [...document.fonts].some((x) => x.family.replace(/["']/g, '') === f && x.status === 'loaded');
  const fonts = ['--font-display', '--font-body', '--font-label'].map((n) => ({ token: n, family: fam(n), loaded: loaded(fam(n)) }));

  const parse = (c) => {
    const m = (c.match(/[\d.]+/g) || ['255', '255', '255']).map(Number);
    return c.startsWith('color(') ? m.slice(0, 3).map((x) => x * 255) : m.slice(0, 3);
  };
  const lum = (c) => { const f = (x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }; const [r, g, b] = parse(c); return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const transparent = (c) => !c || /rgba\(0, 0, 0, 0\)|transparent/.test(c) || /,\s*0\)$/.test(c);
  const bgOf = (e) => { while (e) { const c = getComputedStyle(e).backgroundColor; if (!transparent(c)) return c; e = e.parentElement; } return v('--paper') || 'rgb(255,255,255)'; };

  const low = {};
  document.querySelectorAll('body *').forEach((e) => {
    if (e.closest('.cover, .title-slide, [data-audit-skip]')) return;
    if (![...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return;
    const cs = getComputedStyle(e);
    const fg = cs.color, bg = bgOf(e);
    const a = lum(fg), b = lum(bg);
    const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    if (ratio < 4.5) {
      const key = `${e.className || e.tagName.toLowerCase()} | ${fg} on ${bg}`;
      if (!low[key]) low[key] = { ratio: +ratio.toFixed(2), example: e.textContent.trim().slice(0, 50) };
    }
  });
  const attrs = [...document.querySelectorAll('*')].flatMap((e) => [...e.attributes].map((a) => a.value)).join(' ');
  const placeholders = [...new Set((document.body.innerText + ' ' + attrs).match(/\{\{[^}]+\}\}|\bTODO\b|\bTBD\b|lorem ipsum/gi) || [])].slice(0, 10);
  return JSON.stringify({ fonts, lowContrast: low, placeholders });
})()
