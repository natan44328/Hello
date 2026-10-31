# Follow-Check

Instagram-Übersicht fürs Handy: wer dir entfolgt ist, wer dir nicht zurückfolgt, Fans, gegenseitige Follows, offene Anfragen und ein Verlauf pro Monat.

`index.html` liest den offiziellen Instagram-Datenexport (ZIP, Format JSON) direkt im Browser aus. Kein Login, kein Passwort, nichts wird hochgeladen.

## Anleitung
1. Instagram → Profil → Menü ☰ → **Kontenübersicht**
2. **Deine Informationen und Berechtigungen** → **Deine Informationen herunterladen** → **Informationen herunterladen**
3. Konto wählen → **Einige deiner Informationen** → **Follower und gefolgte Personen** → Weiter
4. **Auf Gerät herunterladen** → Zeitraum **Gesamter Zeitraum**, Format **JSON** → **Dateien erstellen**
5. Warten, bis Instagram meldet, dass die Datei fertig ist, dann **Herunterladen**
6. Follow-Check öffnen → **Export auswählen** → ZIP wählen
7. Regelmäßig wiederholen: unter **Änderungen** siehst du, wer dir seit dem letzten Mal entfolgt ist.

Profilbesucher kann man nicht sehen. Instagram stellt diese Daten nirgends bereit.

## Ratgeber & Affiliate-Links
- Inhalte stehen in `content/ratgeber.json`, die Einstellungen in `links.json` (Amazon-Tracking-ID, Impressum).
- `python3 tools/build.py` erzeugt `ratgeber/*.html`, `impressum.html`, `datenschutz.html`, `sitemap.xml` und `robots.txt`.
- Bei jedem Push auf `master` baut `.github/workflows/pages.yml` die Seite und veröffentlicht sie über GitHub Pages.
- Alle Amazon-Links sind mit ★ und `rel="sponsored"` gekennzeichnet. Auf jeder Seite steht ein Werbehinweis.
