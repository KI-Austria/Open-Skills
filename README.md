# KI Austria Open Skills

Praktische, offen verfügbare Skills von KI Austria. Sie helfen KI-Assistenten, klar definierte Aufgaben nachvollziehbar und wiederholbar auszuführen.

## Verfügbare Skills

### Bild gemeinsam entwickeln

Der Skill führt von einer ersten Bildidee über ein kurzes, adaptives Interview zu einem klaren Bildbriefing, einem präzisen Bildprompt und – wenn ein Bildwerkzeug verfügbar ist – zum fertigen Bild. Er stellt immer nur die nächste entscheidende Frage und nutzt bereits genannten Kontext weiter.

```bash
npx skills add KI-Austria/Open-Skills --skill bild-entwickeln
```

### Text gemeinsam entwickeln

Der Skill klärt einen Schreibauftrag in einem kurzen, adaptiven Gespräch und liefert danach den direkt nutzbaren Text, eine kompakte Conceptmap und eine nachvollziehbare Begründung der sichtbaren Textentscheidungen. Er fragt nur nach Informationen, die das Ergebnis wesentlich verändern.

```bash
npx skills add KI-Austria/Open-Skills --skill text-entwickeln
```

### Kennzeichnungspflicht

Der Skill prüft Inhalte vor einer Veröffentlichung nach den Transparenzregeln des EU AI Act. Er nutzt zuerst den vorhandenen Kontext, fragt nur bei entscheidenden Lücken kompakt nach, empfiehlt danach Kennzeichnung, Wortlaut und Platzierung und setzt die freigegebene Fassung auf Wunsch in Text oder Bild um.

```bash
npx skills add KI-Austria/Open-Skills --skill kennzeichnungspflicht
```

Danach den jeweiligen Skill im Agenten aufrufen, zum Beispiel:

```text
bild-entwickeln
```

oder, wenn die Plattform Skills mit `$` adressiert:

```text
$bild-entwickeln Entwickle mit mir ein Bild für diese Idee.
```

Die Installation über `npx skills` verwendet ein unabhängiges Drittanbieter-Werkzeug. Alternativ kann der jeweilige Ordner unter `skills/` manuell in das Skill-Verzeichnis des verwendeten Agenten kopiert werden.

## So arbeitet der Skill

1. Er prüft Inhalt und Kontext selbst und stellt nur bei entscheidenden Lücken kurze Rückfragen – typischerweise keine bis zwei, niemals mehr als drei.
2. Er liefert eine quellenbasierte Vorprüfung samt genauem Kennzeichnungsvorschlag.
3. Erst nach ausdrücklicher Freigabe verändert er den Text oder erzeugt eine neue gekennzeichnete Bilddatei.

## Hinweise

Die Inhalte dienen der praktischen Orientierung und ersetzen keine Rechtsberatung. Sie geben keine Garantie für Rechtskonformität und keine Haftungsfreistellung. Für die korrekte Einordnung und Veröffentlichung bleiben Nutzerinnen, Nutzer und veröffentlichende Organisationen verantwortlich.

Der Quellcode steht unter der [MIT-Lizenz](LICENSE). Die mitgelieferten EU-Icons stammen von der Europäischen Kommission und bleiben von der MIT-Lizenz ausgenommen; Herkunft und Verwendung sind in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) dokumentiert.

## Mitwirken

Fehlerberichte und Verbesserungsvorschläge sind als GitHub Issue willkommen. Änderungen an rechtlichen Referenzen sollen auf offizielle Primärquellen verweisen und ein Prüfdatum enthalten.
