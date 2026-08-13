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

Der Skill prüft berufliche Texte und Medien vor einer Veröffentlichung nach Art. 50 des EU AI Act. Er sortiert interne Kommunikation und persönliche berufliche Korrespondenz zuerst aus, bestimmt den richtigen Normadressaten und fragt nur bei entscheidenden Lücken nach. Danach liefert er Status, Wortlaut und Platzierung. Eine Freigabe braucht er nur, bevor er Text oder Dateien tatsächlich verändert.

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

1. Er nutzt zuerst den Schnellpfad: Standardbearbeitung, berufliche Einzelkorrespondenz und interne Kommunikation werden nicht wie öffentliche Publikationen behandelt.
2. Er bestimmt Anbieter bzw. Betreiber, Inhalt, Zielgruppe und menschliche Kontrolle und stellt nur bei entscheidenden Lücken kurze Rückfragen.
3. Er liefert eine quellenbasierte Vorprüfung samt genauem Kennzeichnungsvorschlag. Eine ausdrückliche Freigabe ist nur nötig, bevor er Text oder Dateien tatsächlich verändert.

## Entwicklung und Tests

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

Die Tests prüfen Skill-Verträge, portable Paketpfade, CLI-Hilfe, Originalschutz, atomare Ausgabe in vertrauenswürdige Zielverzeichnisse, Ablehnung gemeinsam beschreibbarer Zielverzeichnisse, Bild- und Dimensionslimits, Bildformate, Mindestlesbarkeit, Transparenz, EXIF-Ausrichtung sowie standardmäßige Entfernung und explizite, begrenzte Übernahme von Metadaten. Die fachlichen Abnahmefälle stehen in `tests/behavior-cases.md`.

## Hinweise

Die Inhalte dienen der praktischen Orientierung und ersetzen keine Rechtsberatung. Sie geben keine Garantie für Rechtskonformität und keine Haftungsfreistellung. Für die korrekte Einordnung und Veröffentlichung bleiben Nutzerinnen, Nutzer und veröffentlichende Organisationen verantwortlich.

Der Quellcode steht unter der [MIT-Lizenz](LICENSE). Die mitgelieferten EU-Icons stammen von der Europäischen Kommission und bleiben von der MIT-Lizenz ausgenommen; Herkunft und Verwendung sind in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) dokumentiert.

## Mitwirken

Fehlerberichte und Verbesserungsvorschläge sind als GitHub Issue willkommen. Änderungen an rechtlichen Referenzen sollen auf offizielle Primärquellen verweisen und ein Prüfdatum enthalten.
