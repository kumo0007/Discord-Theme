#!/usr/bin/env python3
"""Embed assets/pokemon-discord-background.webp into MidnightPulse.theme.css as a data URI.

Idempotent: safe to re-run. Matches the full url("...") value, including data URIs that
contain semicolons (data:image/webp;base64,...).
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "pokemon-discord-background.webp"
THEME = ROOT / "MidnightPulse.theme.css"

# Complete healthy declaration (comment + url("...")).
TOKEN_PATTERN = re.compile(
    r"/\* Background artwork.*?\*/\s*--pokemon-bg-image:\s*url\(\"[^\"]*\"\)\s*;",
    flags=re.S,
)

# Recovery: comment through whatever broken content until the next known token.
REPAIR_PATTERN = re.compile(
    r"/\* Background artwork.*?(?=\n\s*--pokemon-bg-overlay:)",
    flags=re.S,
)

HEADER = """/* Background artwork strategy (BD/Vencord):
     Relative file paths and file:// URLs generally do NOT load from injected theme CSS.
     The optimized WebP is embedded as a data URI so the theme remains a single portable
     .theme.css file. Source file kept at assets/pokemon-discord-background.webp.
     To disable artwork: set --pokemon-bg-image to linear-gradient(transparent, transparent)
     so the layered gradient fallback remains visible (avoid bare `none` in multi-layer lists).
     To use your own image: replace with url("https://...") you control — do not use
     invented/placeholder hosts. */
  --pokemon-bg-image: """


def main() -> int:
    if not ASSET.is_file():
        print(f"Missing asset: {ASSET}", file=sys.stderr)
        return 1
    if not THEME.is_file():
        print(f"Missing theme: {THEME}", file=sys.stderr)
        return 1

    data = base64.b64encode(ASSET.read_bytes()).decode("ascii")
    uri = f'url("data:image/webp;base64,{data}")'
    replacement = HEADER + uri + ";"

    css = THEME.read_text(encoding="utf-8")
    css2, n = TOKEN_PATTERN.subn(replacement, css, count=1)
    mode = "replace"
    if n != 1:
        css2, n = REPAIR_PATTERN.subn(replacement + "\n ", css, count=1)
        mode = "repair"
        if n != 1:
            print(
                "Could not locate --pokemon-bg-image artwork block to replace or repair.",
                file=sys.stderr,
            )
            return 1

    css2 = re.sub(r"(@version\s+)[\d.]+", r"\g<1>1.0.3", css2, count=1)
    THEME.write_text(css2, encoding="utf-8", newline="\n")
    print(
        f"Embedded {ASSET.name} ({ASSET.stat().st_size} bytes) -> data URI "
        f"({len(data)} b64 chars) via {mode}"
    )
    print("Theme version set to 1.0.3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
