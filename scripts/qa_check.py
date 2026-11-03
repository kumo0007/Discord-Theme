#!/usr/bin/env python3
"""Local integration-readiness QA for Midnight Pulse."""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "MidnightPulse.theme.css"
README = ROOT / "README.md"
QA_DOC = ROOT / "QA-CHECKLIST.md"

ASSETS = {
    "main": ROOT / "assets" / "pokemon-discord-background.webp",
    "guild": ROOT / "assets" / "pokemon-guild-panel.webp",
    "members": ROOT / "assets" / "pokemon-members-panel.webp",
    "chat": ROOT / "assets" / "pokemon-chat-accent.webp",
}

VAR_FOR_KEY = {
    "main": "--pokemon-bg-image",
    "guild": "--pokemon-guild-image",
    "members": "--pokemon-members-image",
    "chat": "--pokemon-chat-accent-image",
}

REQUIRED_META = ("@name", "@author", "@description", "@version")
REQUIRED_TOKENS = (
    "--pokemon-bg-main",
    "--pokemon-accent-primary",
    "--pokemon-accent-secondary",
    "--pokemon-bg-image",
    "--pokemon-guild-image",
    "--pokemon-members-image",
    "--pokemon-chat-accent-image",
    "--pokemon-bg-fallback",
    "--pokemon-bg-overlay",
    "--pokemon-star-dust",
    "--pokemon-chat-readability",
    "--pokemon-message-scrim",
    "--pokemon-message-scrim-hover",
    "--pokemon-panel-scrim",
    "--pokemon-focus-ring",
    "prefers-reduced-motion",
    "--background-primary",
    "--background-base-lowest",
    "--text-default",
    "ARTWORK:main",
    "ARTWORK:guild",
    "ARTWORK:members",
    "ARTWORK:chat",
)

# Multi-character embeds: ~280KB theme is expected; guard against runaway duplication.
MAX_THEME_CHARS = 520_000
MAX_ASSET_BYTES = 180_000


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


def check_one_embed(css: str, key: str, asset: Path, var_name: str) -> list[str]:
    errors: list[str] = []
    pattern = re.compile(
        rf"/\* ARTWORK:{re.escape(key)}\b.*?\*/\s*{re.escape(var_name)}:\s*url\(\s*\"(data:image/webp;base64,([A-Za-z0-9+/=]+))\"\s*\)\s*;",
        flags=re.S,
    )
    match = pattern.search(css)
    if not match:
        errors.append(f"Expected ARTWORK:{key} embedded data URI for {var_name}")
        return errors
    b64 = match.group(2)
    if len(b64) % 4 != 0:
        errors.append(f"{key}: Base64 length not divisible by 4: {len(b64)}")
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{key}: data URI is not valid base64: {exc}")
        return errors
    if raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
        errors.append(f"{key}: embedded payload is not WebP")
    if not asset.is_file():
        errors.append(f"Source asset missing: {asset}")
    else:
        if raw != asset.read_bytes():
            errors.append(f"{key}: embedded data URI does not match {asset.name}")
        if asset.stat().st_size > MAX_ASSET_BYTES:
            errors.append(f"{key}: asset larger than budget ({asset.stat().st_size} bytes)")
    if css.count(f"{var_name}:") != 1:
        errors.append(f"Duplicate or missing {var_name} declarations")
    return errors


def check_asset_strategy(css: str) -> list[str]:
    errors: list[str] = []
    uri_hits = re.findall(r"data:image/webp;base64,([A-Za-z0-9+/=]+)", css)
    if len(uri_hits) != len(ASSETS):
        errors.append(
            f"Expected exactly {len(ASSETS)} embedded WebP data URIs, found {len(uri_hits)}"
        )
    for key, asset in ASSETS.items():
        errors.extend(check_one_embed(css, key, asset, VAR_FOR_KEY[key]))
    if len(css) > MAX_THEME_CHARS:
        errors.append(
            f"Theme file unexpectedly large ({len(css)} chars); possible duplicate embed"
        )
    for token in ("--pokemon-bg-fallback", "--pokemon-bg-overlay",
    "--pokemon-star-dust", "--pokemon-chat-readability"):
        if token not in css:
            errors.append(f"Missing atmosphere token: {token}")
    code = strip_comments(css)
    if "background-attachment: fixed" in code or "background-attachment:fixed" in code:
        errors.append("background-attachment:fixed should remain removed (Electron issues)")
    return errors


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_contrast(css: str) -> list[str]:
    errors: list[str] = []
    # Spot-check design tokens (solid colors) for body text readability.
    pairs = [
        ("--pokemon-text-primary", "--pokemon-bg-main", 6.0),
        ("--pokemon-text-secondary", "--pokemon-bg-secondary", 4.5),
        ("--pokemon-text-muted", "--pokemon-bg-main", 3.0),
        ("--pokemon-text-link", "--pokemon-bg-main", 4.5),
    ]
    values: dict[str, str] = {}
    for token, _, _ in pairs:
        m = re.search(rf"{re.escape(token)}:\s*(#[0-9a-fA-F]{{6}})", css)
        if not m:
            errors.append(f"Missing solid color for contrast check: {token}")
            continue
        values[token] = m.group(1)
    for bg_token in ("--pokemon-bg-main", "--pokemon-bg-secondary"):
        m = re.search(rf"{re.escape(bg_token)}:\s*(#[0-9a-fA-F]{{6}})", css)
        if not m:
            errors.append(f"Missing solid color for contrast check: {bg_token}")
            continue
        values[bg_token] = m.group(1)
    for fg, bg, minimum in pairs:
        if fg not in values or bg not in values:
            continue
        ratio = contrast_ratio(values[fg], values[bg])
        if ratio < minimum:
            errors.append(f"Contrast {fg} on {bg} is {ratio:.2f}:1 (< {minimum}:1)")
        else:
            print(f"CONTRAST OK: {fg} on {bg} = {ratio:.2f}:1")
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
        "multi-character",
        "pokemon-guild-panel",
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
    if not QA_DOC.is_file():
        failures.append("Missing QA-CHECKLIST.md")

    for key, asset in ASSETS.items():
        if not asset.is_file():
            failures.append(f"Missing asset: {asset}")
        else:
            print(f"ASSET OK: {asset.name} ({asset.stat().st_size} bytes)")

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
        for err in check_contrast(css):
            failures.append(err)
        for token in REQUIRED_TOKENS:
            if token not in css:
                failures.append(f"Missing expected token/feature: {token}")
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
