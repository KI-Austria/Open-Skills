---
name: wo-stehen-wir
description: Strukturiere operative Antworten lesbar mit stabilem Themenrahmen, genau einem TL;DR-Satz, sichtbarer Todo-Liste mit Checkboxen und einer klaren Entscheidungszone. Verwende den Skill, wenn Arbeit getan, gebaut, geprüft oder entschieden wird, bei mehrschrittigen Aufgaben, Statuskommunikation, Abschlussberichten oder wenn der User sichtbare Todos, Häkchen, einen Abschluss-Block oder lesbare Fortschrittsanzeigen verlangt. Verwende ihn außerdem bei Fragen wie „Wo stehen wir?“, „Wo sind wir?“, „Wo stehn wir?“, „Was ist erledigt?“, „Was fehlt noch?“ oder „Wie geht es weiter?“.
license: MIT
metadata:
  hermes:
    tags: [communication, todo, status, handoff, readability]
    related_skills: []
---

# Wo stehen wir?

## Ziel

Mache sichtbar, wo Mensch und KI in einer laufenden Aufgabe gemeinsam stehen. Der User sieht, was erledigt ist, was als Nächstes passiert und ob eine echte Entscheidung fehlt. Interne Tool-Todos zählen nicht als sichtbar: Der Stand muss im Chat mit Markdown-Checkboxen stehen.

Nutze [references/abschluss-vorlage.md](references/abschluss-vorlage.md) als inhaltlichen Leitfaden. Der dort gezeigte Themenrahmen ist verbindlich; die Darstellung der Inhaltszonen bleibt flexibel.

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

Schließe die Antwort als visuell klar erkennbaren Ergebnisblock ab. Der Block muss beim Überfliegen sofort auffindbar sein.

Der Ergebnisblock enthält in dieser Reihenfolge:

1. einen Themenkopf aus nativen Markdown-Trennlinien, `**THEMA**` und einem stabilen, kurzen Themennamen als Überschrift;
2. eine TL;DR-Kurzfassung mit **genau einem Satz**; sichtbar darf sie `TL;DR`, `Kurz gesagt` oder sinngemäß heißen;
3. Ergebnis, Herleitung und Belege in kurzen Absätzen oder Aufzählungen;
4. einen sichtbaren Stand über den gesamten laufenden Arbeitsauftrag:
   - `- [x]` für erledigt;
   - `- [ ] **AKTIV/BLOCKIERT:** ...` für den gerade aktiven Schritt bei einer echten Sperre;
   - `- [ ]` für den nächsten oder späteren offenen Schritt.
   Verwende ausschließlich die portablen Markdown-Zustände `[x]` und `[ ]`; Sonderformen wie `[>]` sind keine verlässlich sichtbaren Checkboxen.
5. eine Entscheidungszone als letzten inhaltlichen Teil.
   - Ist eine Entscheidung nötig: nummerierte Frage, darunter `Empfehlung: ...` mit einem Satz Begründung.
   - Ist nichts offen: exakt `Nichts mehr zu tun.`

Wiederhole denselben Themenkopf nach der Entscheidungszone am Ende der Antwort. Nach diesem zweiten Themenkopf kommt nichts mehr. Verwende für beide Rahmen nur native Markdown-Trennlinien aus `---`; keine langen Unicode-Balken, HTML-Tricks oder festen Linienlängen.

Die Bezeichnungen und die konkrete visuelle Darstellung der Inhaltszonen dürfen sich an Aufgabe und Oberfläche anpassen.

## Kontinuität

- Halte den Themennamen im selben Arbeitsstrang stabil.
- Führe den Stand fort, statt bei jeder Antwort eine neue Momentaufnahme zu erfinden.
- Zeige nur relevante Schritte. Eine lange interne Werkzeugchronik gehört nicht in die Todo-Liste.
- Behaupte kein Häkchen ohne verifiziertes Ergebnis.
- Wenn der Auftrag an einer echten Sperre endet, benenne diese konkret und lasse genau den betroffenen Schritt offen.
- Erfinde keine Nutzerentscheidung. Wenn keine nötig ist, schreibe `Nichts mehr zu tun.`

## Lesbarkeitsregeln

- Aufzählungszeichen und Fettung machen den Abschluss-Block scanbar.
- Ein Absatz behandelt eine Aussage.
- Pfade, IDs und Befehle werden nur genannt, wenn sie dem User beim Prüfen oder Weiterarbeiten helfen.
- Keine Rohdatenwand, kein Toolprotokoll und kein mehrfacher TL;DR.
- Gesprächston und fachlicher Inhalt dürfen lebendig sein; der Abschluss bleibt scanbar.

## Fertig, wenn

- der Auftrag abgeschlossen oder ehrlich blockiert ist;
- der Ergebnisblock beim Überfliegen sofort auffindbar ist;
- am Anfang und Ende derselbe Themenkopf mit nativen Markdown-Trennlinien steht;
- die TL;DR-Kurzfassung genau einen Satz enthält;
- `Stand` mindestens eine sichtbare Markdown-Checkbox enthält;
- Erledigtes und Offenes wahrheitsgemäß markiert sind;
- die Entscheidungszone der letzte inhaltliche Teil ist;
- nach dem zweiten Themenkopf nichts mehr folgt.
