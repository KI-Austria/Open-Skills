---
name: kennzeichnungspflicht
description: Prüfe berufliche Texte und Medien vor Veröffentlichung nach Art. 50 EU AI Act. Sortiere interne Wissensarbeit und Einzelkorrespondenz sofort aus, bestimme den richtigen Normadressaten, frage nur entscheidende Lücken nach und setze eine Kennzeichnung nur vor einer tatsächlichen Änderung nach Freigabe um. Verwende den Skill bei E-Mails, Berichten, Präsentationen, Postings, Webseiten, Bildern, Audio, Video, Chatbots oder Fragen wie „Muss ich das als KI kennzeichnen?“.
version: 2.1.0
author: KI Austria
license: MIT
metadata:
  hermes:
    tags: [eu-ai-act, transparency, knowledge-work, media]
    related_skills: []
---

# Kennzeichnungspflicht

## Ziel und Grenze

Liefere eine praktische Vorprüfung – keine Rechtsberatung, Compliance-Garantie oder Haftungsfreistellung. Trenne **erforderlich**, **vorsorglich empfohlen**, **regelmäßig nicht erforderlich** und **unklar**. Die Verantwortung für Nutzung und Veröffentlichung bleibt bei der handelnden Person oder Organisation. Nutze bekannte Tatsachen; kein Rechtsinterview.

## Schnellpfad für Wissensarbeit – zuerst und ohne Referenzdatei

Prüfe sofort. Ein Teilpfad darf nur diesen Teil der Prüfung ausschließen:

1. **Nur Unterstützung:** Rechtschreibung, Grammatik, Formatierung oder Recherche ohne KI-generierten bzw. KI-manipulierten veröffentlichten Inhalt → schließt nur den öffentlichen Textpfad aus.
2. **Nicht veröffentlicht:** berufliche Einzelkorrespondenz, individueller Kundenbericht, kleine geschlossene Gruppe oder organisationsinterne Kommunikation einschließlich Intranet → schließt nur den öffentlichen Textpfad aus.
3. **Menschlich vermittelte Kommunikation:** Ein Mensch hat einen KI-Entwurf inhaltlich geprüft, versendet ihn selbst und bleibt tatsächlicher Gesprächspartner → schließt nur die direkte KI-Interaktion aus. Hier nicht bei öffentlichem Newsletter, Posting oder öffentlicher Information stoppen; den öffentlichen Textpfad weiterprüfen.

Gib das globale Urteil „Keine Kennzeichnung nach Art. 50 nötig“ erst wenn anhand des bekannten Kontexts auch Deepfake, direkte KI-Interaktion, Emotionserkennung, biometrische Kategorisierung und Anbieterpflicht nach Absatz 2 ausgeschlossen sind. Dann: **Antworte in höchstens drei kurzen Zeilen** mit Status, einfachem Grund und Urteil. Keine Quellenliste, kein Icon, kein Disclaimer und keine Änderungsfrage, sofern nicht verlangt.

Verbindlicher Routingvertrag: Starte mit allen Zweigen, entferne nur die beim bestätigten Signal genannten und schließe global nur bei leerer Restmenge ab.

```json routing-contract
{"branches":["public_text","direct_interaction","deepfake","emotion_recognition","biometric_categorization","provider_content_system"],"signals":{"assistance_only":["public_text"],"not_public":["public_text"],"human_mediated":["direct_interaction"],"no_synthetic_media":["deepfake"],"no_emotion_or_biometrics":["emotion_recognition","biometric_categorization"],"no_provider_content_system":["provider_content_system"]}}
```

## Referenzen nur bei Bedarf laden

- **Lade die Rechtsbaseline erst**, wenn ein öffentlicher KI-Text, direkte KI-Interaktion, Emotionserkennung, biometrische Kategorisierung, Deepfake, Anbieterpflicht, Strafverfolgungsausnahme, Übergangsfrist oder rechtlich entscheidender Grenzfall vorliegt: [references/eu-baseline.md](references/eu-baseline.md).
- **Lade Praxisfälle nur** bei unklarer Abgrenzung oder wenn eine wiederverwendbare Serienregel gebraucht wird: [references/work-examples.md](references/work-examples.md).
- **Lade die Icon-Auswahl nur** vor Auswahl oder Empfehlung eines Icons: [references/icon-selection.md](references/icon-selection.md).
- **Lade das Bild-Setup nur** vor tatsächlicher Bildbearbeitung: [references/image-setup.md](references/image-setup.md).

## Relevante Fälle prüfen

### Tatbestand vor Ausnahme

Bei Übersetzung oder Stilbearbeitung eines öffentlichen Informationstexts zuerst sämtliche Tatbestandsmerkmale prüfen:

1. KI hat den finalen Text erzeugt oder substanziell manipuliert.
2. Der Text wird veröffentlicht.
3. Er soll die Öffentlichkeit informieren.
4. Er betrifft ein Thema von öffentlichem Interesse.

Fehlt eines, liegt dieser Textfall regelmäßig nicht vor. Nur wenn alle erfüllt sind, prüfe die Ausnahme: finale Fassung entweder durch eine fachkundige natürliche Person einschließlich Fakten substanziell geprüft **oder** durch eine verantwortliche Redaktion einschließlich Fakten und Quellenvertrauenswürdigkeit tatsächlich substanziell kontrolliert; zusätzlich braucht es die letztendliche rechtliche Veröffentlichungsverantwortung einschließlich dieser Kontrolle. Details stehen in der Baseline.

### Rollen und Medien

Bestimme den **Normadressat**:

- **Anbieter**: direkte KI-Interaktion und maschinenlesbare Markierung nach Art. 50 Abs. 1 und 2; bei Absatz 2 gegebenenfalls Inverkehrbringungsdatum und Übergangsfrist bis 2. Dezember 2026 prüfen.
- **Betreiber/Deployer**: Emotionserkennung, biometrische Kategorisierung, Deepfakes und bestimmte öffentliche Texte nach Abs. 3 und 4.
- Beschäftigte, reine Empfänger, Hosts oder Weiterverbreiter sind nicht automatisch Betreiber.
- Rein persönliche, nicht berufliche Nutzung natürlicher Personen separat behandeln.

Bild, Audio oder Video nur als Deepfake prüfen, wenn Authentizität oder Wahrheit täuschend dargestellt werden könnte; Fotorealismus allein genügt nicht. Übertrage eine Ausnahme nie pauschal zwischen Anbieter- und Betreiberpflichten.

## Nur entscheidende Lücken fragen

Gehe ohne Rückfrage zur Einstufung, wenn alles Relevante bekannt ist. Sonst frage gebündelt höchstens drei Punkte:

1. Was hat die KI in der finalen Fassung tatsächlich erzeugt oder substanziell verändert?
2. Ist der Inhalt intern, individuell/geschlossen oder öffentlich – und informiert ein Text über ein Thema von öffentlichem Interesse?
3. Wer entschied über Einsatz, finale Kontrolle und letztendliche rechtliche Veröffentlichungsverantwortung?

Nenne die vorläufige Richtung; frage Bekanntes nicht erneut.

## Kompakt entscheiden

```text
Vorprüfung: [erforderlich | vorsorglich empfohlen | regelmäßig nicht erforderlich | unklar]
Warum: [entscheidende Tatsachen in 1–3 einfachen Sätzen]
Empfehlung: [genauer Wortlaut oder „Keine Kennzeichnung nach Art. 50 nötig“]
Platzierung / EU-Icon / Risiko: [nur wenn tatsächlich relevant]
Stand: [Datum]
```

Schließe nur nach der globalen Leerprüfung oben ab. Keine freiwillige Kennzeichnung oder Änderung anbieten, außer konkret sinnvoll oder verlangt.

## Umsetzen – nur mit Mutationsfreigabe

**Nur vor einer tatsächlichen Änderung** an Text oder Datei ist eine ausdrückliche Freigabe nötig. Prüfung, Begründung und vorgeschlagener Wortlaut benötigen keine zweite Runde. Eine imperative Anweisung wie „prüfe und kennzeichne“ zu einem konkreten Inhalt oder einer konkreten Datei gilt als Mutationsfreigabe. „Prüfe, ob eine Kennzeichnung nötig ist“ erlaubt keine Änderung.

### Text

Füge einen nötigen Hinweis beim ersten Kontakt erkennbar ein. Erhalte Ton und Format.

### Bild

Bei tatsächlicher Bildbearbeitung das Bild-Setup laden und befolgen. Überschreibe das Original nicht und prüfe die neue Datei visuell.

### Präsentation, Dokument oder PDF

Der Dateityp löst keine Pflicht aus. Prüfe Öffentlichkeit und betroffenes Element; erhalte das Original.

### Audio oder Video

Bei Offenlegung: im Video sichtbar, im Audio hörbar, bei losgelöster Weitergabe zusätzlich im Begleittext. Prüfe anwendbare Barrierefreiheit wie Kontrast, Alternativtext/Begleitbeschreibung und Untertitel.

## Fertig, wenn

- Rolle, Zielgruppe, KI-Eingriff und einschlägiger Fall geklärt sind;
- der Schnellpfad ohne unnötige Referenzen oder Rückfragen abgeschlossen wurde;
- bestätigte Tatsachen und Annahmen getrennt sind;
- Status und nur tatsächlich relevante Umsetzungshinweise konkret sind;
- eine Datei nur nach Freigabe geändert und das Ergebnis geprüft wurde.
