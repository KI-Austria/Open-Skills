from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import warnings
import zlib

from PIL import Image, PngImagePlugin


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "kennzeichnungspflicht" / "scripts" / "label_image.py"


def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
    )


class LabelImageTest(unittest.TestCase):
    def test_help_works(self) -> None:
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("50-Prozent-Variante", result.stdout)

    def test_creates_sibling_and_preserves_original(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "posting.png"
            Image.new("RGB", (1200, 800), "#f2f0eb").save(source)
            original_hash = hashlib.sha256(source.read_bytes()).hexdigest()

            result = run_cli(source, "--kind", "generated")

            output = Path(directory) / "posting-gekennzeichnet.png"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            self.assertIn("Erstellt:", result.stdout)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_hash)
            with Image.open(output) as rendered:
                self.assertEqual(rendered.size, (1200, 800))
            self.assertNotEqual(hashlib.sha256(output.read_bytes()).hexdigest(), original_hash)

    def test_refuses_to_overwrite_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "posting.png"
            output = Path(directory) / "posting-gekennzeichnet.png"
            Image.new("RGB", (600, 400), "white").save(source)
            output.write_bytes(b"keep")

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), b"keep")

    def test_refuses_dangling_output_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "posting.png"
            output = Path(directory) / "posting-gekennzeichnet.png"
            Image.new("RGB", (600, 400), "white").save(source)
            output.symlink_to(Path(directory) / "missing.png")

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(output.is_symlink())

    def test_refuses_unreadably_small_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tiny.png"
            Image.new("RGB", (20, 20), "white").save(source)

            result = run_cli(source, "--kind", "generated")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("zu klein", result.stderr + result.stdout)
            self.assertFalse((Path(directory) / "tiny-gekennzeichnet.png").exists())

    def test_rejects_animated_gif_instead_of_dropping_frames(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "animated.gif"
            frames = [Image.new("RGB", (300, 200), color) for color in ("red", "blue")]
            frames[0].save(source, save_all=True, append_images=frames[1:], duration=100, loop=0)

            result = run_cli(source, "--kind", "basic", "--output", Path(directory) / "out.png")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PNG, JPEG oder WebP", result.stderr + result.stdout)

    def test_corrupt_input_returns_human_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.png"
            source.write_bytes(b"not an image")

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("nicht gelesen", result.stderr + result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_accepts_jfif_as_jpeg_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "photo.jfif"
            Image.new("RGB", (1200, 800), "white").save(source, format="JPEG")

            result = run_cli(source, "--kind", "basic")

            output = Path(directory) / "photo-gekennzeichnet.jfif"
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(output) as rendered:
                self.assertEqual(rendered.format, "JPEG")

    def test_rejects_oversized_dimensions_before_decode(self) -> None:
        def chunk(kind: bytes, data: bytes) -> bytes:
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bomb.png"
            source.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", 20_000, 20_000, 8, 2, 0, 0, 0))
                + chunk(b"IEND", b"")
            )

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("zu groß", result.stderr + result.stdout)
            self.assertFalse((Path(directory) / "bomb-gekennzeichnet.png").exists())

    def test_rejects_oversized_input_file_before_decode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "large.png"
            with source.open("wb") as stream:
                stream.seek(100 * 1024 * 1024)
                stream.write(b"0")

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Dateigröße", result.stderr + result.stdout)

    def test_strips_all_metadata_including_icc_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "private.jpg"
            image = Image.new("RGB", (1200, 800), "white")
            exif = image.getexif()
            exif[315] = "Secret Author"
            secret_icc = b"ICC_PROFILE_SECRET_PERSONAL_IDENTIFIER_12345"
            image.save(source, exif=exif, dpi=(144, 144), icc_profile=secret_icc)

            result = run_cli(source, "--kind", "basic")

            self.assertEqual(result.returncode, 0, result.stderr)
            output = Path(directory) / "private-gekennzeichnet.jpg"
            with Image.open(output) as rendered:
                self.assertIsNone(rendered.getexif().get(315))
                self.assertNotIn("icc_profile", rendered.info)
                self.assertNotIn("dpi", rendered.info)
            self.assertNotIn(secret_icc, output.read_bytes())

    def test_preserve_metadata_rejects_cross_format_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "private.jpg"
            output = Path(directory) / "converted.webp"
            image = Image.new("RGB", (1200, 800), "white")
            exif = image.getexif()
            exif[315] = "Secret Author"
            image.save(source, exif=exif)

            result = run_cli(
                source,
                "--kind",
                "basic",
                "--output",
                output,
                "--preserve-metadata",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("gleichen Format", result.stderr + result.stdout)
            self.assertFalse(output.exists())

    def test_preserves_same_format_exif_for_jpeg_png_and_webp(self) -> None:
        for suffix, format_name in ((".jpg", "JPEG"), (".png", "PNG"), (".webp", "WEBP")):
            with self.subTest(format=format_name), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / f"source{suffix}"
                image = Image.new("RGB", (1200, 800), "white")
                exif = image.getexif()
                exif[315] = "Reviewed Author"
                exif[274] = 1
                image.save(source, format=format_name, exif=exif)

                result = run_cli(source, "--kind", "basic", "--preserve-metadata")

                self.assertEqual(result.returncode, 0, result.stderr)
                output = Path(directory) / f"source-gekennzeichnet{suffix}"
                with Image.open(output) as rendered:
                    self.assertEqual(rendered.getexif().get(315), "Reviewed Author")
                    self.assertNotEqual(rendered.getexif().get(274), 6)

    def test_snapshot_rejects_non_regular_input(self) -> None:
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO wird auf dieser Plattform nicht unterstützt")
        spec = importlib.util.spec_from_file_location("label_image_fifo_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            fifo = Path(directory) / "input.png"
            os.mkfifo(fifo)

            with self.assertRaises(SystemExit) as raised:
                module.snapshot_input(fifo)

            self.assertIn("reguläre Datei", str(raised.exception))

    def test_snapshot_is_immutable_after_source_replacement(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_snapshot_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.png"
            replacement = Path(directory) / "replacement.png"
            Image.new("RGB", (1200, 800), "white").save(source)
            snapshot = module.snapshot_input(source)
            source.unlink()
            Image.new("RGB", (2000, 1200), "black").save(replacement)
            replacement.rename(source)
            try:
                image, _ = module.load_source_snapshot(snapshot, False, False)
            finally:
                snapshot.close()
            self.assertEqual(image.size, (1200, 800))

    def test_preserves_metadata_only_when_explicitly_requested(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "document.png"
            info = PngImagePlugin.PngInfo()
            info.add_text("Description", "source")
            Image.new("RGB", (1200, 800), "white").save(source, pnginfo=info)

            result = run_cli(source, "--kind", "basic", "--preserve-metadata")

            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(Path(directory) / "document-gekennzeichnet.png") as rendered:
                self.assertEqual(rendered.text["Description"], "source")

    def test_rejects_untrusted_writable_output_directory(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_untrusted_output_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "shared"
            output_dir.mkdir(mode=0o777)
            output_dir.chmod(0o777)
            output = output_dir / "output.png"
            try:
                with self.assertRaises(SystemExit) as raised:
                    module.publish_atomic(Image.new("RGB", (20, 20)), output, "PNG", {})
                self.assertIn("nicht vertrauenswürdig", str(raised.exception))
                self.assertFalse(output.exists())
            finally:
                output_dir.chmod(0o700)

    def test_malformed_preserved_exif_fails_without_traceback_or_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "malformed.jpg"
            output = Path(directory) / "malformed-gekennzeichnet.jpg"
            Image.new("RGB", (1200, 800), "white").save(
                source, format="JPEG", exif=b"Exif\x00\x00II*\x00"
            )

            result = run_cli(source, "--kind", "basic", "--preserve-metadata")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("EXIF-Metadaten", result.stderr + result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(output.exists())

    def test_publish_is_anchored_to_open_directory_descriptor(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_dirfd_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trusted = root / "trusted"
            moved = root / "moved"
            attacker = root / "attacker"
            trusted.mkdir(mode=0o700)
            attacker.mkdir(mode=0o777)
            attacker.chmod(0o777)
            original_link = module.os.link

            def swap_then_link(src: object, dst: object, **kwargs: object) -> None:
                trusted.rename(moved)
                trusted.symlink_to(attacker, target_is_directory=True)
                original_link(src, dst, **kwargs)

            module.os.link = swap_then_link
            try:
                module.publish_atomic(
                    Image.new("RGB", (20, 20), "white"), trusted / "output.png", "PNG", {}
                )
            finally:
                module.os.link = original_link
                attacker.chmod(0o700)

            self.assertTrue((moved / "output.png").is_file())
            self.assertFalse((attacker / "output.png").exists())

    def test_warning_only_corrupt_exif_is_rejected(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_exif_warning_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        malformed = b"Exif\x00\x00II*\x00\x08\x00\x00\x00\x01\x00"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Payload is deliberately truncated but may be accepted by Pillow with a warning only.
            pass
        with self.assertRaises(SystemExit) as raised:
            module.normalized_exif(malformed)
        self.assertIn("EXIF-Metadaten", str(raised.exception))

    def test_type_invalid_nonempty_exif_is_rejected_before_encoding(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_exif_type_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        malformed = bytes.fromhex(
            "4578696600004d4d002a000000080003010e00020000000500000032"
            "01120003000000010006000001000002000000070000003800000000"
            "446573630000417574686f720000"
        )
        with self.assertRaises(SystemExit) as raised:
            module.normalized_exif(malformed)
        self.assertIn("EXIF-Metadaten", str(raised.exception))

    def test_failed_publish_leaves_no_partial_output(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_under_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class FailingImage:
            def save(self, stream: object, **_: object) -> None:
                stream.write(b"PARTIAL")
                raise OSError("simulated encoder failure")

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.png"
            with self.assertRaises(SystemExit) as raised:
                module.publish_atomic(FailingImage(), output, "PNG", {})

            self.assertIn("nicht gespeichert", str(raised.exception))
            self.assertFalse(output.exists())
            self.assertFalse(list(Path(directory).glob(".output.png.*.tmp")))

    def test_all_official_assets_scale_proportionally_without_cropping(self) -> None:
        spec = importlib.util.spec_from_file_location("label_image_assets_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        base = Image.new("RGBA", (1600, 1000), "white")

        for kind in module.KINDS:
            for theme in ("black", "white"):
                for opacity in ("solid", "half"):
                    with self.subTest(kind=kind, theme=theme, opacity=opacity):
                        path = module.icon_path(kind, theme, opacity)
                        with Image.open(path) as source:
                            icon = source.convert("RGBA")
                        target = module.scaled_size(icon, base, 0.32)
                        module.ensure_readable(icon, target)
                        source_ratio = icon.width / icon.height
                        target_ratio = target[0] / target[1]
                        tolerance = 1 / target[1]
                        self.assertAlmostEqual(source_ratio, target_ratio, delta=tolerance)
                        self.assertEqual(module.visible_bbox(icon), icon.getchannel("A").getbbox())

    def test_auto_theme_refuses_unknown_transparent_background(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "transparent.png"
            Image.new("RGBA", (800, 600), (0, 0, 0, 0)).save(source)

            result = run_cli(source, "--kind", "basic")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("transparent", (result.stderr + result.stdout).lower())

    def test_preserves_orientation_visually_but_strips_dpi_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "rotated.jpg"
            image = Image.new("RGB", (600, 1200), "white")
            exif = image.getexif()
            exif[274] = 6
            image.save(source, exif=exif, dpi=(144, 144))

            result = run_cli(source, "--kind", "basic", "--width", 0.5)

            output = Path(directory) / "rotated-gekennzeichnet.jpg"
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(output) as rendered:
                self.assertEqual(rendered.size, (1200, 600))
                self.assertNotEqual(rendered.getexif().get(274), 6)
                self.assertNotIn("dpi", rendered.info)

    def test_strips_png_dpi_and_text_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "print.png"
            info = PngImagePlugin.PngInfo()
            info.add_text("Description", "source")
            Image.new("RGB", (1200, 800), "white").save(source, dpi=(300, 300), pnginfo=info)

            result = run_cli(source, "--kind", "generated")

            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(Path(directory) / "print-gekennzeichnet.png") as rendered:
                self.assertNotIn("dpi", rendered.info)
                self.assertNotIn("Description", rendered.text)


if __name__ == "__main__":
    unittest.main()
