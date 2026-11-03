#!/usr/bin/env python3
"""Embed Pokémon WebP assets into MidnightPulse.theme.css as data URIs.

Idempotent: safe to re-run. Matches the full url("...") value, including data URIs
that contain semicolons (data:image/webp;base64,...). Never uses [^;]+ on the value.
"""

from __future__ import annotations

import base64
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "MidnightPulse.theme.css"
THEME_VERSION = "1.3.0"


@dataclass(frozen=True)
class ArtworkSlot:
    key: str  # e.g. "main"
    asset: Path
    var_name: str  # e.g. "--pokemon-bg-image"
    header: str


SLOTS: tuple[ArtworkSlot, ...] = (
    ArtworkSlot(
        key="main",
        asset=ROOT / "assets" / "pokemon-discord-background.webp",
        var_name="--pokemon-bg-image",
        header="""/* ARTWORK:main — primary multi-character night scene (BD/Vencord):
     Relative file paths and file:// URLs generally do NOT load from injected theme CSS.
     Optimized WebP is embedded as a data URI so the theme remains a single portable
     .theme.css file. Source: assets/pokemon-discord-background.webp.
     To disable artwork: set --pokemon-bg-image to linear-gradient(transparent, transparent)
     so the layered gradient fallback remains visible (avoid bare `none` in multi-layer lists).
     To use your own image: replace with url("https://...") you control — do not use
     invented/placeholder hosts. */
  --pokemon-bg-image: """,
    ),
    ArtworkSlot(
        key="guild",
        asset=ROOT / "assets" / "pokemon-guild-panel.webp",
        var_name="--pokemon-guild-image",
        header="""/* ARTWORK:guild — vertical companion art for the server list column.
     Embedded data URI; source assets/pokemon-guild-panel.webp. */
  --pokemon-guild-image: """,
    ),
    ArtworkSlot(
        key="members",
        asset=ROOT / "assets" / "pokemon-members-panel.webp",
        var_name="--pokemon-members-image",
        header="""/* ARTWORK:members — vertical companion art for the members column.
     Embedded data URI; source assets/pokemon-members-panel.webp. */
  --pokemon-members-image: """,
    ),
    ArtworkSlot(
        key="chat",
        asset=ROOT / "assets" / "pokemon-chat-accent.webp",
        var_name="--pokemon-chat-accent-image",
        header="""/* ARTWORK:chat — dense multi-character chat scene (center populated; messages use local scrims).
     Embedded data URI; source assets/pokemon-chat-accent.webp. */
  --pokemon-chat-accent-image: """,
    ),
)


def data_uri_for(asset: Path) -> str:
    data = base64.b64encode(asset.read_bytes()).decode("ascii")
    return f'url("data:image/webp;base64,{data}")'


def replace_or_insert_slot(css: str, slot: ArtworkSlot) -> tuple[str, str]:
    """Replace an existing ARTWORK:<key> block, or insert after prior slots / tokens."""
    if not slot.asset.is_file():
        raise FileNotFoundError(f"Missing asset: {slot.asset}")

    uri = data_uri_for(slot.asset)
    replacement = slot.header + uri + ";"

    # Healthy replace: comment marker through the full quoted url(...) declaration.
    token_pattern = re.compile(
        rf"/\* ARTWORK:{re.escape(slot.key)}\b.*?\*/\s*{re.escape(slot.var_name)}:\s*url\(\"[^\"]*\"\)\s*;",
        flags=re.S,
    )
    css2, n = token_pattern.subn(replacement, css, count=1)
    if n == 1:
        return css2, "replace"

    # Legacy main background block (pre-1.1.0 comment style).
    if slot.key == "main":
        legacy = re.compile(
            r"/\* Background artwork.*?\*/\s*--pokemon-bg-image:\s*url\(\"[^\"]*\"\)\s*;",
            flags=re.S,
        )
        css2, n = legacy.subn(replacement, css, count=1)
        if n == 1:
            return css2, "legacy-replace"

        repair = re.compile(
            r"/\* Background artwork.*?(?=\n\s*--pokemon-bg-overlay:)"
            r"|/\* ARTWORK:main\b.*?(?=\n\s*--pokemon-bg-overlay:)",
            flags=re.S,
        )
        css2, n = repair.subn(replacement + "\n ", css, count=1)
        if n == 1:
            return css2, "repair"

    # Insert new slots before --pokemon-bg-overlay (after main image declaration).
    insert_at = re.search(r"\n\s*--pokemon-bg-overlay:", css)
    if insert_at:
        css2 = css[: insert_at.start()] + "\n\n  " + replacement + css[insert_at.start() :]
        return css2, "insert"

    raise RuntimeError(f"Could not locate insertion point for ARTWORK:{slot.key}")


def main() -> int:
    if not THEME.is_file():
        print(f"Missing theme: {THEME}", file=sys.stderr)
        return 1

    css = THEME.read_text(encoding="utf-8")
    modes: list[str] = []
    try:
        for slot in SLOTS:
            css, mode = replace_or_insert_slot(css, slot)
            modes.append(f"{slot.key}:{mode}")
            print(
                f"Embedded {slot.asset.name} ({slot.asset.stat().st_size} bytes) "
                f"-> {slot.var_name} ({len(base64.b64encode(slot.asset.read_bytes()))} b64) via {mode}"
            )
    except (FileNotFoundError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    css, n = re.subn(r"(@version\s+)[\d.]+", rf"\g<1>{THEME_VERSION}", css, count=1)
    if n != 1:
        print("Warning: could not update @version", file=sys.stderr)

    THEME.write_text(css, encoding="utf-8", newline="\n")
    print(f"Theme version set to {THEME_VERSION}")
    print("Modes: " + ", ".join(modes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
