#!/usr/bin/env python3
"""Overlay an unmodified official EU AI icon on a raster image."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from PIL import Image, ImageStat
except ImportError as exc:
    raise SystemExit("Pillow fehlt. Installiere es mit: python -m pip install Pillow") from exc


KINDS = {
    "basic": "LABEL_AI_",
    "generated": "LABEL_AI GENERATED_",
    "modified": "LABEL_AI MODIFIED_",
}
POSITIONS = ("top-left", "top-right", "bottom-left", "bottom-right")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fügt ein offizielles EU-KI-Icon ein und erhält das Original."
    )
    parser.add_argument("input", type=Path, help="PNG-, JPEG- oder WebP-Eingabebild")
    parser.add_argument("--output", type=Path, help="Neue Ausgabedatei; Standard: *-gekennzeichnet")
    parser.add_argument("--kind", choices=KINDS, required=True, help="EU-Icon-Typ")
    parser.add_argument("--theme", choices=("auto", "black", "white"), default="auto")
    parser.add_argument(
        "--opacity", choices=("solid", "half"), default="solid", help="Offizielle Voll- oder 50-%-Variante"
    )
    parser.add_argument("--position", choices=POSITIONS, default="bottom-right")
    parser.add_argument(
        "--width", type=float, default=0.32, help="Iconbreite relativ zur Bildbreite, 0.10 bis 0.60"
    )
    parser.add_argument(
        "--margin", type=float, default=0.035, help="Außenabstand relativ zur kürzeren Bildseite"
    )
    return parser.parse_args()


def default_output(input_path: Path) -> Path:
    suffix = input_path.suffix or ".png"
    return input_path.with_name(f"{input_path.stem}-gekennzeichnet{suffix}")


def icon_path(kind: str, theme: str, opacity: str) -> Path:
    variant = f"{theme}{' transparent' if opacity == 'half' else ''}.png"
    return Path(__file__).resolve().parent.parent / "assets" / "eu-icons" / f"{KINDS[kind]}{variant}"


def trim_transparent(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Das Icon enthält keine sichtbaren Pixel.")
    return rgba.crop(bbox)


def coordinates(position: str, canvas: tuple[int, int], overlay: tuple[int, int], margin: int) -> tuple[int, int]:
    width, height = canvas
    overlay_width, overlay_height = overlay
    x = margin if position.endswith("left") else width - overlay_width - margin
    y = margin if position.startswith("top") else height - overlay_height - margin
    return max(0, x), max(0, y)


def local_luminance(image: Image.Image, position: str, size: tuple[int, int], margin: int) -> float:
    x, y = coordinates(position, image.size, size, margin)
    region = image.convert("RGB").crop((x, y, x + size[0], y + size[1])).convert("L")
    return float(ImageStat.Stat(region).mean[0])


def main() -> int:
    args = parse_args()
    if not 0.10 <= args.width <= 0.60:
        raise SystemExit("--width muss zwischen 0.10 und 0.60 liegen.")
    if not 0.0 <= args.margin <= 0.20:
        raise SystemExit("--margin muss zwischen 0.0 und 0.20 liegen.")
    if not args.input.is_file():
        raise SystemExit(f"Eingabedatei nicht gefunden: {args.input}")

    output = args.output or default_output(args.input)
    if output.resolve() == args.input.resolve():
        raise SystemExit("Das Original darf nicht überschrieben werden. Wähle eine neue Ausgabedatei.")
    if output.exists():
        raise SystemExit(f"Ausgabedatei existiert bereits und wird nicht überschrieben: {output}")

    with Image.open(args.input) as source:
        source.load()
        base = source.convert("RGBA")
        metadata = source.info.copy()

    # Use one official file to determine the rendered dimensions before auto contrast selection.
    probe = trim_transparent(Image.open(icon_path(args.kind, "black", args.opacity)))
    target_width = max(1, round(base.width * args.width))
    target_height = max(1, round(probe.height * target_width / probe.width))
    max_height = max(1, round(base.height * 0.35))
    if target_height > max_height:
        target_height = max_height
        target_width = max(1, round(probe.width * target_height / probe.height))

    margin = max(1, round(min(base.size) * args.margin))
    theme = args.theme
    if theme == "auto":
        brightness = local_luminance(base, args.position, (target_width, target_height), margin)
        theme = "black" if brightness >= 140 else "white"

    icon_file = icon_path(args.kind, theme, args.opacity)
    if not icon_file.is_file():
        raise SystemExit(f"EU-Icon fehlt: {icon_file}")
    icon = trim_transparent(Image.open(icon_file)).resize((target_width, target_height), Image.Resampling.LANCZOS)
    x, y = coordinates(args.position, base.size, icon.size, margin)
    base.alpha_composite(icon, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    suffix = output.suffix.lower()
    save_args: dict[str, object] = {}
    if "icc_profile" in metadata:
        save_args["icc_profile"] = metadata["icc_profile"]
    if suffix in (".jpg", ".jpeg"):
        rendered = base.convert("RGB")
        save_args.update(quality=95, subsampling=0)
    elif suffix == ".webp":
        rendered = base
        save_args.update(quality=95)
    elif suffix == ".png":
        rendered = base
    else:
        raise SystemExit("Ausgabeformat muss PNG, JPEG oder WebP sein.")
    rendered.save(output, **save_args)
    print(f"Erstellt: {output}")
    print(f"Icon: {args.kind}, {theme}, {args.opacity}; Position: {args.position}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
