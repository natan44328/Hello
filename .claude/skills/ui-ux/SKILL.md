---
name: ui-ux
description: UI/UX-Regeln für Follow-Check (index.html). Laden, bevor Layout, Farben, Texte, Komponenten oder Interaktionen der App geändert oder neu gebaut werden, und für UI/UX-Reviews der Seite.
---

# UI/UX für Follow-Check

Follow-Check ist eine Handy-App in einer einzigen Datei (`index.html`). Jede Änderung muss zuerst auf dem Handy gut funktionieren.

## Grundsätze
1. **Mobile first.** Eine Spalte, 360–430 px breit, 16 px Seitenabstand, kein horizontales Scrollen. Desktop zentriert die Spalte nur (max. ca. 560 px).
2. **Daumenzone.** Hauptnavigation bleibt die Tab-Leiste unten (`--bar-h`). Wichtige Aktionen liegen unten oder in der Mitte, nie nur oben rechts.
3. **Touch-Ziele** sind mindestens 44×44 px, mit mindestens 8 px Abstand untereinander.
4. **Safe Areas:** `env(safe-area-inset-*)` für Notch und Home-Indikator verwenden, vor allem bei der Tab-Leiste.
5. **Datenschutz sichtbar machen.** Der Hinweis „nichts wird hochgeladen“ steht nahe an der Dateiauswahl. Es gibt keine externen Requests außer Google Fonts.

## Design-Tokens (Pflicht)
- Farben nur über die Variablen in `:root` (`--bg`, `--surface`, `--line`, `--fg`, `--muted`, `--accent`, `--good`, `--warn`, `--bad` und die `*-soft`-Varianten). Keine neuen Hex-Werte direkt in Komponenten.
- Eine neue Farbe bekommt immer drei Werte: hell in `:root`, dunkel unter `@media (prefers-color-scheme: dark)` mit `:root:not([data-theme="light"])` und noch einmal unter `:root[data-theme="dark"]`.
- Bedeutung der Farben: `--bad` = entfolgt oder verloren, `--good` = neu oder gegenseitig, `--warn` = offen oder ausstehend, `--accent` = Aktion oder Auswahl. Farbe ist nie die einzige Information: immer auch Text oder Icon.
- Schriften: `--display` (Bricolage Grotesque) für Überschriften und große Zahlen, `--body` (Figtree) für Fließtext, `--mono` für Benutzernamen und Zahlen in Listen.

## Typografie und Abstände
- Fließtext mindestens 15–16 px, Zeilenhöhe 1.4–1.5. Kleine Hilfstexte mindestens 13 px in `--muted`.
- Abstände im 4-px-Raster (4, 8, 12, 16, 24, 32).
- Zahlen in Statistiken mit `font-variant-numeric: tabular-nums`.

## Zustände: jede Ansicht braucht alle vier
- **Leer:** Noch kein Export geladen. Ein Satz Erklärung und der Button „Export auswählen“.
- **Laden:** Fortschritt beim Entpacken des ZIP zeigen, keinen eingefrorenen Bildschirm.
- **Fehler:** In Klartext sagen, was falsch ist (z. B. „Das ZIP enthält keine JSON-Dateien. Wähle beim Export das Format JSON.“), und den nächsten Schritt nennen.
- **Ergebnis:** Zuerst die Zahl, dann die Liste. Leere Listen bekommen einen freundlichen Satz statt einer weißen Fläche.

## Listen
- Jede Zeile: Benutzername (mono), optional Datum, Tippen öffnet das Profil (`https://instagram.com/<name>`) in einem neuen Tab.
- Ab etwa 30 Einträgen ein Suchfeld oben anbieten; Sortierung sichtbar machen.
- Lange Namen mit `text-overflow: ellipsis` kürzen, nicht umbrechen.

## Texte (UX-Writing)
- Deutsch, „du“-Form, kurz und konkret. Buttons sind Verben: „Export auswählen“, „Verlauf löschen“.
- Instagram-Menüpunkte genau so schreiben, wie sie in der App heißen, und **fett** setzen (siehe README).
- Nichts versprechen, was die Daten nicht hergeben (z. B. keine Profilbesucher).

## Barrierefreiheit
- Kontrast: Text mindestens 4.5:1, große Zahlen und Icons mindestens 3:1, in hellem und dunklem Modus.
- Semantisches HTML: `<button>` für Aktionen, `<a>` für Links, Tabs mit `role="tablist"`, `role="tab"` und `aria-selected`.
- Sichtbarer Fokusring (`:focus-visible`) in `--accent`.
- `prefers-reduced-motion` respektieren: Animationen dann abschalten.

## Interaktion und Bewegung
- Übergänge 150–250 ms, `ease-out`. Keine Animation bei mehr als 100 Listenelementen gleichzeitig.
- Destruktive Aktionen (Verlauf löschen) brauchen eine Bestätigung oder ein Rückgängig.
- Gespeicherter Verlauf (`localStorage`): jeden Zugriff in `try/catch`; ohne Speicher muss die App trotzdem laufen.

## Prüfen vor dem Abschluss
1. Seite mit Playwright (Chromium ist vorinstalliert) in 390×844 öffnen, je einen Screenshot hell und dunkel (`colorScheme: 'dark'`).
2. Bei 320 px Breite prüfen: kein horizontales Scrollen (`document.documentElement.scrollWidth <= innerWidth`).
3. Leer-, Fehler- und Ergebniszustand einmal durchklicken.
4. Mit der Checkliste oben abgleichen und Abweichungen nennen.
