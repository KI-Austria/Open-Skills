# Agent guide – Open Skills

## Zwei getrennte Produktebenen

Ein veröffentlichter Skill besteht aus zwei strikt getrennten Teilen:

1. `skills/<slug>/` ist das portable Laufzeitpaket für KI-Assistenten. Hier stehen nur Arbeitsweise, Referenzen, Assets, Skripte und Laufzeit-Metadaten.
2. `catalog/skills/<slug>.json` beschreibt ausschließlich, wie derselbe Skill auf der KI-Austria-Website erklärt und einsortiert wird.

Website-Texte, Teaser, Vorschau-Schritte, Website-URLs und Installationswerbung gehören nie in `SKILL.md` oder einen anderen Teil des Laufzeitpakets. Umgekehrt darf der Website-Katalog keine zusätzliche Arbeitslogik enthalten, die im Skill fehlt.

## Neuer oder geänderter Skill

- Der Ordnername unter `skills/`, `name` im Frontmatter und `slug` im Katalog müssen identisch sein.
- Jeder Ordner unter `skills/` braucht genau eine Datei unter `catalog/skills/`.
- Die Website-Darstellung knapp und beschreibend halten. Keine Superlative, Leistungsversprechen oder erfundene Funktionen.
- Danach `python scripts/build_catalog.py` ausführen. Das erzeugt `catalog/catalog.json` deterministisch.
- `python scripts/build_catalog.py --check` und `python -m pytest -q` müssen bestehen.

Ein Pull Request darf nicht als fertig gelten, wenn der Katalog fehlt oder `catalog/catalog.json` nicht dem aktuellen Stand entspricht.

## Benennung

- Der Name beschreibt vorzugsweise das praktische Ergebnis für den Menschen, nicht die interne Format- oder Implementierungslogik.
- Skills für gemeinsame Orientierung, Reflexion und Entscheidung dürfen als natürliche **Wir-Frage** benannt werden, zum Beispiel `wo-stehen-wir`. Die Frage bleibt im sichtbaren Titel erhalten; der Slug verwendet Kleinbuchstaben, ASCII und Bindestriche.
- Fachliche Skills wie `kennzeichnungspflicht` werden nicht in dieses Muster gezwungen. Eine Namensfamilie ist nur dann sinnvoll, wenn die Frage den tatsächlichen Zweck des Skills präzise beschreibt.
