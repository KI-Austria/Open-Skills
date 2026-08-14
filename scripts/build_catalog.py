#!/usr/bin/env python3
"""Validate website manifests and build the public Open-Skills catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_DIR = ROOT / "catalog" / "skills"
OUTPUT = ROOT / "catalog" / "catalog.json"
REQUIRED_TEXT = (
    "title",
    "subtitle",
    "description",
    "preview",
    "task",
    "answer",
)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", text)
    if not match:
        raise ValueError(f"{path}: frontmatter field 'name' is missing")
    return match.group(1)


def load_manifests() -> list[dict[str, object]]:
    skill_slugs = {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}
    manifest_paths = sorted(MANIFEST_DIR.glob("*.json"))
    manifest_slugs = {path.stem for path in manifest_paths}

    missing = sorted(skill_slugs - manifest_slugs)
    extra = sorted(manifest_slugs - skill_slugs)
    if missing:
        raise ValueError(f"website manifest missing for: {', '.join(missing)}")
    if extra:
        raise ValueError(f"website manifest without skill: {', '.join(extra)}")

    entries: list[dict[str, object]] = []
    orders: set[int] = set()
    for path in manifest_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        slug = data.get("slug")
        if slug != path.stem or not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            raise ValueError(f"{path}: slug must match filename")
        skill_name = frontmatter_name(SKILLS_DIR / slug / "SKILL.md")
        if skill_name != slug:
            raise ValueError(f"{path}: slug does not match SKILL.md name '{skill_name}'")
        if data.get("schema_version") != 1:
            raise ValueError(f"{path}: schema_version must be 1")
        order = data.get("order")
        if not isinstance(order, int) or order < 0 or order in orders:
            raise ValueError(f"{path}: order must be a unique non-negative integer")
        orders.add(order)
        for field in REQUIRED_TEXT:
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{path}: '{field}' must be non-empty text")
        steps = data.get("steps")
        if not isinstance(steps, list) or len(steps) != 3 or not all(
            isinstance(step, str) and step.strip() for step in steps
        ):
            raise ValueError(f"{path}: 'steps' must contain exactly three texts")
        forbidden = set(data) - {
            "schema_version", "slug", "order", *REQUIRED_TEXT, "steps"
        }
        if forbidden:
            raise ValueError(f"{path}: unsupported fields: {', '.join(sorted(forbidden))}")
        entries.append(data)

    return sorted(entries, key=lambda entry: (entry["order"], entry["slug"]))


def render() -> str:
    payload = {
        "schema_version": 1,
        "generated_from": "catalog/skills/*.json",
        "skills": load_manifests(),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if catalog.json is stale")
    args = parser.parse_args()
    try:
        expected = render()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"catalog error: {error}", file=sys.stderr)
        return 1

    if args.check:
        actual = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if actual != expected:
            print("catalog/catalog.json is stale; run python scripts/build_catalog.py", file=sys.stderr)
            return 1
        print("catalog is valid and current")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
