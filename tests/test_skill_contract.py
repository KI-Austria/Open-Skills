from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "kennzeichnungspflicht"


class SkillContractTest(unittest.TestCase):
    def test_two_step_safety_contract_is_explicit(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        required_phrases = (
            "typischerweise null bis zwei und niemals mehr als drei",
            "Verwandle die Prüfung nicht in ein Interview",
            "Füge in Schritt 1 nichts ein",
            "Erst nach ausdrücklicher Freigabe",
            "überschreibe das Original nicht",
            "keine Rechtsberatung",
        )
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_all_twelve_eu_icon_files_are_present(self) -> None:
        icons = list((SKILL_DIR / "assets" / "eu-icons").glob("*.png"))
        self.assertEqual(len(icons), 12)

    def test_legal_reference_uses_primary_sources(self) -> None:
        text = (SKILL_DIR / "references" / "eu-baseline.md").read_text(encoding="utf-8")
        self.assertIn("eur-lex.europa.eu", text)
        self.assertIn("digital-strategy.ec.europa.eu", text)


if __name__ == "__main__":
    unittest.main()
