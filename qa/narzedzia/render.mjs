// Renderuje ekrany z kanwy "marlik - kierunki wizualne" (*.dc.html) do zwykłych stron HTML,
// osobno dla każdej kombinacji motywu (jasny/ciemny) i koloru akcentu zadeklarowanego w data-props.
// Wartości kolorów liczy własna funkcja renderVals() danego ekranu, więc wynik odpowiada temu,
// co pokazuje kanwa po przełączeniu suwaków "Motyw".
//
// Użycie: node render.mjs <katalog project/> <katalog wyjściowy> <ścieżka do fonts/all.css>

import fs from 'node:fs';
import path from 'node:path';

const [projectDir, outDir, fontsCss] = process.argv.slice(2);
if (!projectDir || !outDir || !fontsCss) {
  console.error('Użycie: node render.mjs <project/> <out/> <fonts/all.css>');
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: true });

const canvas = JSON.parse(fs.readFileSync(path.join(projectDir, 'canvas.json'), 'utf8'));

class DCLogic {
  constructor(props) { this.props = props; }
}

function variantsFor(propsDecl) {
  const darkDefault = propsDecl.dark?.default ?? false;
  const accents = propsDecl.accent?.options ?? [propsDecl.accent?.default];
  const out = [];
  for (const dark of [false, true]) {
    for (const accent of accents) {
      out.push({
        dark,
        accent,
        isDefault: dark === darkDefault && accent === propsDecl.accent?.default,
      });
    }
  }
  return out;
}

const manifest = [];
for (const file of canvas.order) {
  const src = fs.readFileSync(path.join(projectDir, file), 'utf8');
  const lang = (src.match(/<html[^>]*lang="([^"]+)"/) || [])[1] || null;
  const title = (src.match(/<title>([^<]*)<\/title>/) || [])[1] || file;
  const propsDecl = JSON.parse(src.match(/data-props='([^']*)'/)[1]);
  const script = src.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/)[1];
  const Component = new Function('DCLogic', `${script}\nreturn Component;`)(DCLogic);

  const body = src.split('<x-dc>')[1].split('</x-dc>')[0];
  const helmet = (body.match(/<helmet>([\s\S]*?)<\/helmet>/) || [, ''])[1]
    .replace(/<link[^>]*fonts\.googleapis\.com[^>]*>/g, '');
  const markup = body.replace(/<helmet>[\s\S]*?<\/helmet>/, '').trim();

  const board = canvas.boards[file];
  for (const v of variantsFor(propsDecl)) {
    const vals = new Component({ dark: v.dark, accent: v.accent }).renderVals();
    const unresolved = [];
    const html = markup.replace(/\{\{\s*([\w.]+)\s*\}\}/g, (m, key) => {
      const val = key.split('.').reduce((o, k) => (o == null ? undefined : o[k]), vals);
      if (val === undefined) { unresolved.push(key); return ''; }
      return String(val);
    });
    const id = `${file.replace('.dc.html', '')}__${v.dark ? 'ciemny' : 'jasny'}__${v.accent.slice(1)}`;
    const page = `<!doctype html>
<html${lang ? ` lang="${lang}"` : ''}>
<head>
<meta charset="utf-8">
<title>${title}</title>
<link rel="stylesheet" href="${path.relative(outDir, fontsCss)}">
${helmet}
</head>
<body>
${html}
</body>
</html>
`;
    fs.writeFileSync(path.join(outDir, `${id}.html`), page);
    manifest.push({
      id,
      file,
      boardTitle: board.title,
      w: board.w,
      h: board.h,
      kind: board.w <= 430 ? 'telefon' : (file.includes('System') ? 'system' : 'desktop'),
      direction: board.title.split(' · ')[0],
      dark: v.dark,
      accent: v.accent,
      isDefault: v.isDefault,
      unresolved,
      palette: vals.c,
    });
  }
}
fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`Wyrenderowano ${manifest.length} wariantów z ${canvas.order.length} ekranów.`);
