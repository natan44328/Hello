#!/usr/bin/env python3
"""Baut die Ratgeber-Seiten, Rechtliches und sitemap.xml aus content/ratgeber.json + links.json.

Aufruf:  python3 tools/build.py
Neuer Ratgeber: Eintrag in content/ratgeber.json ergänzen, Skript laufen lassen, committen.
"""
import datetime
import html
import json
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "links.json").read_text(encoding="utf-8"))
GUIDES = json.loads((ROOT / "content" / "ratgeber.json").read_text(encoding="utf-8"))
TAG = CFG.get("amazonTag", "").strip()
SITE = CFG["siteUrl"].rstrip("/") + "/"
TODAY = datetime.date.today().isoformat()
e = html.escape


def amazon(query):
    params = {"k": query}
    if TAG:
        params["tag"] = TAG
    return "https://www.amazon.de/s?" + urllib.parse.urlencode(params)


def page(title, description, body, depth, canonical, extra_head=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{e(canonical)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}</head>
<body>
<div class="wrap">
<nav class="crumbs small"><a href="{up}index.html">Follow-Check</a> · <a href="{up}ratgeber/index.html">Ratgeber</a></nav>
{body}
<footer class="foot small muted">
  <p>Hinweis: Links mit ★ sind Affiliate-Links (Werbung). Kaufst du darüber, erhalten wir eine kleine Provision. Für dich ändert sich am Preis nichts. Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.</p>
  <p><a href="{up}impressum.html">Impressum</a> · <a href="{up}datenschutz.html">Datenschutz</a></p>
</footer>
</div>
</body>
</html>
"""


def guide_page(g):
    crit = "".join(f"<li><b>{e(t)}</b><span>{e(x)}</span></li>" for t, x in g["criteria"])
    rows = "".join(
        f"<tr><td><b>{e(t['name'])}</b></td><td>{e(t['for'])}</td><td class='nowrap'>{e(t['price'])}</td></tr>"
        for t in g["types"]
    )
    cards = ""
    for t in g["types"]:
        pros = "".join(f"<li>{e(p)}</li>" for p in t["pros"])
        cons = "".join(f"<li>{e(c)}</li>" for c in t["cons"])
        cards += f"""<section class="panel">
  <h3>{e(t['name'])}</h3>
  <p class="small muted">Passt für: {e(t['for'])} · {e(t['price'])}</p>
  <div class="pc"><ul class="pro">{pros}</ul><ul class="con">{cons}</ul></div>
  <a class="btn" href="{e(amazon(t['query']))}" rel="sponsored nofollow noopener" target="_blank">Aktuelle Angebote bei Amazon ansehen ★</a>
</section>
"""
    faq = "".join(f"<details class='panel'><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faq"])
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]
        ],
    }
    others = "".join(
        f"<a class='chip' href='{o['slug']}.html'>{e(o['short'])}</a>" for o in GUIDES if o["slug"] != g["slug"]
    )
    body = f"""<header>
  <div class="eyebrow">Kaufberatung · aktualisiert {TODAY}</div>
  <h1>{e(g['title'])}</h1>
  <p class="lead">{e(g['intro'])}</p>
  <p class="ad small">Werbung: Diese Seite enthält Affiliate-Links (★).</p>
</header>
<section class="panel"><h2>Die Typen im Überblick</h2>
<div class="tablewrap"><table><thead><tr><th>Typ</th><th>Passt für</th><th>Preis</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<h2>Worauf du achten solltest</h2>
<ul class="crit">{crit}</ul>
<h2>Welcher Typ passt zu dir?</h2>
{cards}
<h2>Häufige Fragen</h2>
{faq}
<section><h2>Weitere Ratgeber</h2><div class="chips">{others}</div></section>
"""
    head = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
    return page(g["title"], g["description"], body, 1, f"{SITE}ratgeber/{g['slug']}.html", head)


def index_page():
    items = "".join(
        f"""<a class="panel card" href="{g['slug']}.html"><h3>{e(g['title'])}</h3><p class="small muted">{e(g['description'])}</p></a>"""
        for g in GUIDES
    )
    body = f"""<header><div class="eyebrow">Ratgeber</div><h1>Ausrüstung für Instagram &amp; TikTok</h1>
<p class="lead">Ehrliche Kaufberatungen für Content mit dem Handy: Was du brauchst, was nicht, und worauf du achten solltest.</p></header>
{items}"""
    return page("Ratgeber: Handy-Ausrüstung für Creator", "Kaufberatungen für Ringlicht, Stativ, Mikrofon und Gimbal fürs Handy.", body, 1, f"{SITE}ratgeber/index.html")


def impressum_page():
    i = CFG.get("impressum", {})
    if i.get("name"):
        data = f"<p>{e(i['name'])}<br>{e(i.get('strasse', ''))}<br>{e(i.get('ort', ''))}</p><p>E-Mail: {e(i.get('email', ''))}</p>"
    else:
        data = "<p class='ad'>Angaben folgen. (Noch nicht ausgefüllt: links.json → impressum)</p>"
    body = f"""<h1>Impressum</h1>
<section class="panel"><h2>Angaben gemäß § 5 DDG</h2>{data}</section>
<section class="panel"><h2>Affiliate-Hinweis</h2><p>Diese Website nimmt am Amazon-EU-Partnerprogramm teil. Mit ★ markierte Links sind Werbelinks. Bei einem Kauf erhalten wir eine Provision, der Preis für dich bleibt gleich.</p></section>"""
    return page("Impressum", "Impressum", body, 0, f"{SITE}impressum.html")


def datenschutz_page():
    body = """<h1>Datenschutz</h1>
<section class="panel"><h2>Hosting</h2><p>Diese Seite wird über GitHub Pages (GitHub Inc.) bereitgestellt. Beim Aufruf verarbeitet GitHub technisch notwendige Daten wie deine IP-Adresse. Details: GitHub Privacy Statement.</p></section>
<section class="panel"><h2>Follow-Check</h2><p>Der Follow-Check verarbeitet deinen Instagram-Export ausschließlich lokal in deinem Browser. Es wird nichts hochgeladen. Gespeicherte Stände liegen nur im Speicher deines Browsers.</p></section>
<section class="panel"><h2>Schriften</h2><p>Schriften werden von Google Fonts geladen. Dabei wird deine IP-Adresse an Google übertragen.</p></section>
<section class="panel"><h2>Amazon-Partnerlinks</h2><p>Klickst du auf einen Amazon-Link, gelten ab dann die Datenschutzbestimmungen von Amazon. Amazon kann Cookies setzen, um den Kauf dieser Seite zuzuordnen.</p></section>
<section class="panel"><h2>Kein Tracking</h2><p>Wir verwenden keine Analyse-Tools und keine eigenen Cookies.</p></section>"""
    return page("Datenschutz", "Datenschutzerklärung", body, 0, f"{SITE}datenschutz.html")


def sitemap():
    urls = ["", "ratgeber/index.html", "impressum.html", "datenschutz.html"] + [f"ratgeber/{g['slug']}.html" for g in GUIDES]
    entries = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>\n'


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("geschrieben:", rel)


if __name__ == "__main__":
    for g in GUIDES:
        write(f"ratgeber/{g['slug']}.html", guide_page(g))
    write("ratgeber/index.html", index_page())
    write("impressum.html", impressum_page())
    write("datenschutz.html", datenschutz_page())
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    if not TAG:
        print("HINWEIS: links.json → amazonTag ist leer. Links funktionieren, bringen aber noch keine Provision.")
