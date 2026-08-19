from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "kennzeichnungspflicht"


class SkillContractTest(unittest.TestCase):
    def test_knowledge_worker_fast_path_is_explicit(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        required_phrases = (
            "Schnellpfad für Wissensarbeit",
            "berufliche Einzelkorrespondenz",
            "organisationsinterne Kommunikation",
            "Normadressat",
            "Nur vor einer tatsächlichen Änderung",
            "einschließlich Fakten substanziell geprüft",
            "Bei Übersetzung oder Stilbearbeitung eines öffentlichen Informationstexts",
            "zuerst sämtliche Tatbestandsmerkmale prüfen",
            "Fehlt eines, liegt dieser Textfall regelmäßig nicht vor",
            "durch eine verantwortliche Redaktion einschließlich Fakten und Quellenvertrauenswürdigkeit",
            "imperative Anweisung",
            "anwendbare Barrierefreiheit",
        )
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_clear_fast_paths_do_not_load_legal_references(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text), 8000)
        self.assertNotIn("Lies vor der Prüfung [references/eu-baseline.md]", text)
        for phrase in (
            "Schnellpfad für Wissensarbeit – zuerst und ohne Referenzdatei",
            "Lade die Rechtsbaseline erst",
            "Lade Praxisfälle nur",
            "Lade die Icon-Auswahl nur",
            "Lade das Bild-Setup nur",
            "Antworte in höchstens drei kurzen Zeilen",
        ):
            self.assertIn(phrase, text)

    def test_fast_path_clearance_is_global_and_fail_closed(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "schließt nur den öffentlichen Textpfad aus",
            "schließt nur die direkte KI-Interaktion aus",
            "nicht bei öffentlichem Newsletter, Posting oder öffentlicher Information stoppen",
            "erst wenn anhand des bekannten Kontexts auch Deepfake",
            "Emotionserkennung, biometrische Kategorisierung und Anbieterpflicht nach Absatz 2 ausgeschlossen sind",
            "Keine Kennzeichnung nach Art. 50 nötig",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("Deepfakes, direkte KI-Interaktion, Verträge und interne Regeln separat prüfen.", text)
        self.assertNotIn("Bei `regelmäßig nicht erforderlich` schließe ab", text)

    def test_media_references_are_routed_separately(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        icon_rule = next(line for line in text.splitlines() if "Lade die Icon-Auswahl nur" in line)
        setup_rule = next(line for line in text.splitlines() if "Lade das Bild-Setup nur" in line)
        self.assertIn("icon-selection.md", icon_rule)
        self.assertNotIn("image-setup.md", icon_rule)
        self.assertIn("image-setup.md", setup_rule)
        self.assertNotIn("icon-selection.md", setup_rule)

    def test_mutation_gate_is_explicit_but_not_required_for_advice(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Nur vor einer tatsächlichen Änderung", text)
        self.assertNotIn("Arbeite immer in zwei getrennten Schritten", text)
        self.assertIn("Überschreibe das Original nicht", text)
        self.assertIn("keine Rechtsberatung", text)

    def test_legal_boundary_and_responsibility_are_preserved(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "keine Rechtsberatung, Compliance-Garantie oder Haftungsfreistellung",
            "Nicht allein verwenden",
            "Verantwortung für Einordnung, Nutzung und Veröffentlichung bleibt bei der handelnden Person oder Organisation",
            "Bei `unklar` keine Änderung durchführen, auch nicht mit vorab erteilter Mutationsfreigabe",
            "fachkundige oder rechtliche Prüfung empfehlen",
        ):
            self.assertIn(phrase, text)

    def test_unclear_result_overrides_prior_mutation_approval(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "Bei `unklar` keine Änderung durchführen, auch nicht mit vorab erteilter Mutationsfreigabe",
            text,
        )
        self.assertIn("„prüfe und kennzeichne“", text)
        self.assertNotIn("Bei `unklar` keine Freigabe ableiten", text)

    def test_human_review_and_editorial_control_are_alternatives(self) -> None:
        text = (SKILL_DIR / "references" / "eu-baseline.md").read_text(encoding="utf-8")
        self.assertIn("eine der beiden folgenden Kontrollformen", text)
        self.assertIn("die Faktenprüfung gehört mindestens dazu", text)
        self.assertIn("dazu gehören Faktenprüfung und die Prüfung", text)
        self.assertIn("Prüfung der Vertrauenswürdigkeit verwendeter Quellen", text)
        self.assertIn("letztendlichen rechtlichen Verantwortung für die Veröffentlichung", text)
        self.assertNotIn("Faktenprüfung und Prüfung der Quellenvertrauenswürdigkeit gehören mindestens dazu", text)
        self.assertIn("Bloße interne Zuständigkeit", text)
        self.assertNotIn("Die Offenlegung entfällt nur, wenn kumulativ:\n\n- fachkundige", text)

    def test_imperative_check_and_label_is_mutation_approval(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("„prüfe und kennzeichne“", text)
        self.assertIn("gilt als Mutationsfreigabe", text)
        self.assertNotIn("„prüfe und kennzeichne“ ohne ausdrücklichen Änderungsauftrag genügt nicht", text)

    def test_law_enforcement_exceptions_are_paragraph_specific(self) -> None:
        text = (SKILL_DIR / "references" / "eu-baseline.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("Absatzspezifische Strafverfolgungsausnahme"), 4)
        self.assertGreaterEqual(text.count("konkreten Einsatz"), 3)
        self.assertGreaterEqual(text.count("angemessene Schutzvorkehrungen"), 4)
        self.assertGreaterEqual(text.count("Dual-Use-Systems"), 3)
        self.assertIn("Öffentlichkeit zur Anzeige einer Straftat", text)
        self.assertIn("Diese Anbieterpflicht entfällt", text)
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Übertrage eine Ausnahme nie pauschal", skill)

    def test_article_50_2_transition_is_current_and_narrow(self) -> None:
        text = (SKILL_DIR / "references" / "eu-baseline.md").read_text(encoding="utf-8")
        for phrase in (
            "Verordnung (EU) 2026/1744",
            "Art. 111 Abs. 4",
            "vor dem 2. August 2026",
            "bis 2. Dezember 2026",
            "ausschließlich Absatz 2",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("Art. 50 ist seit 2. August 2026 anwendbar.", text)

    def test_all_twelve_eu_icon_files_are_present_and_named(self) -> None:
        expected = {
            f"LABEL_AI{suffix}_{theme}{opacity}.png"
            for suffix in ("", " GENERATED", " MODIFIED")
            for theme in ("black", "white")
            for opacity in ("", " transparent")
        }
        actual = {path.name for path in (SKILL_DIR / "assets" / "eu-icons").glob("*.png")}
        self.assertEqual(actual, expected)

    def test_legal_reference_has_actor_and_publication_rules(self) -> None:
        text = (SKILL_DIR / "references" / "eu-baseline.md").read_text(encoding="utf-8")
        for phrase in (
            "Anbieter",
            "Betreiber/Deployer",
            "Nicht als veröffentlicht",
            "berufliche Einzelkorrespondenz",
            "Faktenprüfung",
            "rein persönlichen und nicht beruflichen",
            "tatsächlich im Rahmen einer substanziellen Prüfung ausgeübt",
            "letztendlichen rechtlichen Verantwortung für die Veröffentlichung",
            "Barrierefreiheitsanforderungen",
        ):
            self.assertIn(phrase, text)

    def test_skill_package_contains_runtime_and_provenance_files(self) -> None:
        self.assertTrue((SKILL_DIR / "requirements.txt").is_file())
        self.assertTrue((SKILL_DIR / "LICENSE").is_file())
        self.assertTrue((SKILL_DIR / "THIRD_PARTY_NOTICES.md").is_file())
        self.assertTrue((SKILL_DIR / "references" / "work-examples.md").is_file())

    def test_frontmatter_and_relative_links_are_valid(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter, body = text[4:].split("\n---\n", 1)
        self.assertRegex(frontmatter, r"(?m)^name: kennzeichnungspflicht$")
        description = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" not in target:
                self.assertTrue((SKILL_DIR / target).is_file(), target)


if __name__ == "__main__":
    unittest.main()
