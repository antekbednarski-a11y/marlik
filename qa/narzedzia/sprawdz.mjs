// Wykonuje przypadki testowe z katalogu B (UI / dostępność / układ) na wyrenderowanych ekranach.
// Każde wykonanie = jeden przypadek testowy na jednym ekranie (i jednym wariancie kolorystycznym,
// jeśli wynik zależy od kolorów). Wyniki trafiają do CSV i JSON z dowodami (lista elementów).
//
// Użycie: node sprawdz.mjs <katalog z render.mjs> <katalog wyników>
// Wymaga Playwrighta (globalnie lub lokalnie) i Chromium.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const [renderDir, outDir] = process.argv.slice(2);
if (!renderDir || !outDir) {
  console.error('Użycie: node sprawdz.mjs <render/> <wyniki/>');
  process.exit(2);
}
fs.mkdirSync(path.join(outDir, 'zrzuty'), { recursive: true });

let playwright;
try {
  playwright = createRequire(import.meta.url)('playwright');
} catch {
  const globalRoot = execSync('npm root -g').toString().trim();
  playwright = createRequire(path.join(globalRoot, 'noop.js'))('playwright');
}

const manifest = JSON.parse(fs.readFileSync(path.join(renderDir, 'manifest.json'), 'utf8'));

// Funkcja wykonywana w przeglądarce: mierzy wszystko, czego potrzebują przypadki testowe.
function measure(kind) {
  const root = document.body.firstElementChild;
  const R = root.getBoundingClientRect();
  const parse = (s) => {
    const m = s && s.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[\s,/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  const blend = (fg, bg) => [0, 1, 2].map((i) => fg[i] * fg[3] + bg[i] * (1 - fg[3])).concat(1);
  const effBg = (el) => {
    const stack = [];
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor);
      if (c && c[3] > 0) stack.push(c);
      if (c && c[3] >= 1) break;
    }
    let bg = [255, 255, 255, 1];
    for (let i = stack.length - 1; i >= 0; i--) bg = blend(stack[i], bg);
    return bg;
  };
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const L = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratio = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const hex = (c) => '#' + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  const label = (el) => (el.getAttribute('aria-label') || el.innerText || el.value || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 60);
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };

  const nav = root.querySelector('nav');
  const navTop = nav ? nav.getBoundingClientRect().top : Infinity;

  // Teksty
  const texts = [];
  for (const el of root.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent.trim()).join(' ');
    const isInput = el.tagName === 'INPUT';
    if (!own && !isInput) continue;
    const cs = getComputedStyle(el);
    const bg = effBg(el);
    const fgRaw = parse(cs.color);
    const fg = fgRaw[3] < 1 ? blend(fgRaw, bg) : fgRaw;
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const r = el.getBoundingClientRect();
    const logo = [el, el.parentElement].some((e) => e && /^marlik\.?$/.test(e.textContent.trim()));
    texts.push({
      text: (isInput ? el.value : own).slice(0, 60),
      logo,
      color: hex(fg), bg: hex(bg),
      ratio: Math.round(ratio(fg, bg) * 100) / 100,
      need: large ? 3 : 4.5,
      size, weight,
      ellipsis: cs.textOverflow === 'ellipsis' && el.scrollWidth > el.clientWidth + 1,
      overflowX: cs.textOverflow !== 'ellipsis' && cs.overflow !== 'visible' && el.scrollWidth > el.clientWidth + 1,
      outside: r.right > R.right + 0.5 || r.bottom > R.bottom + 0.5 || r.left < R.left - 0.5,
      underNav: nav && !nav.contains(el) && r.bottom > navTop + 0.5,
      inNav: !!(nav && nav.contains(el)),
    });
  }

  // Elementy interaktywne
  const inter = [];
  for (const el of root.querySelectorAll('a, button, input, select, textarea, [role=button], [tabindex]')) {
    if (!visible(el)) continue;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const parentBg = effBg(el.parentElement);
    const own = parse(cs.backgroundColor);
    const ownBg = own && own[3] > 0 ? blend(own, parentBg) : null;
    const bw = parseFloat(cs.borderTopWidth);
    const bc = parse(cs.borderTopColor);
    const border = bw > 0 && bc && bc[3] > 0 ? blend(bc, ownBg || parentBg) : null;
    const boundary = Math.max(ownBg ? ratio(ownBg, parentBg) : 0, border ? ratio(border, parentBg) : 0);
    const name = (el.getAttribute('aria-label') || el.innerText || el.getAttribute('title') || '').trim()
      || (el.tagName === 'INPUT' && el.closest('label') ? el.closest('label').innerText.trim() : '');
    const group = el.parentElement;
    const siblingsButtons = [...group.children].filter((c) => c.tagName === 'BUTTON');
    const groupBg = parse(getComputedStyle(group).backgroundColor);
    const segmented = el.tagName === 'BUTTON' && siblingsButtons.length >= 2 && siblingsButtons.length === group.children.length
      && siblingsButtons.every((b) => parseFloat(getComputedStyle(b).borderTopWidth) === 0)
      && !!(groupBg && groupBg[3] > 0);
    const iconOnly = !el.innerText.trim() && !!el.querySelector('svg');
    const iconColor = parse(cs.color);
    const iconRatio = iconOnly ? ratio(iconColor[3] < 1 ? blend(iconColor, ownBg || parentBg) : iconColor, ownBg || parentBg) : null;
    inter.push({
      tag: el.tagName.toLowerCase(),
      label: label(el),
      name,
      w: Math.round(r.width), h: Math.round(r.height),
      href: el.getAttribute('href'),
      hasBoundary: !!(ownBg || border),
      boundary: Math.round(boundary * 100) / 100,
      segmented,
      iconOnly,
      iconRatio: iconRatio && Math.round(iconRatio * 100) / 100,
      ariaPressed: el.getAttribute('aria-pressed'),
      ariaSelected: el.getAttribute('aria-selected'),
      role: el.getAttribute('role'),
      inNav: !!(nav && nav.contains(el)),
      ariaCurrent: el.getAttribute('aria-current'),
    });
  }

  // Kwoty łamane między wierszami (np. "1" w jednej linii, "416 zł" w następnej)
  const brokenAmounts = [];
  const amountRe = /[-+]?\d{1,3}(?:[ \u00a0]\d{3})*(?:,\d{2})?[ \u00a0]?(?:zł|€)/g;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    for (const mt of n.textContent.matchAll(amountRe)) {
      const range = document.createRange();
      range.setStart(n, mt.index);
      range.setEnd(n, mt.index + mt[0].length);
      const tops = new Set([...range.getClientRects()].filter((r) => r.width > 0).map((r) => Math.round(r.top)));
      if (tops.size > 1) brokenAmounts.push(`"${mt[0].trim()}" w ${tops.size} wierszach`);
    }
  }
  const headings = [...root.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) => ({ level: +h.tagName[1], text: h.innerText.trim().slice(0, 40) }));
  const content = [...root.querySelectorAll('*')].filter((e) => visible(e) && !(nav && nav.contains(e)) && e !== root);
  const contentBottom = Math.max(...content.map((e) => e.getBoundingClientRect().bottom));
  return {
    lang: document.documentElement.getAttribute('lang'),
    texts, inter, headings, brokenAmounts,
    rootW: R.width, rootH: R.height,
    scrollW: document.documentElement.scrollWidth,
    contentBottom: Math.round(contentBottom), navTop: nav ? Math.round(navTop) : null,
    leftover: document.body.innerHTML.includes('{{'),
  };
}

const results = [];
const add = (tc, m, variantDependent, status, details) => {
  results.push({
    tc, ekran: m.file.replace('.dc.html', ''), kierunek: m.direction, typ: m.kind,
    wariant: variantDependent ? `${m.dark ? 'ciemny' : 'jasny'} ${m.accent}` : 'wszystkie (niezależne od koloru)',
    domyslny: m.isDefault, status, szczegoly: details,
  });
};
const fmt = (list, f, max = 6) => list.slice(0, max).map(f).join('; ') + (list.length > max ? `; … (+${list.length - max})` : '');

const browser = await playwright.chromium.launch();
const seenLayout = new Set();
for (const m of manifest) {
  const page = await browser.newPage({ viewport: { width: m.w, height: m.h } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });
  await page.goto('file://' + path.resolve(renderDir, `${m.id}.html`));
  await page.evaluate(() => document.fonts.ready);
  const d = await page.evaluate(measure, m.kind);
  await page.screenshot({ path: path.join(outDir, 'zrzuty', `${m.id}.png`) });

  // --- Przypadki zależne od koloru (każdy wariant) ---
  const acc = m.accent.toUpperCase();
  const onAccent = (t) => t.bg === acc || t.color === acc;
  const neutral = d.texts.filter((t) => !t.logo && !onAccent(t));
  const lowText = neutral.filter((t) => t.ratio < t.need);
  add('TC-B-001', m, true, lowText.length ? 'Niezaliczony' : 'Zaliczony',
    lowText.length ? `${lowText.length}/${neutral.length} tekstów poniżej progu: ` + fmt(lowText, (t) => `"${t.text}" ${t.ratio}:1 (wym. ${t.need}) ${t.color} na ${t.bg}`)
      : `${neutral.length} tekstów, min. ${Math.min(...neutral.map((t) => t.ratio)).toFixed(2)}:1`);

  const primary = d.texts.filter((t) => !t.logo && onAccent(t));
  const lowPrimary = primary.filter((t) => t.ratio < t.need);
  add('TC-B-002', m, true, primary.length === 0 ? 'Nie dotyczy' : (lowPrimary.length ? 'Niezaliczony' : 'Zaliczony'),
    primary.length === 0 ? 'brak tekstu w kolorze akcentu / na akcencie'
      : lowPrimary.length ? `${lowPrimary.length}/${primary.length}: ` + fmt(lowPrimary, (t) => `"${t.text}" ${t.ratio}:1 (wym. ${t.need}) ${t.color} na ${t.bg}`) : `${primary.length} elementów akcentu, min. ${Math.min(...primary.map((t) => t.ratio)).toFixed(2)}:1`);

  const inputs = d.inter.filter((i) => i.tag === 'input');
  const lowInput = inputs.filter((i) => i.boundary < 3);
  add('TC-B-003', m, true, inputs.length === 0 ? 'Nie dotyczy' : (lowInput.length ? 'Niezaliczony' : 'Zaliczony'),
    inputs.length === 0 ? 'brak pól formularza'
      : lowInput.length ? fmt(lowInput, (i) => `pole "${i.label}" obrys ${i.boundary}:1 (wym. 3)`) : fmt(inputs, (i) => `pole "${i.label}" obrys ${i.boundary}:1`));

  const icons = d.inter.filter((i) => i.iconOnly);
  const lowIcons = icons.filter((i) => i.iconRatio < 3);
  add('TC-B-005', m, true, icons.length === 0 ? 'Nie dotyczy' : (lowIcons.length ? 'Niezaliczony' : 'Zaliczony'),
    icons.length === 0 ? 'brak przycisków z samą ikoną'
      : lowIcons.length ? fmt(lowIcons, (i) => `"${i.label}" ikona ${i.iconRatio}:1`) : `${icons.length} ikon, min. ${Math.min(...icons.map((i) => i.iconRatio)).toFixed(2)}:1`);

  const secondary = d.inter.filter((i) => i.tag === 'button' && !i.segmented && i.hasBoundary);
  const flat = secondary.filter((i) => i.boundary < 3);
  add('TC-B-006', m, true, secondary.length === 0 ? 'Nie dotyczy' : (flat.length ? 'Niezaliczony' : 'Zaliczony'),
    secondary.length === 0 ? 'brak przycisków z tłem/obrysem'
      : flat.length ? `${flat.length}/${secondary.length} przycisków słabo odcina się od tła (< 3:1): ` + fmt(flat, (i) => `"${i.label}" ${i.boundary}:1`) : `${secondary.length} przycisków, min. ${Math.min(...secondary.map((i) => i.boundary)).toFixed(2)}:1`);

  const amountRe = /[-+]?\d[\d\s]*,\d{2}\s?(zł|€)|[-+]?\d[\d\s]*\s?zł/;
  const amounts = d.texts.filter((t) => amountRe.test(t.text));
  const pal = m.palette;
  const colored = amounts.filter((t) => [pal.pos, pal.neg].map((x) => x.toUpperCase()).includes(t.color));
  const noSign = colored.filter((t) => !/^[-+]/.test(t.text.trim()));
  const posNeg = [pal.pos, pal.neg];
  add('TC-B-004', m, true, colored.length === 0 ? 'Nie dotyczy' : (noSign.length ? 'Niezaliczony' : 'Zaliczony'),
    colored.length === 0 ? 'brak kwot w kolorach plus/minus'
      : noSign.length ? `kwoty barwione bez znaku: ${fmt(noSign, (t) => `"${t.text}"`)}` : `${colored.length} kwot barwionych, każda ze znakiem +/−; plus/minus ${posNeg.join(' / ')}`);

  // --- Przypadki niezależne od koloru (raz na ekran) ---
  if (!seenLayout.has(m.file)) {
    seenLayout.add(m.file);
    const isPhone = m.kind === 'telefon';
    const minTarget = isPhone ? 44 : 24;
    const small = d.inter.filter((i) => i.w < minTarget || i.h < minTarget);
    add('TC-B-010', m, false, small.length ? 'Niezaliczony' : 'Zaliczony',
      `próg ${minTarget}×${minTarget}px (${isPhone ? 'Apple HIG / WCAG 2.5.5' : 'WCAG 2.5.8'}); ` + (small.length ? `${small.length}/${d.inter.length} za małych: ` + fmt(small, (i) => `${i.tag} "${i.label}" ${i.w}×${i.h}`) : `${d.inter.length} celów OK`));

    const noName = d.inter.filter((i) => !i.name);
    add('TC-B-011', m, false, noName.length ? 'Niezaliczony' : 'Zaliczony',
      noName.length ? fmt(noName, (i) => `${i.tag} bez nazwy`) : `${d.inter.length} kontrolek ma nazwę dostępną`);

    const seg = d.inter.filter((i) => i.segmented);
    const segBad = seg.filter((i) => i.ariaPressed == null && i.ariaSelected == null);
    add('TC-B-012', m, false, seg.length === 0 ? 'Nie dotyczy' : (segBad.length ? 'Niezaliczony' : 'Zaliczony'),
      seg.length === 0 ? 'brak przełącznika segmentowego' : segBad.length ? `${segBad.length} przycisków przełącznika bez aria-pressed/aria-selected: ` + fmt(segBad, (i) => `"${i.label}"`) : 'stan zakomunikowany');

    const navLinks = d.inter.filter((i) => i.inNav);
    const current = navLinks.filter((i) => i.ariaCurrent);
    add('TC-B-013', m, false, navLinks.length === 0 ? 'Nie dotyczy' : (current.length === 1 ? 'Zaliczony' : 'Niezaliczony'),
      navLinks.length === 0 ? 'brak nawigacji' : `${navLinks.length} pozycji nawigacji, z aria-current: ${current.length} (aktywna pozycja oznaczona tylko kolorem)`);

    const h1 = d.headings.filter((h) => h.level === 1);
    let skip = false;
    d.headings.reduce((prev, h) => { if (h.level > prev + 1) skip = true; return h.level; }, 0);
    add('TC-B-014', m, false, h1.length === 1 && !skip ? 'Zaliczony' : 'Niezaliczony',
      `nagłówki: ${d.headings.map((h) => `h${h.level} "${h.text}"`).join(', ') || 'brak'}${h1.length !== 1 ? ` — h1: ${h1.length}` : ''}${skip ? ' — przeskok poziomu' : ''}`);

    add('TC-B-015', m, false, d.lang === 'pl' ? 'Zaliczony' : 'Niezaliczony', `lang="${d.lang}"`);

    const dead = d.inter.filter((i) => i.tag === 'a' && (!i.href || i.href === '#'));
    const noAction = d.inter.filter((i) => i.tag === 'button');
    add('TC-B-016', m, false, dead.length ? 'Niezaliczony' : 'Zaliczony',
      `${dead.length} linków prowadzi do "#", ${noAction.length} przycisków bez akcji (prototyp statyczny)` + (dead.length ? ': ' + fmt(dead, (i) => `"${i.label}"`) : ''));

    const outside = d.texts.filter((t) => t.outside || t.overflowX);
    add('TC-B-017', m, false, outside.length || d.scrollW > m.w ? 'Niezaliczony' : 'Zaliczony',
      outside.length ? 'poza ekranem: ' + fmt(outside, (t) => `"${t.text}"`) : 'cała treść mieści się w ramce');

    const under = d.texts.filter((t) => t.underNav);
    add('TC-B-018', m, false, d.navTop == null || !isPhone ? 'Nie dotyczy' : (under.length ? 'Niezaliczony' : 'Zaliczony'),
      d.navTop == null || !isPhone ? 'brak dolnej nawigacji (dotyczy ekranów telefonu)' : under.length ? 'pod nawigacją: ' + fmt(under, (t) => `"${t.text}"`) : `dół treści ${d.contentBottom}px, nawigacja od ${d.navTop}px`);

    const ell = d.texts.filter((t) => t.ellipsis);
    add('TC-B-019', m, false, ell.length ? 'Niezaliczony' : 'Zaliczony',
      ell.length ? 'ucięte wielokropkiem: ' + fmt(ell, (t) => `"${t.text}"`) : 'żaden tekst nie jest ucięty');

    const tiny = d.texts.filter((t) => t.size < 12);
    add('TC-B-020', m, false, tiny.length ? 'Niezaliczony' : 'Zaliczony',
      tiny.length ? `${tiny.length} tekstów < 12px: ` + fmt([...new Map(tiny.map((t) => [t.text, t])).values()], (t) => `"${t.text}" ${t.size}px`) : 'wszystkie teksty ≥ 12px');

    add('TC-B-021', m, false, errors.length || d.leftover || m.unresolved.length ? 'Niezaliczony' : 'Zaliczony',
      errors.length ? errors.slice(0, 3).join(' | ') : (m.unresolved.length ? `nierozwiązane pola: ${m.unresolved.join(', ')}` : 'render bez błędów i bez pustych pól {{…}}'));

    add('TC-B-023', m, false, d.brokenAmounts.length ? 'Niezaliczony' : 'Zaliczony',
      d.brokenAmounts.length ? 'kwota złamana między wierszami: ' + d.brokenAmounts.join('; ') : 'żadna kwota nie jest łamana');

    // Klawiatura: przejście Tabem przez wszystkie kontrolki, widoczny wskaźnik fokusu.
    const tabStops = [];
    for (let i = 0; i < d.inter.length + 2; i++) {
      await page.keyboard.press('Tab');
      const info = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        return { label: (el.getAttribute('aria-label') || el.innerText || el.tagName).trim().slice(0, 30), outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 };
      });
      if (!info) break;
      if (tabStops.length && tabStops[0].label === info.label && tabStops.length >= d.inter.length) break;
      tabStops.push(info);
    }
    const noRing = tabStops.filter((s) => !s.outline);
    add('TC-B-022', m, false, tabStops.length >= d.inter.length && !noRing.length ? 'Zaliczony' : 'Niezaliczony',
      `${Math.min(tabStops.length, d.inter.length)}/${d.inter.length} kontrolek osiągalnych Tabem; bez widocznego fokusu: ${noRing.length}`);
  }
  await page.close();
}

// --- Przypadki responsywności i powiększenia tekstu (ekrany telefonu, raz na ekran) ---
const phones = manifest.filter((m) => m.kind === 'telefon' && m.isDefault);
const desktops = manifest.filter((m) => m.kind === 'desktop' && m.isDefault);
async function layoutProbe(m, { width, textScale }) {
  const page = await browser.newPage({ viewport: { width, height: m.h } });
  await page.goto('file://' + path.resolve(renderDir, `${m.id}.html`));
  await page.evaluate(() => document.fonts.ready);
  const r = await page.evaluate(({ width, textScale, fixedW }) => {
    const root = document.body.firstElementChild;
    if (fixedW) root.style.width = width + 'px';
    if (textScale !== 1) {
      for (const el of root.querySelectorAll('*')) {
        const fs = el.style.fontSize;
        if (fs && fs.endsWith('px')) el.style.fontSize = (parseFloat(fs) * textScale) + 'px';
      }
      root.style.fontSize = (parseFloat(root.style.fontSize || 15) * textScale) + 'px';
    }
    const R = root.getBoundingClientRect();
    const nav = root.querySelector('nav');
    const navTop = nav ? nav.getBoundingClientRect().top : R.bottom;
    const bad = [];
    for (const el of root.querySelectorAll('*')) {
      const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      if (!own) continue;
      const rr = el.getBoundingClientRect();
      if (rr.width === 0) continue;
      const cs = getComputedStyle(el);
      const clippedX = rr.right > R.right + 0.5 || (cs.textOverflow === 'ellipsis' && el.scrollWidth > el.clientWidth + 1);
      const hidden = !(nav && nav.contains(el)) && rr.bottom > navTop + 0.5;
      if (clippedX || hidden) bad.push(`"${el.textContent.trim().slice(0, 30)}"${hidden ? ' (pod nawigacją/poza ekranem)' : ' (ucięty w poziomie)'}`);
    }
    return { bad, hScroll: document.documentElement.scrollWidth > window.innerWidth };
  }, { width, textScale, fixedW: m.kind === 'telefon' });
  await page.close();
  return r;
}
for (const m of phones) {
  for (const [tc, opts, opis] of [
    ['TC-B-030', { width: 360, textScale: 1 }, 'szerokość 360 px (typowy Android)'],
    ['TC-B-031', { width: 320, textScale: 1 }, 'szerokość 320 px (iPhone SE 1. gen.)'],
    ['TC-B-032', { width: 390, textScale: 1.3 }, 'tekst powiększony do 130% (Dynamic Type / ustawienia czcionki)'],
    ['TC-B-033', { width: 390, textScale: 2 }, 'tekst powiększony do 200% (WCAG 1.4.4)'],
  ]) {
    const r = await layoutProbe(m, opts);
    add(tc, m, false, r.bad.length || r.hScroll ? 'Niezaliczony' : 'Zaliczony',
      `${opis}: ` + (r.bad.length ? `${r.bad.length} problemów: ` + fmt(r.bad, (x) => x, 5) : 'bez ucięć') + (r.hScroll ? '; poziomy scroll' : ''));
  }
}
for (const m of desktops) {
  for (const [tc, width, opis] of [['TC-B-034', 1024, 'okno 1024 px (laptop/tablet poziomo)'], ['TC-B-035', 1440, 'okno 1440 px (duży monitor)']]) {
    const page = await browser.newPage({ viewport: { width, height: m.h } });
    await page.goto('file://' + path.resolve(renderDir, `${m.id}.html`));
    const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, w: window.innerWidth, rootW: document.body.firstElementChild.getBoundingClientRect().width }));
    await page.close();
    const fail = r.sw > r.w || (width > 1280 && r.rootW < width);
    add(tc, m, false, fail ? 'Niezaliczony' : 'Zaliczony',
      `${opis}: układ ma sztywne ${r.rootW}px` + (r.sw > r.w ? `, poziomy scroll (${r.sw}px > ${r.w}px)` : '') + (width > 1280 && r.rootW < width ? `, ${width - r.rootW}px pustego pasa po prawej` : ''));
  }
}
await browser.close();

fs.writeFileSync(path.join(outDir, 'wyniki-B.json'), JSON.stringify(results, null, 2));
const csvEsc = (s) => `"${String(s).replace(/"/g, '""')}"`;
const header = ['lp', 'tc', 'ekran', 'kierunek', 'typ', 'wariant', 'domyslny', 'status', 'szczegoly'];
const csv = [header.join(',')].concat(results.map((r, i) => [i + 1, r.tc, r.ekran, r.kierunek, r.typ, r.wariant, r.domyslny ? 'tak' : 'nie', r.status, r.szczegoly].map(csvEsc).join(','))).join('\n');
fs.writeFileSync(path.join(outDir, 'wyniki-B.csv'), '﻿' + csv + '\n');

const by = {};
for (const r of results) { by[r.tc] ??= { Zaliczony: 0, Niezaliczony: 0, 'Nie dotyczy': 0 }; by[r.tc][r.status]++; }
console.log(`Wykonano ${results.length} przypadków.`);
console.table(by);
