# Bildkennzeichnung einrichten

## Abhängigkeit

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Das Skript benötigt Pillow und unterstützt PNG, JPEG/JFIF und WebP.

## Verwendung

```bash
python scripts/label_image.py eingabe.png --kind generated --position bottom-right
```

Das Original wird nie überschrieben. Die Ausgabe wird vollständig erzeugt, synchronisiert und anschließend ohne Ersetzen einer vorhandenen Zieldatei veröffentlicht.

## Sicherheits- und Datenschutzgrenzen

- Eingabe: reguläre Datei, maximal 64 MiB, maximal 40 Megapixel und maximal 16.384 Pixel je Kante.
- Die Eingabe wird als begrenzter unveränderlicher Snapshot decodiert.
- Das Zielverzeichnis muss der ausführenden Person gehören und darf nicht gruppen- oder weltbeschreibbar sein.
- Metadaten werden standardmäßig vollständig entfernt.
- `--preserve-metadata` nur nach Sensitivitätsprüfung, nur ohne Formatwechsel und kumulativ bis 256 KiB. Unterstützt werden formatspezifisch ICC, DPI, normalisierte EXIF und bei PNG Textfelder.
- Beschädigte oder nicht verlustfrei normalisierbare EXIF-Daten werden abgelehnt.

## Kontrolle

Nach jeder Erzeugung das Ergebnis visuell prüfen: vollständiges offizielles Icon, unveränderte Proportionen, ausreichender Kontrast, Außenabstand, Lesbarkeit und keine Überdeckung wichtiger Bildbereiche.
