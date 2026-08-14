from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "wo-stehen-wir"


class WoStehenWirContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.template = (SKILL_DIR / "references" / "abschluss-vorlage.md").read_text(
            encoding="utf-8"
        )

    def test_frontmatter_and_trigger_are_explicit(self) -> None:
        self.assertTrue(self.skill.startswith("---\n"))
        frontmatter, _ = self.skill[4:].split("\n---\n", 1)
        self.assertRegex(frontmatter, r"(?m)^name: wo-stehen-wir$")
        for phrase in (
            "sichtbarer Todo-Liste mit Checkboxen",
            "getan, gebaut, geprüft oder entschieden",
            "sichtbare Todos",
            "Wo stehen wir?",
            "Wo sind wir?",
            "Wo stehn wir?",
            "Was ist erledigt?",
            "Was fehlt noch?",
            "Wie geht es weiter?",
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

    def _final_templates(self) -> list[str]:
        return re.findall(r"```markdown\n(.*?)\n```", self.template, flags=re.DOTALL)

    def test_required_final_zones_and_order_are_contractual(self) -> None:
        for phrase in (
            "Schließe die Antwort als visuell klar erkennbaren Ergebnisblock ab.",
            "Der Block muss beim Überfliegen sofort auffindbar sein.",
            "eine TL;DR-Kurzfassung mit **genau einem Satz**",
            "einen sichtbaren Stand",
            "eine Entscheidungszone",
            "Nichts mehr zu tun.",
        ):
            self.assertIn(phrase, self.skill)

        templates = self._final_templates()
        self.assertEqual(len(templates), 2)
        for output in templates:
            with self.subTest(output=output[:80]):
                self.assertEqual(output.count("**Kurz gesagt:**"), 1)
                self.assertEqual(output.count("**Ergebnis**"), 1)
                self.assertEqual(output.count("**Stand**"), 1)
                self.assertEqual(output.count("**Deine Entscheidung**"), 1)
                ordered = [
                    output.index("**Kurz gesagt:**"),
                    output.index("**Ergebnis**"),
                    output.index("**Stand**"),
                    output.index("**Deine Entscheidung**"),
                ]
                self.assertEqual(ordered, sorted(ordered))
                self.assertNotIn("━━━━━━━━", output)
                self.assertNotIn("**Thema:", output)

    def test_visible_checkbox_states_are_present(self) -> None:
        for marker in ("- [x]", "- [ ]"):
            self.assertIn(marker, self.skill)
            self.assertIn(marker, self.template)
        checkbox_lines = [
            line for line in self.template.splitlines() if re.match(r"^\s*- \[", line)
        ]
        self.assertTrue(checkbox_lines)
        for line in checkbox_lines:
            with self.subTest(checkbox=line):
                self.assertRegex(line, r"^\s*- \[(?:x| )\](?:\s|$)")
        self.assertIn("AKTIV/BLOCKIERT", self.skill)
        self.assertIn("AKTIV/BLOCKIERT", self.template)
        self.assertIn("Interne Tool-Todos zählen nicht als sichtbar", self.skill)

    def test_completed_and_blocked_templates_cannot_contradict_each_other(self) -> None:
        completed, blocked = self.template.split("## Variante B: Echte Nutzersperre", 1)
        self.assertIn("## Variante A: Auftrag vollständig erledigt", completed)
        self.assertIn("Nichts mehr zu tun.", completed)
        self.assertNotIn("- [ ]", completed)
        self.assertNotIn("AKTIV/BLOCKIERT", completed)
        self.assertIn("- [ ]", blocked)
        self.assertEqual(blocked.count("- [ ] **AKTIV/BLOCKIERT:"), 1)
        self.assertNotIn("- [x] **AKTIV/BLOCKIERT:", blocked)
        self.assertIn("Empfehlung:", blocked)
        self.assertNotIn("Nichts mehr zu tun.", blocked)

    def test_visual_frame_stays_adaptive(self) -> None:
        self.assertIn("### <stabiler Themenname>", self.template)
        self.assertIn("kein starres Layout", self.template)
        self.assertIn("keine langen Unicode-Balken", self.skill)
        self.assertIn("wiederhole den Themennamen nicht dekorativ am Ende", self.skill)
        self.assertIn("genau einem Satz", self.skill)

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
