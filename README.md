# Follow-Check

Instagram-Übersicht fürs Handy: wer dir entfolgt ist, wer dir nicht zurückfolgt, Fans, gegenseitige Follows, offene Anfragen und ein Verlauf pro Monat.

`index.html` liest den offiziellen Instagram-Datenexport (ZIP, Format JSON) direkt im Browser aus. Es gibt keinen Login und kein Passwort, nichts wird hochgeladen. Es werden auch keine fremden Schriften oder Tracker geladen.

## Anleitung
1. Instagram → Profil → Menü ☰ → **Kontenübersicht**
2. **Deine Informationen und Berechtigungen** → **Deine Informationen herunterladen** → **Informationen herunterladen**
3. Konto wählen → **Einige deiner Informationen** → **Follower und gefolgte Personen** → Weiter
4. **Auf Gerät herunterladen** → Zeitraum **Gesamter Zeitraum**, Format **JSON** → **Dateien erstellen**
5. Warten, bis Instagram meldet, dass die Datei fertig ist, dann **Herunterladen**
6. Follow-Check öffnen → **Export auswählen** → ZIP wählen
7. Regelmäßig wiederholen: Unter **Änderungen** siehst du, wer dir seit dem letzten Mal entfolgt ist.

Profilbesucher kann man nicht sehen. Instagram stellt diese Daten nirgends bereit.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Die App |
| `anleitung-instagram-export.html` | Anleitungsseite für Google („Wer hat mir auf Instagram entfolgt?“) |
| `impressum.html`, `datenschutz.html` | Rechtliche Seiten. **Platzhalter `[...]` ausfüllen!** |
| `site.css` | Stil der Unterseiten |
| `BUSINESS.md` | Businessplan, Einnahmen-Rechnung und Start-Checkliste |

## Online stellen (kostenlos)
GitHub → Settings → **Pages** → Branch auswählen → Save.

## Geld verdienen
Die Einstellungen stehen ganz oben im `<script>` von `index.html`:

```js
const SUPPORT_URL = "";   // z. B. https://ko-fi.com/deinname → Unterstützen-Button
const PRO_URL = "";       // Lemon-Squeezy-Checkout-Link → aktiviert die Pro-Freischaltung
const PRO_PRICE = "4,99 € inkl. USt.";
const LS_STORE_ID = 0;    // deine Lemon-Squeezy-Store-ID
```

- Solange `PRO_URL` leer ist, ist alles kostenlos.
- Mit `PRO_URL` sind Verlauf, Zusatzlisten, „Namen kopieren“ und der Vergleich mit älteren Exporten Pro-Funktionen. Die Beispieldaten zeigen trotzdem alles, damit man sieht, was Pro kann.
- Freigeschaltet wird mit einem Lizenzschlüssel von Lemon Squeezy. Dabei wird nur der Schlüssel geprüft, keine Instagram-Daten.

Details stehen in [BUSINESS.md](BUSINESS.md).
