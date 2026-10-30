#!/usr/bin/env python3
"""Local integration-readiness QA for Midnight Pulse."""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "MidnightPulse.theme.css"
ASSET = ROOT / "assets" / "pokemon-discord-background.webp"
README = ROOT / "README.md"
QA_DOC = ROOT / "QA-CHECKLIST.md"

REQUIRED_META = ("@name", "@author", "@description", "@version")
REQUIRED_TOKENS = (
    "--pokemon-bg-main",
    "--pokemon-accent-primary",
    "--pokemon-accent-secondary",
    "--pokemon-bg-image",
    "--pokemon-bg-fallback",
    "--pokemon-bg-overlay",
    "--pokemon-focus-ring",
    "prefers-reduced-motion",
    "--background-primary",
    "--background-base-lowest",
    "--text-default",
)


def check_meta(css: str) -> list[str]:
    errors: list[str] = []
    if not css.lstrip().startswith("/**"):
        errors.append("Theme must start with a JSDoc meta block")
        return errors
    meta_end = css.find("*/")
    if meta_end == -1:
        errors.append("Meta block is not closed")
        return errors
    meta = css[: meta_end + 2]
    for field in REQUIRED_META:
        if field not in meta:
            errors.append(f"Missing required meta field: {field}")
    name = re.search(r"@name\s+(.+)", meta)
    version = re.search(r"@version\s+([\d.]+)", meta)
    if name and name.group(1).strip() != "MidnightPulse":
        errors.append(f"Unexpected @name value: {name.group(1).strip()!r}")
    if version and not re.fullmatch(r"\d+\.\d+\.\d+", version.group(1).strip()):
        errors.append(f"Unexpected @version value: {version.group(1).strip()!r}")
    if "MidnightPulse.theme.css" != THEME.name:
        errors.append("Theme filename must be MidnightPulse.theme.css for BD/Vencord")
    return errors


def check_css_balance(css: str) -> list[str]:
    errors: list[str] = []
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    depth = 0
    in_str: str | None = None
    i = 0
    while i < len(stripped):
        ch = stripped[i]
        if in_str:
            if ch == "\\" and i + 1 < len(stripped):
                i += 2
                continue
            if ch == in_str:
                in_str = None
        else:
            if ch in ('"', "'"):
                in_str = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    errors.append("Unmatched closing brace '}'")
                    return errors
        i += 1
    if in_str:
        errors.append(f"Unterminated string literal ({in_str})")
    if depth != 0:
        errors.append(f"Unbalanced braces; remaining depth={depth}")
    return errors


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def check_safety(css: str) -> list[str]:
    errors: list[str] = []
    code = strip_comments(css).lower()
    forbidden = [
        ("<script", "script tag"),
        ("javascript:", "javascript: URL"),
        ('@import url("http://', "insecure remote @import"),
        ("fetch(", "JS fetch"),
        ("xmlhttprequest", "XHR"),
        ("discord.com/api", "Discord API URL"),
    ]
    for needle, label in forbidden:
        if needle in code:
            errors.append(f"Unexpected content: {label}")
    urls = re.findall(r"url\(\s*['\"]?(https?://[^)'\"]+)", code, flags=re.I)
    if urls:
        errors.append(f"Unexpected remote url() references: {urls}")
    return errors


def check_asset_strategy(css: str) -> list[str]:
    errors: list[str] = []
    uri_hits = re.findall(r"data:image/webp;base64,([A-Za-z0-9+/=]+)", css)
    if len(uri_hits) != 1:
        errors.append(f"Expected exactly one embedded WebP data URI, found {len(uri_hits)}")
    match = re.search(
        r"--pokemon-bg-image:\s*url\(\s*\"(data:image/webp;base64,([A-Za-z0-9+/=]+))\"\s*\)\s*;",
        css,
    )
    if not match:
        errors.append("Expected embedded data:image/webp;base64 --pokemon-bg-image")
        return errors
    b64 = match.group(2)
    if len(b64) % 4 != 0:
        errors.append(f"Background Base64 length not divisible by 4: {len(b64)}")
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Background data URI is not valid base64: {exc}")
        return errors
    if raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
        errors.append("Embedded background is not a WebP payload")
    if not ASSET.is_file():
        errors.append(f"Source asset missing: {ASSET}")
    else:
        source = ASSET.read_bytes()
        if raw != source:
            errors.append("Embedded data URI does not match assets/pokemon-discord-background.webp")
        # Guard against embed-script duplication blowups (~48k b64 => theme ~70k chars).
        if len(css) > 100_000:
            errors.append(
                f"Theme file unexpectedly large ({len(css)} chars); possible duplicate embed"
            )
    if css.count("--pokemon-bg-image:") != 1:
        errors.append("Duplicate or missing --pokemon-bg-image declarations")
    if "--pokemon-bg-fallback" not in css or "--pokemon-bg-overlay" not in css:
        errors.append("Gradient overlay/fallback tokens missing")
    code = strip_comments(css)
    if "background-attachment: fixed" in code or "background-attachment:fixed" in code:
        errors.append("background-attachment:fixed should remain removed (Electron issues)")
    return errors


def check_docs() -> list[str]:
    errors: list[str] = []
    if not README.is_file():
        errors.append("Missing README.md")
        return errors
    text = README.read_text(encoding="utf-8")
    required_snippets = [
        "BetterDiscord",
        "Vencord",
        "UNVERIFIED",
        "gradient",
        "Disable",
        "background",
        "Terms of Service",
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"README missing expected guidance containing: {snippet}")
    return errors


def main() -> int:
    failures: list[str] = []
    print(f"ROOT: {ROOT}")

    if not THEME.is_file():
        failures.append(f"Missing theme file: {THEME}")
    if not ASSET.is_file():
        failures.append(f"Missing asset: {ASSET}")
    else:
        print(f"ASSET OK: {ASSET.name} ({ASSET.stat().st_size} bytes)")
        if ASSET.stat().st_size > 1_500_000:
            failures.append(f"Asset larger than expected budget: {ASSET.stat().st_size} bytes")
    if not QA_DOC.is_file():
        failures.append("Missing QA-CHECKLIST.md")

    if THEME.is_file():
        css = THEME.read_text(encoding="utf-8")
        print(f"THEME OK: {THEME.name} ({len(css)} chars)")
        for err in check_meta(css):
            failures.append(err)
        for err in check_css_balance(css):
            failures.append(err)
        for err in check_safety(css):
            failures.append(err)
        for err in check_asset_strategy(css):
            failures.append(err)
        for token in REQUIRED_TOKENS:
            if token not in css:
                failures.append(f"Missing expected token/feature: {token}")
        # Overly broad username force-color should stay removed
        if re.search(r"\[class\*=\"username_\"\]\s*\{[^}]*color:", css):
            failures.append("Username color override present; role colors would break")

    for err in check_docs():
        failures.append(err)

    if failures:
        print("\nQA FAILURES:")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("\nQA PASSED: structural + asset-strategy checks OK")
    print("NOTE: Live BetterDiscord/Vencord client integration remains UNVERIFIED here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
