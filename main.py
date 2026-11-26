#!/usr/bin/env python3
"""Funniest Sign on a Haunted Server Room Door — make.fun entry.

The program writes exactly one funny sign for the door of a haunted server
room, at most 120 characters, to /output/entry.txt, and prints it to stdout.

Deterministic: identical output on every run. No network, no secrets,
no input files, no randomness: the sign is a literal in this file.
"""

import os
import re
from pathlib import Path

SIGN = (
    "NOTICE: Rack 9 was decommissioned in 2019. "
    "It still answers pings. Do not talk to it."
)

MAX_CHARS = 120

# A sign speaks in sign voice: an imperative or a posted notice. A bare
# third-person narrative ("The ghost does X") is not a sign, so the line
# must open with a sign marker. This is the third-person guard.
SIGN_OPENERS = (
    "WARNING:", "NOTICE:", "DO NOT", "PLEASE", "IF ", "NO ",
    "AUTHORIZED", "KNOCK", "KEEP", "ENTER", "LEAVE", "SHOUT",
)

DIALOGUE_TAGS = (
    "said", "asked", "whispered", "shouted", "replied", "murmured",
    "cried", "yelled", "answered",
)

JUDGE_WORDS = ("judge", "pick me", "vote for", "choose me", "dear reader")

MARKDOWN_CHARS = set("#*_`[]")


def validate(line: str) -> None:
    """Raise ValueError on any banned pattern. The winning line passes all."""
    if not line or not line.strip():
        raise ValueError("empty line")
    if "\n" in line or "\r" in line:
        raise ValueError("two-line line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"over-limit line: {len(line)} > {MAX_CHARS}")
    if re.search(r"https?://|www\.", line):
        raise ValueError("link in line")
    if any(ch in MARKDOWN_CHARS for ch in line):
        raise ValueError("markdown in line")
    stripped = line.strip()
    if stripped.startswith(('"', "'")) or stripped.endswith(('"', "'")):
        raise ValueError("quoted line")
    low = line.lower()
    if any(re.search(r"\b" + tag + r"\b", low) for tag in DIALOGUE_TAGS):
        raise ValueError("dialogue tag in line")
    if any(word in low for word in JUDGE_WORDS):
        raise ValueError("judge-addressed line")
    if not any(low.startswith(op.lower()) for op in SIGN_OPENERS):
        raise ValueError("third-person line: no sign opener")


def main() -> None:
    validate(SIGN)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out = Path(out_dir) / "entry.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(SIGN, encoding="utf-8")
    # Self-check: read the file back and confirm it holds exactly the sign.
    if out.read_bytes() != SIGN.encode("utf-8"):
        raise SystemExit("entry.txt does not match the sign literal")
    print(SIGN)


if __name__ == "__main__":
    main()
