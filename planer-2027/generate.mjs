// Erzeugt den „Planer 2027“ als druckbare und iPad-taugliche PDFs, eine Ausgabe pro Bundesland.
// Aufruf: node planer-2027/generate.mjs        (alle Ausgaben)
//         node planer-2027/generate.mjs BY     (nur Bayern, zum schnellen Testen)
import { createRequire } from "node:module";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const DIST = join(ROOT, "dist");
const BUILD = join(ROOT, ".build");
const YEAR = 2027;

/* ---------------- Bundesländer und Feiertage ---------------- */
export const STATES = {
  DE: "Deutschland", BW: "Baden-Württemberg", BY: "Bayern", BE: "Berlin", BB: "Brandenburg", HB: "Bremen",
  HH: "Hamburg", HE: "Hessen", MV: "Mecklenburg-Vorpommern", NI: "Niedersachsen", NW: "Nordrhein-Westfalen",
  RP: "Rheinland-Pfalz", SL: "Saarland", SN: "Sachsen", ST: "Sachsen-Anhalt", SH: "Schleswig-Holstein", TH: "Thüringen"
};

const D = (y, m, d) => new Date(Date.UTC(y, m - 1, d));
const addDays = (dt, n) => new Date(dt.getTime() + n * 86400000);
const key = dt => dt.toISOString().slice(0, 10);

function easter(y) { // Gaußsche Osterformel (Meeus/Jones/Butcher)
  const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4;
  const f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
  return D(y, month, day);
}
function bussUndBettag(y) { // Mittwoch vor dem 23. November
  let dt = D(y, 11, 22);
  while (dt.getUTCDay() !== 3) dt = addDays(dt, -1);
  return dt;
}

// states: "ALL" oder Liste; partial: Länder, in denen der Tag nur regional gilt
export function holidays(y) {
  const E = easter(y);
  return [
    { d: D(y, 1, 1), n: "Neujahr", s: "ALL" },
    { d: D(y, 1, 6), n: "Heilige Drei Könige", s: ["BW", "BY", "ST"] },
    { d: D(y, 3, 8), n: "Internationaler Frauentag", s: ["BE", "MV"] },
    { d: addDays(E, -2), n: "Karfreitag", s: "ALL" },
    { d: E, n: "Ostersonntag", s: ["BB", "HE"] },
    { d: addDays(E, 1), n: "Ostermontag", s: "ALL" },
    { d: D(y, 5, 1), n: "Tag der Arbeit", s: "ALL" },
    { d: addDays(E, 39), n: "Christi Himmelfahrt", s: "ALL" },
    { d: addDays(E, 49), n: "Pfingstsonntag", s: ["BB", "HE"] },
    { d: addDays(E, 50), n: "Pfingstmontag", s: "ALL" },
    { d: addDays(E, 60), n: "Fronleichnam", s: ["BW", "BY", "HE", "NW", "RP", "SL"], partial: ["SN", "TH"] },
    { d: D(y, 8, 15), n: "Mariä Himmelfahrt", s: ["SL"], partial: ["BY"] },
    { d: D(y, 9, 20), n: "Weltkindertag", s: ["TH"] },
    { d: D(y, 10, 3), n: "Tag der Deutschen Einheit", s: "ALL" },
    { d: D(y, 10, 31), n: "Reformationstag", s: ["BB", "HB", "HH", "MV", "NI", "SN", "ST", "SH", "TH"] },
    { d: D(y, 11, 1), n: "Allerheiligen", s: ["BW", "BY", "NW", "RP", "SL"] },
    { d: bussUndBettag(y), n: "Buß- und Bettag", s: ["SN"] },
    { d: D(y, 12, 25), n: "1. Weihnachtstag", s: "ALL" },
    { d: D(y, 12, 26), n: "2. Weihnachtstag", s: "ALL" }
  ];
}

// Feiertage einer Ausgabe als Map datum → {n, partial}
function holidayMap(state) {
  const m = new Map();
  for (const h of holidays(YEAR)) {
    const full = h.s === "ALL" || h.s.includes(state);
    const part = !full && (h.partial || []).includes(state);
    if (full || part) m.set(key(h.d), { n: h.n, partial: part });
  }
  return m;
}

/* ---------------- Kalender-Helfer ---------------- */
const MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
const MON_SHORT = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
const DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"];
const DAYS_SHORT = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
const wd = dt => (dt.getUTCDay() + 6) % 7; // 0 = Montag
const daysIn = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate();
function isoWeek(dt) {
  const t = addDays(dt, 3 - wd(dt)); // Donnerstag derselben Woche
  const jan4 = D(t.getUTCFullYear(), 1, 4);
  return 1 + Math.round((t - addDays(jan4, -wd(jan4))) / (7 * 86400000));
}
const fmt = dt => `${dt.getUTCDate()}. ${MONTHS[dt.getUTCMonth()]}`;
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// Alle Montage der Wochen, die 2027 berühren (beginnt mit KW 53/2026)
function weekStarts() {
  const out = [];
  let m = addDays(D(YEAR, 1, 1), -wd(D(YEAR, 1, 1)));
  while (m.getUTCFullYear() <= YEAR) { out.push(m); m = addDays(m, 7); }
  return out;
}

/* ---------------- Stil ---------------- */
const font = (fam, w, file) => `@font-face{font-family:"${fam}";font-weight:${w};src:url("file://${join(ROOT, "fonts", file)}") format("truetype");}`;
const CSS = `
${font("Fraunces", 500, "Fraunces-500.ttf")}${font("Fraunces", 700, "Fraunces-700.ttf")}
${font("Figtree", 400, "Figtree-400.ttf")}${font("Figtree", 500, "Figtree-500.ttf")}${font("Figtree", 600, "Figtree-600.ttf")}${font("Figtree", 700, "Figtree-700.ttf")}
/* Papier-Planer: helle Flächen (tintensparend), Salbeigrün als Akzent, Beere für Feiertage */
:root{
  --ink:#24302b; --soft:#6d7a74; --line:#cfd8d3; --faint:#e6ece8; --tint:#f3f6f4;
  --sage:#4f7a68; --sage-soft:#e2ece7; --berry:#a33b5c; --berry-soft:#f6e5ea;
  --display:"Fraunces",Georgia,serif; --body:"Figtree",Arial,sans-serif;
}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:var(--body);color:var(--ink);font-size:9.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit;text-decoration:none}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:13mm 22mm 12mm 14mm;display:flex;flex-direction:column;gap:5mm}
.page:last-child{page-break-after:auto}
.tabs{position:absolute;top:13mm;right:0;width:11mm;display:flex;flex-direction:column;gap:1.2mm}
.tabs a{display:block;background:var(--faint);color:var(--soft);font-size:7pt;font-weight:600;text-align:center;padding:2.1mm 0;border-radius:2mm 0 0 2mm;letter-spacing:.02em}
.tabs a.on{background:var(--sage);color:#fff}
.tabs .sep{height:2mm}
h1,h2,h3{margin:0;font-family:var(--display);font-weight:700;letter-spacing:-.01em}
.head{display:flex;align-items:flex-end;justify-content:space-between;gap:6mm;border-bottom:.6mm solid var(--ink);padding-bottom:2.5mm}
.head h1{font-size:30pt;line-height:1}
.head .meta{font-size:8.5pt;color:var(--soft);text-align:right;line-height:1.35}
.eyebrow{font-size:7pt;text-transform:uppercase;letter-spacing:.12em;color:var(--soft);font-weight:600}
.lines,.dots{flex:1;position:relative;min-height:0}
svg.pat{position:absolute;inset:0;width:100%;height:100%}
.box{border:.3mm solid var(--line);border-radius:2mm;padding:2.5mm 3mm;display:flex;flex-direction:column;gap:1.5mm}
.hol{color:var(--berry);font-weight:600}
.hol.part{font-weight:500;font-style:italic}

/* Deckblatt */
.cover{justify-content:space-between;padding:22mm 22mm 18mm 18mm}
.cover .year{font-family:var(--display);font-size:150pt;line-height:.8;font-weight:700;letter-spacing:-.04em;color:var(--sage)}
.cover .title{font-family:var(--display);font-size:34pt;font-weight:500}
.cover .state{font-size:13pt;font-weight:600}
.cover .feat{display:grid;grid-template-columns:1fr 1fr;gap:2mm 8mm;font-size:9.5pt;color:var(--soft)}
.cover .name{border-bottom:.3mm solid var(--line);height:12mm;display:flex;align-items:flex-end;color:var(--soft);font-size:8pt;padding-bottom:1mm}

/* Jahresübersicht */
.yeargrid{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm 6mm}
.mini h3{font-size:11pt;margin-bottom:1.5mm}
.mini table{width:100%;border-collapse:collapse;font-size:7.3pt;text-align:center;font-variant-numeric:tabular-nums}
.mini th{color:var(--soft);font-weight:600;padding:.6mm 0}
.mini td{padding:.7mm 0}
.mini td.we{color:var(--soft)}
.mini td.h{background:var(--berry-soft);color:var(--berry);font-weight:700;border-radius:1mm}
.mini td.p{background:var(--berry-soft);color:var(--berry);border-radius:1mm}
.hlist{columns:2;column-gap:8mm;font-size:8pt;line-height:1.55}
.hlist div{break-inside:avoid;display:flex;gap:2mm}
.hlist b{font-variant-numeric:tabular-nums;min-width:19mm;font-weight:600}

/* Monat */
.month{display:grid;grid-template-columns:7mm repeat(7,1fr);border-top:.3mm solid var(--line);border-left:.3mm solid var(--line)}
.month > div{border-right:.3mm solid var(--line);border-bottom:.3mm solid var(--line)}
.month .dh{font-size:7.5pt;font-weight:600;color:var(--soft);text-align:center;padding:1.5mm 0;background:var(--tint)}
.month .kw{font-size:6.5pt;color:var(--soft);writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;background:var(--tint)}
.month .c{height:var(--ch);padding:1.5mm;display:flex;flex-direction:column;gap:.5mm}
.month .c .n{font-family:var(--display);font-size:12pt;font-weight:500;line-height:1}
.month .c.we{background:var(--tint)}
.month .c.out .n{color:var(--line)}
.month .c .hn{font-size:6.6pt;line-height:1.15}
.month .c.h{background:var(--berry-soft)}
.month .c.h .n{color:var(--berry)}

/* Woche */
.week{flex:1;display:grid;grid-template-columns:1fr 52mm;gap:5mm;min-height:0}
.days{display:grid;grid-template-rows:repeat(5,1fr) .8fr .8fr;gap:2mm;min-height:0}
.day{border:.3mm solid var(--line);border-radius:2mm;padding:2mm 3mm;display:flex;flex-direction:column;gap:1mm;position:relative;overflow:hidden}
.day svg.pat{top:8mm;height:auto;bottom:0}
.day .t{position:relative}
.day .t{display:flex;align-items:baseline;gap:2mm;background:#fff;align-self:flex-start;padding-right:2mm}
.day .t b{font-family:var(--display);font-size:13pt;font-weight:700;line-height:1}
.day .t span{font-size:8pt;color:var(--soft);font-weight:600}
.day.we{background-color:var(--tint)}
.day.we .t{background:var(--tint)}
.day.other .t b{color:var(--soft)}
.side{display:flex;flex-direction:column;gap:4mm;min-height:0}
.check{display:flex;flex-direction:column}
.check div{display:flex;align-items:center;gap:2mm;height:7mm;border-bottom:.3mm solid var(--faint)}
.check div::before{content:"";width:3.2mm;height:3.2mm;border:.3mm solid var(--soft);border-radius:.8mm;flex:none}
.prio div::before{border-radius:50%;border-color:var(--sage);border-width:.5mm}

/* Tracker und Budget */
table.grid{width:100%;border-collapse:collapse;font-size:7.5pt;font-variant-numeric:tabular-nums}
table.grid th,table.grid td{border:.3mm solid var(--line);text-align:center;padding:0}
table.grid th{font-weight:600;color:var(--soft);height:6mm;background:var(--tint)}
table.grid th.we{color:var(--sage)}
table.grid td{height:7.4mm}
table.grid td.name,table.grid th.name{width:34mm;text-align:left;padding-left:2mm}
table.grid td.we{background:var(--tint)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.ledger{width:100%;border-collapse:collapse;font-size:8.5pt}
.ledger th{text-align:left;font-weight:600;color:var(--soft);border-bottom:.5mm solid var(--ink);padding:1.5mm 0;font-size:7.5pt;text-transform:uppercase;letter-spacing:.08em}
.ledger th:last-child,.ledger td:last-child{text-align:right;width:24mm}
.ledger td{height:7.2mm;border-bottom:.3mm solid var(--line);color:var(--soft);font-size:8pt}
.ledger tr.sum td{border-bottom:.6mm solid var(--ink);color:var(--ink);font-weight:700}
.sumbox{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.sumbox .box{min-height:20mm}
.areas{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:4mm;flex:1}
.areas .box h3{font-size:12pt}
.foot{font-size:7pt;color:var(--soft);display:flex;justify-content:space-between}
`;

/* ---------------- Seiten ---------------- */
// Linien und Punktraster als Vektor-SVG (CSS-Verläufe würden im PDF als Bild gespeichert)
const MM = 3.7795;
let patId = 0;
function pat(kind, color = "#cfd8d3") {
  const id = "p" + (++patId);
  const body = kind === "dots"
    ? `<pattern id="${id}" width="${5 * MM}" height="${5 * MM}" patternUnits="userSpaceOnUse"><circle cx="${2.5 * MM}" cy="${2.5 * MM}" r="${0.35 * MM}" fill="${color}"/></pattern>`
    : `<pattern id="${id}" width="10" height="${7.5 * MM}" patternUnits="userSpaceOnUse"><rect y="${7.5 * MM - 0.75}" width="10" height="0.75" fill="${color}"/></pattern>`;
  return `<svg class="pat" aria-hidden="true"><defs>${body}</defs><rect width="100%" height="100%" fill="url(#${id})"/></svg>`;
}
const LINES = () => `<div class="lines">${pat("lines")}</div>`;
const DOTS = () => `<div class="dots">${pat("dots")}</div>`;
function tabs(active) {
  return `<nav class="tabs"><a href="#jahr" class="${active === "jahr" ? "on" : ""}">Jahr</a><div class="sep"></div>${MON_SHORT.map((m, i) =>
    `<a href="#m${i + 1}" class="${active === i + 1 ? "on" : ""}">${m}</a>`).join("")}<div class="sep"></div><a href="#ziele" class="${active === "ziele" ? "on" : ""}">Ziele</a></nav>`;
}

function cover(state) {
  return `<section class="page cover">
    <div><div class="eyebrow">Jahresplaner</div></div>
    <div style="display:flex;flex-direction:column;gap:6mm">
      <div class="year">${YEAR}</div>
      <div class="title">Mein Jahr, gut geplant.</div>
      <div class="state">${state === "DE" ? "Mit allen bundesweiten Feiertagen" : `Mit allen Feiertagen in ${esc(STATES[state])}`}</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:8mm">
      <div class="feat"><span>Jahresübersicht und Jahresziele</span><span>12 Monatsseiten</span><span>${weekStarts().length} Wochenseiten mit Kalenderwochen</span><span>Gewohnheiten-Tracker und Budget pro Monat</span></div>
      <div class="name">Dieser Planer gehört</div>
    </div>
  </section>`;
}

function miniMonth(m, hm) {
  const first = D(YEAR, m, 1), n = daysIn(YEAR, m), off = wd(first);
  const cells = [];
  for (let i = 0; i < off; i++) cells.push("<td></td>");
  for (let d = 1; d <= n; d++) {
    const dt = D(YEAR, m, d), h = hm.get(key(dt)), w = wd(dt);
    const cls = h ? (h.partial ? "p" : "h") : w > 4 ? "we" : "";
    cells.push(`<td class="${cls}">${d}</td>`);
  }
  while (cells.length % 7) cells.push("<td></td>");
  const rows = [];
  for (let i = 0; i < cells.length; i += 7) rows.push(`<tr>${cells.slice(i, i + 7).join("")}</tr>`);
  return `<a class="mini" href="#m${m}"><h3>${MONTHS[m - 1]}</h3><table><tr>${DAYS_SHORT.map(d => `<th>${d}</th>`).join("")}</tr>${rows.join("")}</table></a>`;
}

function yearPage(state, hm) {
  const list = [...hm.entries()].sort().map(([k, h]) => {
    const dt = new Date(k + "T00:00:00Z");
    return `<div><b>${DAYS_SHORT[wd(dt)]}, ${dt.getUTCDate()}.${dt.getUTCMonth() + 1}.</b><span class="${h.partial ? "hol part" : ""}">${esc(h.n)}${h.partial ? " (regional)" : ""}</span></div>`;
  }).join("");
  return `<section class="page" id="jahr">${tabs("jahr")}
    <div class="head"><h1>${YEAR}</h1><div class="meta">Jahresübersicht<br>${esc(STATES[state])}</div></div>
    <div class="yeargrid">${Array.from({ length: 12 }, (_, i) => miniMonth(i + 1, hm)).join("")}</div>
    <div class="box"><div class="eyebrow">Feiertage ${state === "DE" ? "(bundesweit)" : "in " + esc(STATES[state])}</div><div class="hlist">${list}</div></div>
    ${noteRegional(state)}
  </section>`;
}

function noteRegional(state) {
  const notes = {
    BY: "Mariä Himmelfahrt gilt nur in Gemeinden mit überwiegend katholischer Bevölkerung, in Augsburg ist zusätzlich am 8. August Friedensfest.",
    SN: "Fronleichnam gilt nur in einigen Gemeinden im Landkreis Bautzen.",
    TH: "Fronleichnam gilt nur in einigen Gemeinden im Eichsfeld und im Wartburgkreis."
  };
  return notes[state] ? `<p class="foot"><span>Regional: ${notes[state]}</span></p>` : "";
}

function goalsPage() {
  const areas = ["Gesundheit", "Finanzen", "Arbeit & Schule", "Familie & Freunde", "Freizeit & Reisen", "Lernen & Neues"];
  return `<section class="page" id="ziele">${tabs("ziele")}
    <div class="head"><h1>Ziele ${YEAR}</h1><div class="meta">Was soll am Ende<br>des Jahres anders sein?</div></div>
    <div class="box" style="height:34mm"><div class="eyebrow">Mein Motto für ${YEAR}</div></div>
    <div class="areas">${areas.map(a => `<div class="box"><h3>${a}</h3>${LINES()}</div>`).join("")}</div>
  </section>`;
}

function monthPage(m, state, hm) {
  const first = D(YEAR, m, 1), n = daysIn(YEAR, m), off = wd(first);
  const total = Math.ceil((off + n) / 7) * 7, rows = total / 7;
  let start = addDays(first, -off);
  const cells = [`<div class="dh">KW</div>`, ...DAYS_SHORT.map(d => `<div class="dh">${d}</div>`)];
  for (let r = 0; r < rows; r++) {
    cells.push(`<div class="kw">${isoWeek(addDays(start, r * 7))}</div>`);
    for (let c = 0; c < 7; c++) {
      const dt = addDays(start, r * 7 + c), inM = dt.getUTCMonth() === m - 1, h = inM && hm.get(key(dt));
      const cls = ["c", c > 4 ? "we" : "", !inM ? "out" : "", h ? "h" : ""].join(" ");
      cells.push(`<div class="${cls}"><span class="n">${dt.getUTCDate()}</span>${h ? `<span class="hn hol ${h.partial ? "part" : ""}">${esc(h.n)}</span>` : ""}</div>`);
    }
  }
  return `<section class="page" id="m${m}">${tabs(m)}
    <div class="head"><h1>${MONTHS[m - 1]}</h1><div class="meta">${YEAR}<br>${esc(STATES[state])}</div></div>
    <div class="month" style="--ch:${rows === 6 ? 27 : 32}mm">${cells.join("")}</div>
    <div class="split" style="flex:1;min-height:0">
      <div class="box"><div class="eyebrow">Wichtig diesen Monat</div><div class="check">${"<div></div>".repeat(rows === 6 ? 5 : 7)}</div></div>
      <div class="box"><div class="eyebrow">Notizen</div>${LINES()}</div>
    </div>
  </section>`;
}

function weekPage(mon, active, hm) {
  const sun = addDays(mon, 6), kw = isoWeek(mon);
  const range = mon.getUTCMonth() === sun.getUTCMonth()
    ? `${mon.getUTCDate()}.–${fmt(sun)}` : `${fmt(mon)} – ${fmt(sun)}`;
  const days = Array.from({ length: 7 }, (_, i) => {
    const dt = addDays(mon, i), h = dt.getUTCFullYear() === YEAR && hm.get(key(dt));
    const cls = ["day", i > 4 ? "we" : "", dt.getUTCFullYear() !== YEAR ? "other" : ""].join(" ");
    return `<div class="${cls}">${pat("lines", "#e6ece8")}<div class="t"><b>${dt.getUTCDate()}</b><span>${DAYS[i]}</span>${h ? `<span class="hol ${h.partial ? "part" : ""}">${esc(h.n)}</span>` : ""}</div></div>`;
  }).join("");
  return `<section class="page">${tabs(active)}
    <div class="head"><h1>KW ${kw}</h1><div class="meta">${range} ${sun.getUTCFullYear()}</div></div>
    <div class="week">
      <div class="days">${days}</div>
      <div class="side">
        <div class="box"><div class="eyebrow">Top 3 der Woche</div><div class="check prio">${"<div></div>".repeat(3)}</div></div>
        <div class="box"><div class="eyebrow">To-dos</div><div class="check">${"<div></div>".repeat(11)}</div></div>
        <div class="box" style="flex:1"><div class="eyebrow">Notizen</div>${DOTS()}</div>
      </div>
    </div>
  </section>`;
}

function habitPage(m) {
  const n = daysIn(YEAR, m);
  const head = Array.from({ length: n }, (_, i) => { const w = wd(D(YEAR, m, i + 1)); return `<th class="${w > 4 ? "we" : ""}">${i + 1}</th>`; }).join("");
  const row = `<tr><td class="name"></td>${Array.from({ length: n }, (_, i) => `<td class="${wd(D(YEAR, m, i + 1)) > 4 ? "we" : ""}"></td>`).join("")}</tr>`;
  return `<section class="page">${tabs(m)}
    <div class="head"><h1>Gewohnheiten</h1><div class="meta">${MONTHS[m - 1]} ${YEAR}<br>Abhaken, was du geschafft hast</div></div>
    <table class="grid"><tr><th class="name">Gewohnheit</th>${head}</tr>${row.repeat(14)}</table>
    <div class="split" style="flex:1">
      <div class="box"><div class="eyebrow">Was lief gut?</div>${LINES()}</div>
      <div class="box"><div class="eyebrow">Was mache ich nächsten Monat anders?</div>${LINES()}</div>
    </div>
  </section>`;
}

function budgetPage(m) {
  const ledger = (title, rows) => `<table class="ledger"><tr><th>${title}</th><th>Betrag</th></tr>${rows.map(r => `<tr><td>${r}</td><td></td></tr>`).join("")}<tr class="sum"><td>Summe</td><td>€</td></tr></table>`;
  return `<section class="page">${tabs(m)}
    <div class="head"><h1>Budget</h1><div class="meta">${MONTHS[m - 1]} ${YEAR}</div></div>
    <div class="sumbox">
      <div class="box"><div class="eyebrow">Einnahmen</div></div>
      <div class="box"><div class="eyebrow">Ausgaben</div></div>
      <div class="box"><div class="eyebrow">Gespart</div></div>
    </div>
    <div class="split">
      ${ledger("Einnahmen", ["Lohn / Gehalt / Taschengeld", "Nebenjob", "Sonstiges", ""])}
      ${ledger("Fixkosten", ["Miete / Wohnen", "Strom & Internet", "Handy", "Versicherungen", "Abos & Streaming", ""])}
    </div>
    ${ledger("Variable Ausgaben", ["Lebensmittel", "Essen gehen & Lieferdienst", "Mobilität", "Kleidung", "Freizeit", "Geschenke", "", "", ""])}
    <div class="box" style="flex:1"><div class="eyebrow">Sparziel und Notizen</div>${LINES()}</div>
  </section>`;
}

export function buildHtml(state) {
  const hm = holidayMap(state);
  const weeks = weekStarts();
  const parts = [cover(state), yearPage(state, hm), goalsPage()];
  for (let m = 1; m <= 12; m++) {
    parts.push(monthPage(m, state, hm));
    for (const w of weeks) {
      const home = w.getUTCFullYear() < YEAR ? 1 : w.getUTCMonth() + 1;
      if (home === m) parts.push(weekPage(w, m, hm));
    }
    parts.push(habitPage(m), budgetPage(m));
  }
  return `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Planer ${YEAR} – ${esc(STATES[state])}</title><style>${CSS}</style></head><body>${parts.join("")}</body></html>`;
}

/* ---------------- Gratis-Probe: Feiertagstabelle aller Länder ---------------- */
export function buildSampleHtml() {
  const codes = Object.keys(STATES).filter(k => k !== "DE");
  const rows = holidays(YEAR).map(h => {
    const dt = h.d;
    return `<tr><td class="name"><b>${DAYS_SHORT[wd(dt)]}, ${dt.getUTCDate()}.${dt.getUTCMonth() + 1}.</b> ${esc(h.n)}</td>${codes.map(c => {
      const full = h.s === "ALL" || h.s.includes(c), part = !full && (h.partial || []).includes(c);
      return `<td style="${full ? "background:var(--berry-soft);color:var(--berry);font-weight:700" : part ? "color:var(--berry)" : ""}">${full ? "●" : part ? "◐" : ""}</td>`;
    }).join("")}</tr>`;
  }).join("");
  const hm = holidayMap("DE");
  return `<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Feiertage ${YEAR}</title><style>${CSS}
    .ft td.name{width:62mm;font-size:8pt} .ft td{height:7.6mm;font-size:9pt} .ft th{font-size:7pt;height:8mm}
  </style></head><body>
  <section class="page" style="padding-right:14mm">
    <div class="head"><h1>Feiertage ${YEAR}</h1><div class="meta">Alle Bundesländer<br>Gratis-Übersicht</div></div>
    <div class="yeargrid" style="gap:3mm 6mm">${Array.from({ length: 12 }, (_, i) => miniMonth(i + 1, hm)).join("")}</div>
    <table class="grid ft"><tr><th class="name">Feiertag</th>${codes.map(c => `<th>${c}</th>`).join("")}</tr>${rows}</table>
    <p class="foot"><span>● gesetzlicher Feiertag · ◐ nur regional · Mini-Kalender zeigt bundesweite Feiertage</span><span>Den kompletten Planer ${YEAR} für dein Bundesland gibt es im Shop.</span></p>
  </section></body></html>`;
}

/* ---------------- PDFs erzeugen ---------------- */
async function main() {
  const only = process.argv[2];
  mkdirSync(DIST, { recursive: true }); mkdirSync(BUILD, { recursive: true });
  const { chromium } = createRequire(import.meta.url)("playwright");
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const render = async (html, name) => {
    const f = join(BUILD, name + ".html");
    writeFileSync(f, html);
    await page.goto("file://" + f);
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: join(DIST, name + ".pdf"), preferCSSPageSize: true, printBackground: true });
    console.log("✓", name);
  };
  for (const s of Object.keys(STATES)) {
    if (only && s !== only) continue;
    await render(buildHtml(s), `Planer-${YEAR}-${s}-${STATES[s].replace(/ü/g, "ue").replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/\s+/g, "-")}`);
  }
  if (!only) await render(buildSampleHtml(), `GRATIS-Feiertage-${YEAR}-alle-Bundeslaender`);
  await browser.close();
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main();
