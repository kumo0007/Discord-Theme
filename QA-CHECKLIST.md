# Midnight Pulse — Integration-readiness QA

Theme version under audit: **1.0.3**

## Verified (local / structural)

| Check | Result | Notes |
|-------|--------|-------|
| Meta header `@name` / `@author` / `@description` / `@version` | PASS | JSDoc block at file start; name `MidnightPulse` |
| Filename `MidnightPulse.theme.css` | PASS | BD/Vencord convention |
| CSS brace / string balance | PASS | `scripts/qa_check.py` |
| Discord variable bridge (legacy + newer tokens) | PASS | Includes `--background-*`, `--bg-*`, `--background-base-*`, `--text-default` |
| Embedded WebP data URI matches `assets/` source | PASS | Reliable BD/Vencord strategy (no relative/file URL) |
| Gradient overlay + fallback present | PASS | Works when artwork disabled |
| No `background-attachment: fixed` | PASS | Removed for Electron stability |
| No remote tracking / http(s) `url()` in theme | PASS | |
| Focus-visible + reduced-motion rules | PASS | |
| Username role-color override absent | PASS | Compatibility fix in 1.0.3 |
| Overly broad transparent/`clickable` hover narrowed | PASS | Compatibility fix in 1.0.3 |
| README separates verified vs UNVERIFIED; BD vs Vencord steps | PASS | |
| Contrast spot-check (prior run) | PASS | Primary/secondary/muted/link ≥ 6:1 on main surfaces |
| Local preview harness | PASS | Atmosphere only — not a Discord client |

## UNVERIFIED (live client)

| Check | Result | Notes |
|-------|--------|-------|
| BetterDiscord Themes UI loads MidnightPulse | **UNVERIFIED** | BetterDiscord not installed |
| Vencord Themes UI loads MidnightPulse | **UNVERIFIED** | Vencord not installed |
| Chat / channels / composer / menus / settings in real Discord | **UNVERIFIED** | |
| Background art visible in injected CSS environment | **UNVERIFIED** | Data URI expected to work; not observed live |
| Post-Discord-update selector durability | **UNVERIFIED** | |

## Asset strategy decision

| Approach | BD/Vencord reality | Chosen? |
|----------|--------------------|---------|
| Relative `./assets/...` | Generally fails (injected `<style>`, no theme-file base URL) | No (default) |
| `file://` absolute path | Generally blocked / unreliable | No |
| Invented CDN/host URL | Forbidden by audit prompt | No |
| Embedded `data:image/webp;base64,...` | Works offline in a single `.theme.css` | **Yes (default)** |
| CSS gradient fallback | Always available under artwork layer | **Yes** |

## Bugs found & fixed in this audit

1. Relative asset URL was not a reliable BD/Vencord strategy → embedded optimized WebP data URI.
2. Broad transparent rule included `[class*="container_"][class*="themed"]` (risk to settings/surfaces) → removed.
3. Broad `[class*="container_"][class*="clickable"]:hover` → removed.
4. Forced `[class*="username_"]` color broke Discord role colors → removed.
5. Docs implied relative assets might work on Vencord by default → clarified as generally unsupported; install = single file.
6. **Pre-release:** `scripts/embed_background.py` used `[^;]+`, which truncated at the semicolon inside `data:image/webp;base64,...` and corrupted the theme on re-embed → fixed to match full `url("...")`; QA now rejects duplicate/oversized embeds. Regeneration is idempotent.

## Re-run local QA

```bash
python scripts/qa_check.py
python scripts/embed_background.py   # only after replacing the WebP
```

## Live integration test steps

See README → **Live integration test (exact steps)**. Requires BetterDiscord or Vencord installed and the theme enabled in that client.

## Sign-off

- Structural / asset-strategy / documentation audit: **complete**
- Live BetterDiscord or Vencord integration: **UNVERIFIED** — not claimed production-verified
