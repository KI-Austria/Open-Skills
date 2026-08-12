from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "kennzeichnungspflicht" / "scripts" / "label_image.py"


class LabelImageTest(unittest.TestCase):
    def test_creates_sibling_and_preserves_original(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "posting.png"
            Image.new("RGB", (1200, 800), "#f2f0eb").save(source)
            original_hash = hashlib.sha256(source.read_bytes()).hexdigest()

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--kind", "generated"],
                check=True,
                capture_output=True,
                text=True,
            )

            output = Path(directory) / "posting-gekennzeichnet.png"
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

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--kind", "basic"],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
