from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "lesbares-antwortformat"


class LesbaresAntwortformatContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.template = (SKILL_DIR / "references" / "abschluss-vorlage.md").read_text(
            encoding="utf-8"
        )

    def test_frontmatter_and_trigger_are_explicit(self) -> None:
        self.assertTrue(self.skill.startswith("---\n"))
        frontmatter, _ = self.skill[4:].split("\n---\n", 1)
        self.assertRegex(frontmatter, r"(?m)^name: lesbares-antwortformat$")
        for phrase in (
            "sichtbarer Todo-Liste mit Checkboxen",
            "getan, gebaut, geprüft oder entschieden",
            "sichtbare Todos",
        ):
            self.assertIn(phrase, frontmatter)

    def test_completion_gate_prevents_mid_work_reports(self) -> None:
        for phrase in (
            "Wenn noch ein klarer nächster Schritt ausführbar ist, arbeite weiter",
            "Setze dabei keinen Abschluss-Block",
            "der Auftrag vollständig abgearbeitet ist",
            "eine echte Sperre besteht",
            "Eine reine Zwischenfrage braucht keinen Abschluss-Block",
        ):
            self.assertIn(phrase, self.skill)

    def test_required_final_zones_and_order_are_contractual(self) -> None:
        for phrase in (
            "# TL;DR",
            "**Gebaut**",
            "**Stand**",
            "**Deine Entscheidung**",
            "Nichts mehr zu tun.",
            "Nach dem Schlusstrenner kommt nichts mehr.",
        ):
            self.assertIn(phrase, self.skill)

        ordered = [
            self.template.index("# TL;DR"),
            self.template.index("**Gebaut**"),
            self.template.index("**Stand**"),
            self.template.index("**Deine Entscheidung**"),
        ]
        self.assertEqual(ordered, sorted(ordered))

    def test_visible_checkbox_states_are_present(self) -> None:
        for marker in ("- [x]", "- [>]", "- [ ]"):
            self.assertIn(marker, self.skill)
            self.assertIn(marker, self.template)
        self.assertIn("Interne Tool-Todos zählen nicht als sichtbar", self.skill)

    def test_completed_and_blocked_templates_cannot_contradict_each_other(self) -> None:
        completed, blocked = self.template.split("## Variante B: Echte Nutzersperre", 1)
        self.assertIn("## Variante A: Auftrag vollständig erledigt", completed)
        self.assertIn("Nichts mehr zu tun.", completed)
        self.assertNotIn("- [ ]", completed)
        self.assertNotIn("- [>]", completed)
        self.assertIn("- [>]", blocked)
        self.assertIn("- [ ]", blocked)
        self.assertIn("Empfehlung:", blocked)
        self.assertNotIn("Nichts mehr zu tun.", blocked)

    def test_theme_frame_and_single_sentence_tldr_are_explicit(self) -> None:
        self.assertIn("Thema: <stabiler Themenname>", self.template)
        self.assertIn("Thema: <derselbe stabile Themenname>", self.template)
        self.assertIn("genau einem Satz", self.skill)
        self.assertIn("Anfangs- und Schlussthema identisch", self.skill)

    def test_decision_zone_does_not_invent_work(self) -> None:
        for phrase in (
            "Erfinde keine Nutzerentscheidung",
            "Ist nichts offen: exakt `Nichts mehr zu tun.`",
            "Empfehlung:",
        ):
            self.assertIn(phrase, self.skill)

    def test_reference_link_resolves(self) -> None:
        targets = re.findall(r"\]\((references/[^)]+\.md)\)", self.skill)
        self.assertEqual(targets, ["references/abschluss-vorlage.md"])
        self.assertTrue((SKILL_DIR / targets[0]).is_file())


if __name__ == "__main__":
    unittest.main()
