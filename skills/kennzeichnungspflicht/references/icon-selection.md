# Auswahl der offiziellen EU-Icons

Quelle: [Europäische Kommission – EU icons for labelling AI-generated content](https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content), Stand 10. August 2026.

Die Icons sind ein freiwilliges Hilfsmittel zur einheitlichen Transparenz. Die Offenlegungspflicht kann verbindlich sein, obwohl das konkrete EU-Icon freiwillig ist. Verwende bei einem rechtlich relevanten Fall zusätzlich einen verständlichen Hinweis, wenn das Icon allein den Sachverhalt nicht klar erklärt.

## Icon-Typ wählen

| Typ | Wann verwenden | Asset-Präfix |
|---|---|---|
| **AI Generated** | Der gesamte betroffene Deepfake bzw. Medieninhalt wurde vollständig durch KI erzeugt; außer Prompting gab es keine menschlich erstellten Bestandteile oder redaktionelle Kontrolle. | `LABEL_AI GENERATED_` |
| **AI Modified** | Ein bereits bestehender menschlicher Medieninhalt wurde mit KI teilweise so verändert, dass ein betroffener Deepfake entstand. | `LABEL_AI MODIFIED_` |
| **Basic AI** | KI war beteiligt, aber „vollständig erzeugt“ oder „teilweise verändert“ lässt sich nicht zuverlässig zuordnen. | `LABEL_AI_` |
| **Keines** | Keine sichtbare Kennzeichnung empfohlen, der Fall betrifft nur Text oder ein Icon wäre für den Fall irreführend. Für kennzeichnungspflichtige Texte genügt regelmäßig ein klarer verständlicher Texthinweis; lege kein EU-Icon nahe, wenn es den Prüfstatus oder die Entstehung überzeichnet. | – |

Wenn die Entstehung nicht bestätigt ist, stelle eine Rückfrage. Wähle nicht aufgrund des Aussehens.

## Farb- und Transparenzvariante wählen

Jeder Typ liegt in vier offiziellen Varianten vor:

- `black.png`: schwarze, voll deckende Variante auf hellem oder unruhigem Grund;
- `white.png`: weiße, voll deckende Variante auf dunklem oder unruhigem Grund;
- `black transparent.png`: schwarze 50-%-Variante nur bei ausreichend hellem, ruhigem Grund;
- `white transparent.png`: weiße 50-%-Variante nur bei ausreichend dunklem, ruhigem Grund.

Bevorzuge voll deckend, wenn Lesbarkeit oder Kontrast nicht eindeutig sind. Verändere Farbe, Wortlaut, Seitenverhältnis und innere Abstände nicht.

## Platzierung

- Beim ersten Kontakt und direkt am betroffenen Inhalt.
- So groß, dass der Text auf dem tatsächlichen Ausgabegerät lesbar bleibt.
- Mit sicherem Außenabstand; nicht in Beschnitt-, Untertitel-, Bedien- oder Logo-Zonen.
- Bei Bild oder Video meist oben oder unten rechts, sofern dort ausreichender Kontrast und keine wichtige Bildinformation liegt.
- Bei Weitergabe muss die Kennzeichnung möglichst im exportierten Medium erhalten bleiben.

Das Skript `scripts/label_image.py` wählt bei `--theme auto` anhand der lokalen Helligkeit eine schwarze oder weiße voll deckende Variante. Prüfe das gerenderte Ergebnis trotzdem visuell.
