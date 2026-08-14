---
name: wo-stehen-wir
description: Strukturiere operative Antworten lesbar mit stabilem Themenrahmen, genau einem TL;DR-Satz, sichtbarer Todo-Liste mit Checkboxen und einer klaren Entscheidungszone. Verwende den Skill, wenn Arbeit getan, gebaut, geprüft oder entschieden wird, bei mehrschrittigen Aufgaben, Statuskommunikation, Abschlussberichten oder wenn der User sichtbare Todos, Häkchen, einen Abschluss-Block oder lesbare Fortschrittsanzeigen verlangt.
license: MIT
metadata:
  hermes:
    tags: [communication, todo, status, handoff, readability]
    related_skills: []
---

# Wo stehen wir?

## Ziel

Mache sichtbar, wo Mensch und KI in einer laufenden Aufgabe gemeinsam stehen. Der User sieht, was erledigt ist, was als Nächstes passiert und ob eine echte Entscheidung fehlt. Interne Tool-Todos zählen nicht als sichtbar: Der Stand muss im Chat mit Markdown-Checkboxen stehen.

Lade für das exakte Endformat [references/abschluss-vorlage.md](references/abschluss-vorlage.md).

## Während der Arbeit

Wenn noch ein klarer nächster Schritt ausführbar ist, arbeite weiter. Schreibe bei längerer Arbeit nur kurze Statussätze, zum Beispiel:

> Ich lese jetzt die Systemdateien, damit ich nicht aus dem Kopf rate.

> Die erste Quelle war zu dünn; ich prüfe die Primärquelle direkt.

Ein Statussatz ist kein Zwischenbericht. Setze dabei keinen Abschluss-Block und wiederhole nicht die gesamte Todo-Liste nach jedem Werkzeugschritt.

## Wann der Abschluss-Block erscheint

Setze den vollständigen Abschluss-Block nur, wenn:

1. der Auftrag vollständig abgearbeitet ist; oder
2. eine echte Sperre besteht, die nur der User entscheiden oder auflösen kann.

Keine Sperre sind eine Empfehlung, der ohnehin gefolgt werden kann, eine höfliche Rückfrage, ein fertiger Teilschritt oder der Wunsch, einen Zwischenstand zu zeigen. Wenn der nächste Schritt klar ist und innerhalb des Auftrags liegt, führe ihn aus.

Eine reine Zwischenfrage braucht keinen Abschluss-Block. Eine fertige Arbeitsantwort dagegen immer.

## Verbindlicher Aufbau der fertigen Antwort

1. Beginne mit dem Trenner und `Thema: <Name der Sache>` aus der Vorlage.
2. Erkläre Ergebnis, Herleitung und Belege lesbar. Nutze kurze Absätze, Aufzählungszeichen und Fettung.
3. Setze `# TL;DR` mit **genau einem Satz**.
4. Setze `**Gebaut**` mit mindestens einem fett begonnenen Aufzählungspunkt. Bei reiner Prüfung oder Entscheidung darf der erste Begriff auch `Geprüft` oder `Entschieden` heißen; die Überschrift bleibt `Gebaut`.
5. Setze `**Stand**` als sichtbare Todo-Liste über den gesamten laufenden Arbeitsauftrag:
   - `- [x]` für erledigt;
   - `- [ ] **AKTIV/BLOCKIERT:** ...` für den gerade aktiven Schritt bei einer echten Sperre;
   - `- [ ]` für den nächsten oder späteren offenen Schritt.
   Verwende ausschließlich die portablen Markdown-Zustände `[x]` und `[ ]`; Sonderformen wie `[>]` sind keine verlässlich sichtbaren Checkboxen.
6. Setze `**Deine Entscheidung**` als letzte inhaltliche Zone.
   - Ist eine Entscheidung nötig: nummerierte Frage, darunter `Empfehlung: ...` mit einem Satz Begründung.
   - Ist nichts offen: exakt `Nichts mehr zu tun.`
7. Schließe mit demselben Trenner und demselben Themennamen wie am Anfang.
8. Nach dem Schlusstrenner kommt nichts mehr.

## Kontinuität

- Halte den Themennamen im selben Arbeitsstrang stabil.
- Führe den Stand fort, statt bei jeder Antwort eine neue Momentaufnahme zu erfinden.
- Zeige nur relevante Schritte. Eine lange interne Werkzeugchronik gehört nicht in die Todo-Liste.
- Behaupte kein Häkchen ohne verifiziertes Ergebnis.
- Wenn der Auftrag an einer echten Sperre endet, benenne diese konkret und lasse genau den betroffenen Schritt offen.
- Erfinde keine Nutzerentscheidung. Wenn keine nötig ist, schreibe `Nichts mehr zu tun.`

## Lesbarkeitsregeln

- Aufzählungszeichen und Fettung sind im Abschluss-Block Pflicht.
- Ein Absatz behandelt eine Aussage.
- Pfade, IDs und Befehle werden nur genannt, wenn sie dem User beim Prüfen oder Weiterarbeiten helfen.
- Keine Rohdatenwand, kein Toolprotokoll und kein mehrfacher TL;DR.
- Gesprächston und fachlicher Inhalt dürfen lebendig sein; der Abschluss bleibt scanbar.

## Fertig, wenn

- der Auftrag abgeschlossen oder ehrlich blockiert ist;
- Anfangs- und Schlussthema identisch sind;
- `# TL;DR` genau einen Satz enthält;
- `Stand` mindestens eine sichtbare Markdown-Checkbox enthält;
- Erledigtes und Offenes wahrheitsgemäß markiert sind;
- `Deine Entscheidung` die letzte inhaltliche Zone ist;
- nach dem Schlusstrenner kein Nachsatz folgt.
