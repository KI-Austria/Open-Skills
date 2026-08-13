from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kennzeichnungspflicht" / "SKILL.md"


def routing_contract() -> dict[str, object]:
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(r"```json routing-contract\n(.*?)\n```", text, re.DOTALL)
    assert match, "routing-contract missing from SKILL.md"
    return json.loads(match.group(1))


def route(case: dict[str, bool]) -> tuple[set[str], bool]:
    contract = routing_contract()
    remaining = set(contract["branches"])
    for signal, excluded in contract["signals"].items():
        if case.get(signal, False):
            remaining.difference_update(excluded)
    return remaining, not remaining


def test_personal_human_sent_email_can_clear_globally() -> None:
    remaining, cleared = route(
        {
            "assistance_only": True,
            "not_public": True,
            "human_mediated": True,
            "no_synthetic_media": True,
            "no_emotion_or_biometrics": True,
            "no_provider_content_system": True,
        }
    )
    assert cleared
    assert remaining == set()


def test_public_human_sent_newsletter_keeps_public_text_branch() -> None:
    remaining, cleared = route(
        {
            "human_mediated": True,
            "no_synthetic_media": True,
            "no_emotion_or_biometrics": True,
            "no_provider_content_system": True,
        }
    )
    assert not cleared
    assert remaining == {"public_text"}


def test_internal_deepfake_keeps_deepfake_branch() -> None:
    remaining, cleared = route(
        {
            "not_public": True,
            "human_mediated": True,
            "no_emotion_or_biometrics": True,
            "no_provider_content_system": True,
        }
    )
    assert not cleared
    assert remaining == {"deepfake"}


def test_closed_autonomous_chat_keeps_direct_interaction_branch() -> None:
    remaining, cleared = route(
        {
            "not_public": True,
            "no_synthetic_media": True,
            "no_emotion_or_biometrics": True,
            "no_provider_content_system": True,
        }
    )
    assert not cleared
    assert remaining == {"direct_interaction"}


def test_no_partial_signal_can_clear_globally() -> None:
    contract = routing_contract()
    for signal in contract["signals"]:
        remaining, cleared = route({signal: True})
        assert not cleared, signal
        assert remaining, signal