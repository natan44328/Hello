---
name: find-skills
description: Passende Skills finden und hinzufügen. Laden, wenn der Nutzer nach einem Skill fragt („gibt es einen Skill für …“, „füge den Skill X hinzu“, „find skills“) oder wenn eine Aufgabe wiederkehrt und ein Skill sie besser machen würde.
---

# Skills finden

Ziel: Für eine Aufgabe den besten vorhandenen Skill finden. Gibt es keinen, einen neuen im Repo anlegen. Nie einen Skill erfinden oder als vorhanden ausgeben, der nicht gefunden wurde.

## 1. Anfrage verstehen
- Worum geht es (Thema, Werkzeug, Ergebnis)? Daraus 2–5 Suchbegriffe ableiten, auf Deutsch und Englisch (z. B. „ui ux“, „design“, „accessibility“).
- Ist der Name ungenau oder abgekürzt (z. B. „mem“), nach dem Begriff und nach verwandten Begriffen suchen („memory“, „notes“).

## 2. Der Reihe nach suchen
1. **Schon geladene Skills:** die Skill-Liste in dieser Sitzung durchsehen (inklusive Plugin-Skills wie `design:…`, `productivity:…`).
2. **Projekt-Skills:** `ls .claude/skills/` im Repo.
3. **Persönliche Skills:** `ls ~/.claude/skills/` (falls vorhanden).
4. **claude.ai-Konto:** `ListSkills` (aktivierte) und `SearchSkills` (alle) mit den Suchbegriffen. Passt ein Ergebnis, das noch nicht aktiviert ist: mit `SuggestSkills` die Karte zum Hinzufügen zeigen.
5. **Öffentliche Skills (optional, braucht Netzwerk):** `npx skills find <begriff>` sucht im offenen Skills-Verzeichnis (skills.sh); `npx skills add <owner/repo>` installiert. Vor der Installation den `SKILL.md`-Inhalt lesen und dem Nutzer zeigen: fremde Skills sind nicht geprüft und können Befehle enthalten.

## 3. Ergebnis zeigen
- Höchstens 3–5 Treffer, je eine Zeile: Name, wofür, wo er liegt (geladen / Projekt / Konto / öffentlich).
- Einen klaren Vorschlag machen, welcher am besten passt.
- Kein Treffer: das offen sagen und anbieten, einen eigenen Skill zu schreiben.

## 4. Eigenen Skill anlegen (wenn nichts passt)
- Pfad: `.claude/skills/<name>/SKILL.md`, Name klein mit Bindestrichen.
- Frontmatter mit `name` und `description`. Die Beschreibung sagt, **wann** der Skill geladen werden soll; sie entscheidet, ob er später automatisch greift.
- Inhalt auf das Projekt zuschneiden (vorhandene Dateien, Tokens, Konventionen lesen), konkrete Regeln statt allgemeiner Tipps, am Ende eine kurze Prüfliste.
- Hinweis an den Nutzer: Neue Skills werden erst in der nächsten Sitzung geladen.
- Für aufwendigere Skills (Skripte, Evals) den Skill `anthropic-skills:skill-creator` verwenden.
