from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_catalog.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_catalog", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_runtime_skill_has_one_external_manifest() -> None:
    skill_slugs = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    manifest_slugs = {path.stem for path in (ROOT / "catalog" / "skills").glob("*.json")}
    assert manifest_slugs == skill_slugs


def test_catalog_is_deterministic_and_current() -> None:
    builder = load_builder()
    expected = builder.render()
    actual = (ROOT / "catalog" / "catalog.json").read_text(encoding="utf-8")
    assert actual == expected
    payload = json.loads(actual)
    assert payload["schema_version"] == 1
    assert [entry["slug"] for entry in payload["skills"]][0] == "kennzeichnungspflicht"


def test_runtime_packages_contain_no_website_manifests() -> None:
    forbidden_names = {"website.json", "catalog.json", "homepage.json"}
    for path in (ROOT / "skills").rglob("*"):
        assert path.name not in forbidden_names, path


def test_website_copy_is_not_duplicated_into_runtime_skill() -> None:
    for manifest_path in (ROOT / "catalog" / "skills").glob("*.json"):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "skills" / manifest["slug"]).rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"}
        )
        website_only = [manifest["preview"], manifest["task"], manifest["answer"], *manifest["steps"]]
        for text in website_only:
            assert text not in runtime_text, f"website copy leaked into skills/{manifest['slug']}"
