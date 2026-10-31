# Businessplan: Follow-Check

Ein kleines Online-Business mit **0 € Startkosten** und wenig laufendem Aufwand.

## Die Idee in einem Satz
Ein deutsches Web-Tool, das zeigt, wer dir auf Instagram entfolgt ist, **ohne Passwort und ohne Upload**. Die Grundfunktionen sind gratis, eine einmalige Pro-Freischaltung kostet 4,99 €, dazu kommen freiwillige Spenden.

## Warum das Sinn macht
- **Nachfrage:** „Wer hat mir entfolgt?“ fragen sich sehr viele Instagram-Nutzer, und Instagram zeigt es nicht an.
- **Schwache Konkurrenz:** Die meisten Apps wollen das Instagram-Passwort. Das führt zu Kontosperren und Sicherheitsrisiken. Dazu kommen teure Abos (oft 5,99 $ pro **Woche**). Follow-Check ist sicher, deutsch und ohne Abo.
- **Keine laufenden Kosten:** Alles läuft im Browser. Das Hosting über GitHub Pages ist kostenlos, und es gibt keinen Server, der ausfallen kann.
- **Das Produkt ist schon fertig.** Du musst es nur noch online stellen und bekannt machen.

## Ehrliche Einnahmen-Rechnung

| Besucher pro Monat | Kaufen Pro (2 %) | Spenden (0,5 % à 3 €) | Umsatz ca. |
|---|---|---|---|
| 300 | 6 × 4,99 € | 1–2 | ~ 30 € |
| 2.000 | 40 × 4,99 € | 10 | ~ 230 € |
| 10.000 | 200 × 4,99 € | 50 | ~ 1.150 € |

- **Gebühren:** Lemon Squeezy nimmt ca. 5 % + 0,50 $ pro Verkauf. Bei 4,99 € bleiben dir etwa 4,25 €.
- Die Kaufquote von 1–3 % ist eine Schätzung und **keine Garantie**.
- **Realistisch:** In den ersten Monaten kommen eher 0–50 € rein. Mehr wird es erst, wenn Google die Seite findet und du ein paar Videos postest.
- **„Faul“ heißt hier:** einmal etwa 5–10 Stunden einrichten und bewerben. Danach reichen ein bis zwei Stunden pro Monat (E-Mails beantworten, ab und zu ein Video).

## Start-Checkliste
1. **Online stellen:** GitHub → Repo → Settings → Pages → Branch auswählen → Save. Danach ist die Seite unter `https://<dein-name>.github.io/Hello/` erreichbar.
   - Tipp: Das Repo in `follow-check` umbenennen. Eine eigene Domain (ca. 10 € pro Jahr) ist optional.
2. **Spendenlink:** Ein kostenloses Konto bei [Ko-fi](https://ko-fi.com) anlegen und den Link in `index.html` bei `SUPPORT_URL` eintragen.
3. **Pro verkaufen:**
   1. Konto bei [Lemon Squeezy](https://www.lemonsqueezy.com) anlegen.
   2. Produkt „Follow-Check Pro“ für 4,99 € erstellen und **„Generate license keys“** aktivieren.
   3. In `index.html` den Checkout-Link bei `PRO_URL` und die Store-ID bei `LS_STORE_ID` eintragen.
   - Lemon Squeezy kümmert sich als „Merchant of Record“ um die Umsatzsteuer in allen Ländern.
   - Solange `PRO_URL` leer ist, ist alles kostenlos. Du kannst also erst Nutzer sammeln und später Pro einschalten.
4. **Impressum und Datenschutz:** Die Platzhalter `[...]` in `impressum.html` und `datenschutz.html` mit echten Daten füllen. Ohne Impressum darfst du in Deutschland kein Geld verdienen, und du riskierst Abmahnungen.
   - Wer seine Wohnadresse nicht veröffentlichen will, kann einen Impressum-Service (ca. 5–10 € pro Monat) nutzen.
5. **Gewerbe anmelden:** online beim Gewerbeamt deiner Stadt, ca. 20–60 €.
   - Im Fragebogen beim Finanzamt die **Kleinunternehmerregelung (§ 19 UStG)** wählen. Bis 25.000 € Umsatz im Vorjahr (und höchstens 100.000 € im laufenden Jahr) gibt es keine Umsatzsteuer und kaum Papierkram.
   - Gewinne müssen trotzdem in die Steuererklärung.
6. **Unter 18?** Dann brauchst du deine Eltern. Für ein eigenes Gewerbe nötig sind:
   - die Zustimmung deiner Eltern **und** des Familiengerichts (§ 112 BGB)
   - Auch Lemon Squeezy, PayPal und Stripe verlangen meist 18+.
   - Einfachste Lösung: Ein Elternteil meldet das Gewerbe an und führt die Konten.

## Bekannt machen (wenig Aufwand, kostet nichts)
- **TikTok, Reels, Shorts:** Kurze Bildschirmvideos, zum Beispiel:
  - „So siehst du, wer dir auf Instagram entfolgt ist – ohne App und ohne Passwort“
  - „Warum du Unfollower-Apps NIE dein Passwort geben solltest“

  Fünf bis zehn Videos einmalig aufnehmen und über ein paar Wochen verteilt posten.
- **Google:** Die Seite `anleitung-instagram-export.html` ist auf Suchbegriffe wie „wer hat mir auf Instagram entfolgt“ ausgerichtet. Melde die Seite in der [Google Search Console](https://search.google.com/search-console) an, damit Google sie schneller findet.
- **Reddit und Foren:** Bei passenden Fragen (r/de, r/Instagram, gutefrage.net) hilfreich antworten und das Tool erwähnen. Kein Spam.

## Mögliche Erweiterungen später
- Dasselbe Prinzip für **TikTok** (TikTok bietet auch einen Datenexport an): ein zweites Produkt mit wenig Zusatzaufwand.
- Englische Version für mehr Reichweite.

## Vorsicht vor Abzocke
Kurse zu „Passive Income“, Dropshipping-Coaches, Krypto-Signale und alles, wofür du **vorher** Geld zahlen sollst, sind fast immer Abzocke. Echtes passives Einkommen entsteht nur aus einem nützlichen Produkt plus etwas Geduld. Genau das ist dieses hier.
