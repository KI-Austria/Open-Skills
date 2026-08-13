---
name: kennzeichnungspflicht
description: Prüfe berufliche Texte und Medien vor Veröffentlichung nach Art. 50 EU AI Act. Sortiere interne Wissensarbeit und Einzelkorrespondenz sofort aus, bestimme den richtigen Normadressaten, frage nur entscheidende Lücken nach und setze eine Kennzeichnung nur vor einer tatsächlichen Änderung nach Freigabe um. Verwende den Skill bei E-Mails, Berichten, Präsentationen, Postings, Webseiten, Bildern, Audio, Video, Chatbots oder Fragen wie „Muss ich das als KI kennzeichnen?“.
version: 2.0.0
author: KI Austria
license: MIT
metadata:
  hermes:
    tags: [eu-ai-act, transparency, knowledge-work, media]
    related_skills: []
---

# Kennzeichnungspflicht

## Ziel und Grenze

Liefere eine praktische, quellenbasierte Vorprüfung – keine Rechtsberatung, Compliance-Garantie oder Haftungsfreistellung. Trenne **erforderlich**, **vorsorglich empfohlen**, **regelmäßig nicht erforderlich** und **unklar**. Die Verantwortung für konkrete Nutzung und Veröffentlichung bleibt bei der handelnden Person oder Organisation; gesetzlicher Normadressat ist je nach Fall Anbieter oder Betreiber.

Lies vor der Prüfung [references/eu-baseline.md](references/eu-baseline.md). Nutze für typische Büro- und Medienfälle [references/work-examples.md](references/work-examples.md). Lies [references/icon-selection.md](references/icon-selection.md) nur vor einer Icon-Empfehlung oder Bildbearbeitung.

## Schnellpfad für Wissensarbeit

Prüfe in dieser Reihenfolge und stoppe, sobald der Fall eindeutig ist:

1. **Nur Unterstützung:** Rechtschreibung, Grammatik, Formatierung oder Recherche ohne KI-generierten bzw. KI-manipulierten veröffentlichten Inhalt → regelmäßig nicht erforderlich. Bei Übersetzung oder Stilbearbeitung eines öffentlichen Informationstexts zuerst sämtliche Tatbestandsmerkmale prüfen, insbesondere Informationszweck und Thema von öffentlichem Interesse. Fehlt eines, liegt dieser Textfall regelmäßig nicht vor. Nur wenn alle erfüllt sind, zusätzlich qualifizierte Kontrolle der finalen Fassung und letztendliche rechtliche Veröffentlichungsverantwortung einschließlich dieser Kontrolle prüfen.
2. **Nicht veröffentlicht:** berufliche Einzelkorrespondenz, individueller Kundenbericht, kleine geschlossene Gruppe oder organisationsinterne Kommunikation einschließlich Intranet → Art.-50-Textkennzeichnung regelmäßig nicht erforderlich. Deepfakes, direkte KI-Interaktion, andere Gesetze, Verträge oder interne Regeln separat prüfen.
3. **Menschlich vermittelte Kommunikation:** Ein Mensch hat einen KI-Entwurf inhaltlich geprüft, versendet ihn selbst und bleibt der tatsächliche Gesprächspartner → regelmäßig keine direkte KI-Interaktion.
4. **Öffentlicher Text:** Weiterprüfen, wenn ein KI-generierter oder KI-manipulierter Text veröffentlicht wird, die Öffentlichkeit informieren soll und ein Thema von öffentlichem Interesse betrifft. Für die Ausnahme müssen kumulativ eine qualifizierte Kontrolle der finalen Fassung und die letztendliche rechtliche Veröffentlichungsverantwortung einschließlich dieser Kontrolle vorliegen.
5. **Bild, Audio oder Video:** Nur als Deepfake prüfen, wenn der Inhalt hinsichtlich Authentizität oder Wahrheit täuschen könnte. Fotorealismus allein genügt nicht.

## Prüflogik

### 1. Tatsachen und Normadressat bestimmen

Nutze Inhalt, Metadaten und Gesprächskontext zuerst selbst. Leite die Entstehungsgeschichte nie nur aus Stil oder Aussehen ab.

Bestimme den **Normadressat**:

- **Anbieter** für direkte KI-Interaktion und maschinenlesbare Markierung nach Art. 50 Abs. 1 und 2; bei Absatz 2 am Stichtag zusätzlich Inverkehrbringungsdatum und Übergangsfrist bis 2. Dezember 2026 prüfen;
- **Betreiber/Deployer** für Emotionserkennung, biometrische Kategorisierung, Deepfakes und bestimmte öffentliche Texte nach Art. 50 Abs. 3 und 4;
- Beschäftigte unter Weisung, reine Empfänger, Hosts oder Weiterverbreiter sind nicht automatisch eigene Betreiber;
- rein persönliche und nicht berufliche Nutzung natürlicher Personen gesondert behandeln.

Prüfe zusätzlich für den jeweils einschlägigen Absatz, ob das konkrete System gesetzlich für Strafverfolgungszwecke zugelassen ist und die absatzspezifischen Grenzen und Schutzvorkehrungen erfüllt. Übertrage eine Ausnahme nie pauschal zwischen Anbieter- und Betreiberpflichten; Details stehen in der Baseline.

### 2. Nur entscheidende Lücken fragen

Gehe ohne Rückfrage zur Einstufung, wenn alles Relevante bekannt ist. Sonst stelle gebündelt höchstens drei kurze Fragen:

1. **KI-Eingriff:** Was hat die KI in der finalen Fassung tatsächlich erzeugt oder substanziell verändert?
2. **Zielgruppe und Zweck:** Intern, Einzelperson/geschlossene Gruppe oder öffentlich – und soll der Text die Öffentlichkeit über ein Thema von öffentlichem Interesse informieren?
3. **Kontrolle und Rolle:** Wer entschied über den KI-Einsatz? Wurde die finale Fassung entweder von einer fachkundigen natürlichen Person einschließlich Fakten substanziell geprüft oder durch eine verantwortliche Redaktion einschließlich Fakten und Quellenvertrauenswürdigkeit tatsächlich substanziell kontrolliert – und wer trägt die letztendliche rechtliche Verantwortung für die Veröffentlichung einschließlich dieser Kontrolle?

Nenne bereits eine vorläufige Richtung mit sichtbarer Annahme. Frage bekannte Tatsachen nicht erneut.

### 3. Kompakt entscheiden

```text
Vorprüfung: [erforderlich | vorsorglich empfohlen | regelmäßig nicht erforderlich | unklar]
Warum: [entscheidende Tatsachen in 2–4 einfachen Sätzen]
Empfehlung: [genauer Wortlaut oder „keine Kennzeichnung nach Art. 50 nötig“]
Platzierung: [nur wenn ein Hinweis sinnvoll ist]
EU-Icon: [Basic | AI Generated | AI Modified | keines] – [bei Text regelmäßig keines; sonst nur bei sinnvoller Medienkennzeichnung]
Offen/Risiko: [nur falls relevant]
Stand: [Datum] · Grundlage: Art. 50 EU AI Act und EU-Kommissionsleitlinien
```

Bei `regelmäßig nicht erforderlich` schließe ab. Biete keine Änderung an, außer eine freiwillige Kennzeichnung ist konkret sinnvoll. Bei Serienfällen liefere zusätzlich eine wiederverwendbare Regel für den Workflow statt jeden Inhalt einzeln zu interviewen.

## Umsetzen – nur mit Mutationsfreigabe

**Nur vor einer tatsächlichen Änderung** an Text oder Datei ist eine ausdrückliche Freigabe nötig. Reine Prüfung, Begründung und ein vorgeschlagener Wortlaut benötigen keine zweite Runde. Eine imperative Anweisung wie „prüfe und kennzeichne“ zu einem konkreten Inhalt oder einer konkreten Datei gilt als Mutationsfreigabe, auch wenn Wortlaut und genaue Umsetzung erst ermittelt werden. Nur eine reine Prüfbitte wie „prüfe, ob eine Kennzeichnung nötig ist“ oder echte Unklarheit über das gewünschte Ziel erfordert vor der Änderung eine Rückfrage.

### Text

Füge den freigegebenen Hinweis beim ersten Kontakt mit dem betroffenen Inhalt klar und leicht erkennbar ein. Erhalte Ton und Format.

### Bild

Nutze ausschließlich vollständige Dateien aus `assets/eu-icons/`. Verändere Farben, Beschriftung, Seitenverhältnis oder innere Abstände nicht. Prüfe vorab Python und Pillow; Setup siehe [references/image-setup.md](references/image-setup.md).

```bash
python scripts/label_image.py eingabe.png --kind generated --position bottom-right
```

Erzeuge immer eine neue Datei mit `-gekennzeichnet`, überschreibe das Original nicht und prüfe Ergebnis, Lesbarkeit, Kontrast, sichere Position und Orientierung visuell. Verwende ein eigenes, nicht gruppen- oder weltbeschreibbares Zielverzeichnis; unsichere gemeinsame Verzeichnisse werden abgelehnt. Das Skript entfernt standardmäßig sämtliche Metadaten einschließlich EXIF, ICC, DPI und PNG-Text. Übernimm Metadaten nur ausdrücklich, nach Prüfung und ohne Formatwechsel mit `--preserve-metadata`; unterstützt werden formatspezifisch ICC, DPI und normalisierte EXIF sowie bei PNG Textfelder, insgesamt größenbegrenzt. Wenn das nicht möglich ist, behaupte keine Umsetzung.

### Präsentation, Dokument oder PDF

Prüfe zuerst Öffentlichkeit und konkretes Element. Der Dateityp löst keine Pflicht aus. Kennzeichne nur betroffene Inhalte beim ersten Kontakt, erhalte das Original und erzeuge eine neue Datei.

### Audio oder Video

Bei erforderlicher Offenlegung: im Video sichtbar, im Audio hörbar und bei losgelöster Weitergabe zusätzlich im Begleittext. Prüfe anwendbare Barrierefreiheit: ausreichender Kontrast, Alternativtext bzw. zugängliche Begleitbeschreibung sowie bei Video Untertitel und gegebenenfalls eine hörbare Form. Verändere Medien nur mit geeignetem Werkzeug und Mutationsfreigabe.

## Fertig, wenn

- Normadressat, Zielgruppe, KI-Eingriff und einschlägiger Art.-50-Fall geklärt sind;
- interne Wissensarbeit nicht wie öffentliche Publikation behandelt wurde;
- bestätigte Tatsachen und Annahmen getrennt sind;
- Status, Wortlaut, gegebenenfalls Platzierung und anwendbare Barrierefreiheit konkret sind;
- eine Dateiänderung nur nach Freigabe erfolgt und das neue Ergebnis wirklich geprüft wurde;
- Prüfdatum und bei ausführlicher Antwort offizielle Quellen genannt sind.
