---
name: kennzeichnungspflicht
description: Prüfe Inhalte vor Veröffentlichung auf Transparenz- und Kennzeichnungspflichten nach Art. 50 EU AI Act, werte vorhandenen Kontext zuerst selbst aus, frage nur bei entscheidenden Lücken kompakt nach, empfehle eine konkrete Kennzeichnung und füge sie erst nach ausdrücklicher Freigabe in Text oder Bild ein. Verwende den Skill bei Postings, Webseiten, Präsentationen, Schulungen, Dokumenten, Bildern, Audio oder Video sowie bei Fragen wie „Muss ich das als KI kennzeichnen?“, „Kennzeichnungspflicht“ oder „Füge das EU-KI-Label ein“.
---

# Kennzeichnungspflicht

## Zweck und Grenze

Gib eine praktische, quellenbasierte Vorprüfung nach dem aktuell geltenden EU-Rechtsrahmen. Trenne strikt zwischen rechtlich erforderlich, vorsorglich empfohlen, regelmäßig nicht erforderlich und unklar.

Gib keine Rechtsberatung, Compliance-Garantie oder Haftungsfreistellung. Weise bei Grenzfällen, hohem Risiko oder fehlenden Tatsachen auf eine qualifizierte rechtliche Prüfung hin. Die Verantwortung für Inhalt und Veröffentlichung bleibt bei der veröffentlichenden Person oder Organisation.

Lies vor jeder fachlichen Prüfung [references/eu-baseline.md](references/eu-baseline.md). Lies vor einer Icon-Empfehlung oder Bildbearbeitung zusätzlich [references/icon-selection.md](references/icon-selection.md).

## Verbindlicher Ablauf

Arbeite immer in zwei getrennten Schritten. Überspringe die Freigabegrenze nicht.

### Schritt 0: Kontext selbst prüfen, nur entscheidende Lücken erfragen

Untersuche zuerst selbstständig den bereitgestellten Inhalt, sein Format, Metadaten und den bisherigen Gesprächskontext. Extrahiere alle bereits bekannten Tatsachen und frage sie nicht erneut ab. Leite die Entstehungsgeschichte trotzdem niemals allein aus Stil, Metadaten oder Aussehen ab.

Gehe direkt zu Schritt 1, wenn die entscheidenden Tatsachen eindeutig vorliegen. Stelle nur dann Rückfragen, wenn eine fehlende Tatsache die Einstufung oder die Wahl des Icons tatsächlich ändern kann. Stelle typischerweise null bis zwei und niemals mehr als drei kurze, gebündelte Fragen:

1. **KI-Anteil:** Was hat die KI tatsächlich erzeugt oder verändert: ganzer Inhalt, einzelne Teile oder nur Assistenz wie Rechtschreibung, Recherche oder Formatierung?
2. **Inhalt:** Handelt es sich um Bild, Audio oder Video mit realistisch dargestellten Personen/Ereignissen, um einen Text zu einem Thema von öffentlichem Interesse oder um einen anderen Inhalt?
3. **Veröffentlichung:** Wo und in welcher Rolle wird veröffentlicht; gab es eine inhaltliche menschliche Prüfung und übernimmt eine Person oder Organisation redaktionelle Verantwortung?

Frage nur nach Punkten, die nicht schon eindeutig beantwortet sind. Wenn eine Antwort eine neue wesentliche Lücke öffnet, stelle höchstens eine kurze Anschlussfrage. Liefere zusammen mit den Fragen bereits eine hilfreiche vorläufige Richtung, soweit dies möglich ist, und kennzeichne deren Annahmen sichtbar. Gib erst nach Klärung der entscheidenden Lücken eine abschließende Einstufung. Verändere keine Datei.

### Schritt 1: Prüfen und einen konkreten Weg empfehlen

Bewerte den Fall anhand der Referenz in dieser Reihenfolge:

1. Bestimme Rolle, Medium, KI-Eingriff und Veröffentlichungskontext.
2. Prüfe, ob eine sichtbare Pflicht nach Art. 50 betroffen ist.
3. Trenne die sichtbare Kennzeichnung von möglichen maschinenlesbaren Pflichten des Systemanbieters.
4. Ordne den Fall als **erforderlich**, **vorsorglich empfohlen**, **regelmäßig nicht erforderlich** oder **unklar** ein.
5. Wähle bei Bildern nur ein offizielles, unverändertes EU-Icon nach der Auswahlreferenz.
6. Formuliere den konkreten Hinweis und bestimme dessen Platzierung am ersten Kontaktpunkt.

Antworte kompakt in diesem Schema:

```text
Vorprüfung: [Status]
Warum: [2–4 verständliche Sätze mit den entscheidenden Tatsachen]
Empfehlung: [genauer Wortlaut]
Platzierung: [konkreter Ort und Zeitpunkt]
EU-Icon: [Basic | AI Generated | AI Modified | keines] – [Variante und Grund]
Offen/Risiko: [nur falls nötig]
Stand: [Datum] · Grundlage: Art. 50 EU AI Act und EU-Kommissionsleitlinien

Soll ich diese Fassung jetzt in den Text bzw. in eine neue Bilddatei einfügen?
```

Bei noch offenen entscheidenden Tatsachen verwende stattdessen kurz:

```text
Vorläufige Richtung: [wahrscheinlicher Status unter klar genannter Annahme]
Mein Vorschlag: [bereits hilfreicher nächster Weg]
Damit ich richtig entscheide: [nur 1–3 entscheidende Fragen]
```

Füge in Schritt 1 nichts ein. Eine Aufforderung wie „prüfe und kennzeichne“ ersetzt die Freigabe nach der Vorschau nicht.

### Schritt 2: Erst nach ausdrücklicher Freigabe umsetzen

Akzeptiere nur eine eindeutige Freigabe wie „ja“, „einfügen“, „umsetzen“ oder eine ausdrücklich korrigierte Fassung. Bei Änderungen am Vorschlag zeige die korrigierte Kurzfassung erneut und hole dafür die Freigabe ein.

#### Text

Füge den freigegebenen Hinweis so ein, dass er beim ersten Kontakt mit dem betroffenen Inhalt klar und leicht erkennbar ist. Erhalte Ton und Format. Kennzeichne den geänderten Abschnitt in der Übergabe oder liefere den vollständigen finalen Text, wenn der Nutzer ihn direkt braucht.

#### Bild

Nutze ausschließlich die Dateien in `assets/eu-icons/`. Erzeuge das EU-Icon nie neu und verändere seine Proportionen, Farben oder Beschriftung nicht.

Wenn Python und Pillow verfügbar sind, führe `scripts/label_image.py` aus. Erzeuge immer eine neue Datei mit dem Zusatz `-gekennzeichnet`; überschreibe das Original nicht. Prüfe das Ergebnis anschließend visuell. Beispiel:

```bash
python scripts/label_image.py eingabe.png --kind generated --position bottom-right
```

Wenn keine Bildbearbeitung verfügbar ist, behaupte keine erfolgreiche Änderung. Liefere stattdessen die gewählte Asset-Datei, Zielposition, empfohlene Größe und Abstände.

#### Präsentation, Dokument oder PDF

Nutze vorhandene Werkzeuge für das Dateiformat. Platziere den sichtbaren Hinweis auf der ersten betroffenen Folie oder Seite und bei Bedarf zusätzlich direkt am betroffenen Element. Erzeuge eine neue Datei und erhalte das Original.

#### Audio oder Video

Empfehle bzw. erstelle einen klar wahrnehmbaren Hinweis beim ersten Kontakt; bei Video in der Regel als sichtbares Overlay, bei Audio als hörbaren Hinweis. Ergänze den Hinweis in Beschreibung oder Begleittext, wenn der Inhalt außerhalb der Datei geteilt werden kann. Verändere Medien nur mit einer dafür verfügbaren Bearbeitungsmöglichkeit und nach Freigabe.

## Qualitätsregeln

- Behaupte niemals, eine Datei geändert zu haben, ohne das Ergebnis zu prüfen.
- Verwende einfache deutsche Sprache und erkläre Rechtsbegriffe kurz.
- Nenne das Prüfdatum und verlinke in einer ausführlichen Antwort die offiziellen Quellen aus der Referenz.
- Bezeichne freiwillige EU-Icons nicht als zwingend, wenn nur der klare Offenlegungshinweis verpflichtend ist.
- Behandle Barrierefreiheit, Kontrast, Lesbarkeit und Weitergabe als Teil einer guten Kennzeichnung.
- Empfehle bei einer unklaren Entstehungsgeschichte keine scheinpräzise Icon-Kategorie.
- Dokumentiere Annahmen und trenne sie sichtbar von bestätigten Tatsachen.
- Verwandle die Prüfung nicht in ein Interview: Nutze vorhandenen Kontext und frage nur entscheidungsrelevante Lücken.
