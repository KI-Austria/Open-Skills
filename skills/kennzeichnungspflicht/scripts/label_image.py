#!/usr/bin/env python3
"""Overlay a complete, unmodified official EU AI icon on a raster image."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import secrets
import stat
import struct
import sys
import tempfile
from typing import Optional
import warnings

try:
    from PIL import Image, ImageOps, ImageStat, PngImagePlugin, UnidentifiedImageError
except ImportError as exc:
    raise SystemExit(
        "Pillow fehlt. Installiere es im Skill-Ordner mit: "
        "python -m pip install -r requirements.txt"
    ) from exc


KINDS = {
    "basic": "LABEL_AI_",
    "generated": "LABEL_AI GENERATED_",
    "modified": "LABEL_AI MODIFIED_",
}
POSITIONS = ("top-left", "top-right", "bottom-left", "bottom-right")
SUPPORTED_FORMATS = {"PNG", "JPEG", "WEBP"}
MIN_VISIBLE_HEIGHT = 24
MIN_VISIBLE_WIDTH = 48
MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_DIMENSION = 16_384
MAX_METADATA_BYTES = 256 * 1024
Image.MAX_IMAGE_PIXELS = MAX_PIXELS
warnings.simplefilter("error", Image.DecompressionBombWarning)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fügt ein vollständiges offizielles EU-KI-Icon ein und erhält das Original."
    )
    parser.add_argument("input", type=Path, help="PNG-, JPEG- oder WebP-Eingabebild")
    parser.add_argument("--output", type=Path, help="Neue Ausgabedatei; Standard: *-gekennzeichnet")
    parser.add_argument("--kind", choices=KINDS, required=True, help="EU-Icon-Typ")
    parser.add_argument(
        "--theme",
        choices=("auto", "black", "white"),
        default="auto",
        help="Automatischer Kontrast oder feste schwarze/weiße Variante",
    )
    parser.add_argument(
        "--opacity",
        choices=("solid", "half"),
        default="solid",
        help="Offizielle Voll- oder 50-Prozent-Variante",
    )
    parser.add_argument("--position", choices=POSITIONS, default="bottom-right")
    parser.add_argument(
        "--width", type=float, default=0.32, help="Iconbreite relativ zur Bildbreite, 0.10 bis 0.60"
    )
    parser.add_argument(
        "--margin", type=float, default=0.035, help="Außenabstand relativ zur kürzeren Bildseite"
    )
    parser.add_argument(
        "--preserve-metadata",
        action="store_true",
        help="Geprüfte Metadaten bis 256 KiB formatspezifisch übernehmen; nur ohne Formatwechsel, kann sensible Daten enthalten",
    )
    return parser.parse_args()


def default_output(input_path: Path) -> Path:
    suffix = input_path.suffix or ".png"
    return input_path.with_name(f"{input_path.stem}-gekennzeichnet{suffix}")


def icon_path(kind: str, theme: str, opacity: str) -> Path:
    variant = f"{theme}{' transparent' if opacity == 'half' else ''}.png"
    return Path(__file__).resolve().parent.parent / "assets" / "eu-icons" / f"{KINDS[kind]}{variant}"


def visible_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Das Icon enthält keine sichtbaren Pixel.")
    return bbox


def coordinates(
    position: str, canvas: tuple[int, int], overlay: tuple[int, int], margin: int
) -> tuple[int, int]:
    width, height = canvas
    overlay_width, overlay_height = overlay
    x = margin if position.endswith("left") else width - overlay_width - margin
    y = margin if position.startswith("top") else height - overlay_height - margin
    return max(0, x), max(0, y)


def local_luminance(
    image: Image.Image, position: str, size: tuple[int, int], margin: int
) -> float:
    x, y = coordinates(position, image.size, size, margin)
    region = image.convert("RGB").crop((x, y, x + size[0], y + size[1])).convert("L")
    return float(ImageStat.Stat(region).mean[0])


def scaled_size(icon: Image.Image, base: Image.Image, width_ratio: float) -> tuple[int, int]:
    target_width = max(1, round(base.width * width_ratio))
    target_height = max(1, round(icon.height * target_width / icon.width))
    max_height = max(1, round(base.height * 0.35))
    if target_height > max_height:
        target_height = max_height
        target_width = max(1, round(icon.width * target_height / icon.height))
    return target_width, target_height


def ensure_readable(icon: Image.Image, target_size: tuple[int, int]) -> None:
    left, top, right, bottom = visible_bbox(icon)
    scale_x = target_size[0] / icon.width
    scale_y = target_size[1] / icon.height
    visible_width = round((right - left) * scale_x)
    visible_height = round((bottom - top) * scale_y)
    if visible_width < MIN_VISIBLE_WIDTH or visible_height < MIN_VISIBLE_HEIGHT:
        raise SystemExit(
            "Das Bild ist für ein lesbares EU-KI-Label zu klein oder zu flach "
            f"(sichtbarer Bereich nur ca. {visible_width}×{visible_height} Pixel)."
        )


def metadata_size(value: object) -> int:
    if isinstance(value, bytes):
        return len(value)
    if isinstance(value, str):
        return len(value.encode("utf-8", errors="replace"))
    return 0


def snapshot_input(path: Path) -> tempfile.SpooledTemporaryFile:
    descriptor = None
    snapshot = tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024, mode="w+b")
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise SystemExit("Die Eingabe muss eine reguläre Datei sein.")
        with os.fdopen(os.dup(descriptor), "rb") as source:
            remaining = MAX_INPUT_BYTES + 1
            while remaining:
                chunk = source.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                snapshot.write(chunk)
                remaining -= len(chunk)
        if snapshot.tell() > MAX_INPUT_BYTES:
            raise SystemExit(
                f"Die Dateigröße überschreitet das Sicherheitslimit von {MAX_INPUT_BYTES // (1024 * 1024)} MB."
            )
        snapshot.seek(0)
        return snapshot
    except SystemExit:
        snapshot.close()
        raise
    except OSError as exc:
        snapshot.close()
        raise SystemExit(f"Eingabedatei konnte nicht geöffnet oder gelesen werden: {exc}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def load_source_snapshot(
    snapshot: tempfile.SpooledTemporaryFile, auto_theme: bool, preserve_metadata: bool
) -> tuple[Image.Image, dict[str, object]]:
    try:
        snapshot.seek(0)
        with Image.open(snapshot) as source:
            if source.format not in SUPPORTED_FORMATS:
                raise SystemExit("Eingabeformat muss PNG, JPEG oder WebP sein.")
            width, height = source.size
            if (
                width > MAX_DIMENSION
                or height > MAX_DIMENSION
                or width * height > MAX_PIXELS
            ):
                raise SystemExit(
                    "Das Eingabebild ist für die sichere Verarbeitung zu groß "
                    f"({width}×{height} Pixel; maximal {MAX_PIXELS:,} Pixel und "
                    f"{MAX_DIMENSION} Pixel pro Kante)."
                )
            if getattr(source, "n_frames", 1) != 1:
                raise SystemExit("Mehrteilige oder animierte Bilder werden nicht unterstützt.")
            source.load()
            if auto_theme and "A" in source.getbands():
                alpha = source.getchannel("A")
                if alpha.getextrema()[0] < 255:
                    raise SystemExit(
                        "Bei transparentem Bildhintergrund ist der spätere Kontrast unbekannt. "
                        "Wähle --theme black oder --theme white ausdrücklich."
                    )
            metadata: dict[str, object] = {"source_format": source.format}
            if preserve_metadata:
                total_metadata_bytes = 0
                for key in ("icc_profile", "dpi", "exif"):
                    if key not in source.info:
                        continue
                    item_size = metadata_size(source.info[key])
                    if total_metadata_bytes + item_size <= MAX_METADATA_BYTES:
                        metadata[key] = source.info[key]
                        total_metadata_bytes += item_size
                if source.format == "PNG" and getattr(source, "text", None):
                    text: dict[str, str] = {}
                    for key, value in source.text.items():
                        if not isinstance(key, str) or not isinstance(value, str):
                            continue
                        item_size = metadata_size(key) + metadata_size(value)
                        if total_metadata_bytes + item_size > MAX_METADATA_BYTES:
                            continue
                        text[key] = value
                        total_metadata_bytes += item_size
                    if text:
                        metadata["png_text"] = text
            transposed = ImageOps.exif_transpose(source)
            return transposed.convert("RGBA"), metadata
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise SystemExit("Das Eingabebild ist für die sichere Verarbeitung zu groß.") from None
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise SystemExit(f"Das Eingabebild konnte nicht gelesen werden: {exc}") from None


def validate_output_directory_descriptor(descriptor: int) -> None:
    try:
        info = os.fstat(descriptor)
    except OSError as exc:
        raise SystemExit(f"Das Zielverzeichnis konnte nicht geprüft werden: {exc}") from None
    if not stat.S_ISDIR(info.st_mode):
        raise SystemExit("Das Zielverzeichnis ist kein reguläres Verzeichnis.")
    if hasattr(os, "geteuid") and info.st_uid != os.geteuid():
        raise SystemExit(
            "Das Zielverzeichnis ist nicht vertrauenswürdig: Es gehört nicht dem aktuellen Benutzer."
        )
    if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise SystemExit(
            "Das Zielverzeichnis ist nicht vertrauenswürdig: Gruppen- oder Welt-Schreibrechte sind aktiv."
        )


def normalized_exif(payload: object) -> Image.Exif:
    if not isinstance(payload, bytes):
        raise SystemExit("Die angeforderten EXIF-Metadaten konnten nicht sicher übernommen werden.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            exif = Image.Exif()
            exif.load(payload)
        # A non-empty EXIF payload that parses to no entries is corrupt or unsupported.
        if payload and not exif:
            raise ValueError("leere oder beschädigte EXIF-Struktur")
        exif.pop(274, None)
        serialized = exif.tobytes()
        verified = Image.Exif()
        verified.load(serialized)
        # Round-trip must preserve the same normalized mapping.
        if dict(verified) != dict(exif):
            raise ValueError("EXIF-Roundtrip ist nicht verlustfrei")
        return verified
    except (TypeError, ValueError, SyntaxError, struct.error, OverflowError, Warning):
        raise SystemExit(
            "Die angeforderten EXIF-Metadaten konnten nicht sicher übernommen werden."
        ) from None


def publish_atomic(
    rendered: Image.Image, output: Path, format_name: str, save_args: dict[str, object]
) -> None:
    """Encode and no-replace publish relative to one identity-bound directory descriptor."""
    output.parent.mkdir(parents=True, exist_ok=True)
    directory_descriptor: Optional[int] = None
    temporary_name: Optional[str] = None
    stream: Optional[object] = None
    try:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        directory_descriptor = os.open(output.parent, directory_flags)
        validate_output_directory_descriptor(directory_descriptor)
        if "/" in output.name or output.name in ("", ".", ".."):
            raise SystemExit("Ungültiger Ausgabedateiname.")

        for _ in range(20):
            candidate = f".{output.name}.{secrets.token_hex(12)}.tmp"
            try:
                temporary_descriptor = os.open(
                    candidate,
                    os.O_RDWR | os.O_CREAT | os.O_EXCL,
                    0o600,
                    dir_fd=directory_descriptor,
                )
                temporary_name = candidate
                break
            except FileExistsError:
                continue
        else:
            raise SystemExit("Temporäre Ausgabedatei konnte nicht sicher angelegt werden.")

        try:
            with os.fdopen(temporary_descriptor, "w+b") as opened_stream:
                stream = opened_stream
                rendered.save(opened_stream, format=format_name, **save_args)
                opened_stream.flush()
                os.fsync(opened_stream.fileno())
        finally:
            stream = None

        try:
            os.link(
                temporary_name,
                output.name,
                src_dir_fd=directory_descriptor,
                dst_dir_fd=directory_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError:
            raise SystemExit(
                f"Ausgabedatei existiert bereits und wird nicht überschrieben: {output}"
            ) from None
        except OSError as exc:
            raise SystemExit(
                "Die Ausgabe konnte nicht sicher und ohne Überschreiben veröffentlicht werden: "
                f"{exc}"
            ) from None
        os.fsync(directory_descriptor)
    except SystemExit:
        raise
    except OSError as exc:
        raise SystemExit(f"Die Ausgabedatei konnte nicht gespeichert werden: {exc}") from None
    finally:
        if temporary_name is not None and directory_descriptor is not None:
            try:
                os.unlink(temporary_name, dir_fd=directory_descriptor)
            except FileNotFoundError:
                pass
            except OSError:
                pass
        if directory_descriptor is not None:
            os.close(directory_descriptor)


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
    if output.exists() or output.is_symlink():
        raise SystemExit(f"Ausgabedatei existiert bereits und wird nicht überschrieben: {output}")
    suffix = output.suffix.lower()
    if suffix in (".jpg", ".jpeg", ".jpe", ".jfif"):
        format_name = "JPEG"
    elif suffix == ".webp":
        format_name = "WEBP"
    elif suffix == ".png":
        format_name = "PNG"
    else:
        raise SystemExit("Ausgabeformat muss PNG, JPEG oder WebP sein.")

    snapshot = snapshot_input(args.input)
    try:
        base, metadata = load_source_snapshot(
            snapshot, args.theme == "auto", args.preserve_metadata
        )
    finally:
        snapshot.close()

    if args.preserve_metadata and metadata["source_format"] != format_name:
        raise SystemExit(
            "--preserve-metadata ist nur bei Ausgabe im gleichen Format unterstützt; "
            "wähle die ursprüngliche Dateiendung oder entferne die Option."
        )

    probe_path = icon_path(args.kind, "black", args.opacity)
    if not probe_path.is_file():
        raise SystemExit(f"EU-Icon fehlt: {probe_path}")
    with Image.open(probe_path) as probe_source:
        probe_source.load()
        probe = probe_source.convert("RGBA")

    probe_size = scaled_size(probe, base, args.width)
    ensure_readable(probe, probe_size)
    margin = max(1, round(min(base.size) * args.margin))

    theme = args.theme
    if theme == "auto":
        brightness = local_luminance(base, args.position, probe_size, margin)
        theme = "black" if brightness >= 140 else "white"

    selected_path = icon_path(args.kind, theme, args.opacity)
    if not selected_path.is_file():
        raise SystemExit(f"EU-Icon fehlt: {selected_path}")
    with Image.open(selected_path) as icon_source:
        icon_source.load()
        selected = icon_source.convert("RGBA")
        target_size = scaled_size(selected, base, args.width)
        ensure_readable(selected, target_size)
        icon = selected.resize(target_size, Image.Resampling.LANCZOS)

    x, y = coordinates(args.position, base.size, icon.size, margin)
    base.alpha_composite(icon, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    save_args: dict[str, object] = {}
    if "icc_profile" in metadata:
        save_args["icc_profile"] = metadata["icc_profile"]
    if "dpi" in metadata:
        save_args["dpi"] = metadata["dpi"]
    if "exif" in metadata:
        save_args["exif"] = normalized_exif(metadata["exif"])

    if format_name == "JPEG":
        rendered = base.convert("RGB")
        save_args.update(quality=95, subsampling=0)
    elif format_name == "WEBP":
        rendered = base
        save_args.update(quality=95)
    else:
        rendered = base
        if "png_text" in metadata:
            pnginfo = PngImagePlugin.PngInfo()
            for key, value in metadata["png_text"].items():
                if isinstance(value, str):
                    pnginfo.add_text(key, value)
            save_args["pnginfo"] = pnginfo

    publish_atomic(rendered, output, format_name, save_args)

    print(f"Erstellt: {output}")
    print(f"Icon: {args.kind}, {theme}, {args.opacity}; Position: {args.position}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
