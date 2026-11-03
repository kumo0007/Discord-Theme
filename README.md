# Midnight Pulse — Pokémon-inspired Discord Theme

Unofficial, fan-made Discord theme: midnight navy / deep violet, electric cyan accents, restrained Poké Ball red, and a **dense multi-character** night atmosphere — recognizable Pokémon-inspired companions across the home background, **central chat column**, server list, and members panel (v1.3.0).

**Not affiliated with, endorsed by, or officially supported by Discord, Nintendo, Game Freak, or The Pokémon Company.**

> **Warning:** Third-party Discord client modifications can violate Discord’s Terms of Service and may carry account, security, or stability risks. Use at your own discretion. This theme is CSS-only: no login automation, credential collection, telemetry, or Discord binary modification.

## What it changes

- App atmosphere (multi-character embedded artwork + CSS gradient fallback)
- Distinct companion art on server-list and members columns (not the same image repeated)
- Dense chat-column artwork with light wash + per-message translucent scrims (center is not left empty)
- Guild list, channel list, chat, composer, headers
- Member list / user panels
- Buttons, links, badges, hover/selected states
- Context menus, popovers, modals, tooltips
- Settings surfaces and scrollbars
- Focus rings and reduced-motion behavior

## Supported loaders (required)

Discord’s official client does **not** load arbitrary custom CSS. This theme targets:

| Loader | Install file | Themes folder (Windows) |
|--------|--------------|-------------------------|
| **BetterDiscord** | `MidnightPulse.theme.css` only | `%appdata%\BetterDiscord\themes\` |
| **Vencord** (desktop / Vesktop) | `MidnightPulse.theme.css` only | `%appdata%\Vencord\themes\` |

macOS / Linux:

- BetterDiscord: `~/Library/Application Support/BetterDiscord/themes/` or `~/.config/BetterDiscord/themes/`
- Vencord: `~/Library/Application Support/Vencord/themes/` or `~/.config/Vencord/themes/`

### Asset loading (important)

BetterDiscord and Vencord inject theme CSS into the Discord UI. **Relative paths like `./assets/...` and local `file://` URLs generally do not load** from that injected CSS.

Midnight Pulse therefore **embeds** four optimized WebPs as `data:image/webp;base64,...` values:

| Token | Source asset | Where it shows |
|-------|--------------|----------------|
| `--pokemon-bg-image` | `pokemon-discord-background.webp` | App shell / home atmosphere |
| `--pokemon-guild-image` | `pokemon-guild-panel.webp` | Server-list column |
| `--pokemon-members-image` | `pokemon-members-panel.webp` | Members column |
| `--pokemon-chat-accent-image` | `pokemon-chat-accent.webp` | Central chat column (multi-character; messages use local scrims) |

That keeps a single portable `.theme.css` file working offline without inventing a hosted CDN URL.

- Source artwork remains in `assets/` for regeneration (`python3 scripts/embed_background.py`).
- If image layers are disabled or fail, `--pokemon-bg-overlay` + `--pokemon-bg-fallback` still paint a cohesive atmosphere.
- Narrow viewports drop photo layers and keep the gradient fallback for clarity.

## Installation

### BetterDiscord

1. Install BetterDiscord for the Discord desktop client ([betterdiscord.app](https://betterdiscord.app/)).
2. Copy **only** `MidnightPulse.theme.css` into `%appdata%\BetterDiscord\themes\`.
3. Fully restart Discord (quit from the system tray, then reopen), or use BetterDiscord’s reload if available.
4. Open **User Settings** → **Themes** (BetterDiscord Themes panel).
5. Enable **MidnightPulse**.
6. Set Discord **Appearance** to **Dark** (this theme is designed for dark mode).

### Vencord

1. Install Vencord for Discord desktop, or use Vesktop ([vencord.dev](https://vencord.dev/)).
2. Copy **only** `MidnightPulse.theme.css` into `%appdata%\Vencord\themes\` (Vesktop may use its own user-data themes path; open Vencord Themes and use “Open Themes Folder” if unsure).
3. Restart Discord / Vesktop if the theme list does not refresh.
4. Open **User Settings** → **Vencord** → **Themes**.
5. Enable **MidnightPulse**.
6. Keep Discord **Appearance** on **Dark**.

## Enable / disable / remove

| Action | BetterDiscord | Vencord |
|--------|---------------|---------|
| **Enable** | User Settings → Themes → toggle MidnightPulse on | User Settings → Vencord → Themes → toggle MidnightPulse on |
| **Disable** | Toggle MidnightPulse off in Themes | Toggle MidnightPulse off in Themes |
| **Remove** | Disable, then delete `MidnightPulse.theme.css` from the themes folder | Same |

## Customization

Edit tokens at the top of `MidnightPulse.theme.css`:

| Variable | Purpose |
|----------|---------|
| `--pokemon-bg-main` / `--pokemon-bg-secondary` / `--pokemon-bg-tertiary` | Surfaces |
| `--pokemon-text-primary` / `--pokemon-text-secondary` / `--pokemon-text-muted` | Text |
| `--pokemon-accent-primary` / `--pokemon-accent-secondary` | Cyan / red accents |
| `--pokemon-border` | Dividers |
| `--pokemon-bg-image` | Main multi-character scene (`data:` URI) |
| `--pokemon-guild-image` / `--pokemon-members-image` / `--pokemon-chat-accent-image` | Column / chat companion art |
| `--pokemon-bg-fallback` | Pure CSS atmosphere if art is off |
| `--pokemon-chat-readability` / `--pokemon-panel-scrim` | Light column washes (not a heavy center blank) |
| `--pokemon-message-scrim` / `--pokemon-message-scrim-hover` | Per-message translucent plates for readable text over art |

Disable artwork (keep gradient atmosphere):

```css
--pokemon-bg-image: linear-gradient(transparent, transparent);
--pokemon-guild-image: linear-gradient(transparent, transparent);
--pokemon-members-image: linear-gradient(transparent, transparent);
--pokemon-chat-accent-image: linear-gradient(transparent, transparent);
```

Use your own hosted image (you must supply a real URL you control — this project does not ship a CDN link):

```css
--pokemon-bg-image: url("https://example.com/your-image.webp");
```

Regenerate embedded artwork from `assets/` after replacing any WebP:

```bash
python3 scripts/embed_background.py
python3 scripts/qa_check.py
```

## Verified vs unverified

### Verified in this repository

- BetterDiscord/Vencord meta header (`@name`, `@author`, `@description`, `@version`) and `*.theme.css` filename
- CSS brace/string balance and required design tokens
- Four embedded WebP data URIs match their `assets/*.webp` sources (idempotent re-embed)
- Gradient overlay + fallback + chat readability scrub present; no remote tracking URLs
- Local contrast checks and preview harness (`preview/index.html`)
- `scripts/qa_check.py` structural suite

### UNVERIFIED (no live loader here)

| Check | Status |
|-------|--------|
| Theme appears in BetterDiscord Themes UI | **UNVERIFIED** — BetterDiscord not installed |
| Theme appears in Vencord Themes UI | **UNVERIFIED** — Vencord not installed |
| Full Discord UI (settings, voice, modals) with theme enabled | **UNVERIFIED** |
| Behavior after a future Discord class-hash update | **UNVERIFIED** |

Official Discord was detected locally; BetterDiscord and Vencord were **not**. Do not treat this deliverable as production-verified on a live client.

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| Theme missing from the list | Filename must end with `.theme.css`; meta block must be the first bytes of the file; restart the client |
| Theme on but looks stock | Appearance = Dark; disable other themes; confirm MidnightPulse is toggled on |
| No background artwork | Embedded data URIs should show by default. Restore via `python3 scripts/embed_background.py`, or set URLs you host. Gradient fallback should still appear |
| Artwork too strong / chat hard to read | Raise `--pokemon-message-scrim` opacity, slightly strengthen `--pokemon-chat-readability`, or disable artwork (transparent gradient trick above) |
| Chat center looks empty | Ensure v1.3.0+ theme file is loaded; chat art should populate the center behind message scrims |
| Layout odd after a Discord update | Disable the theme; Discord class hashes may have changed — variable overrides usually survive longer than attribute selectors |

## Live integration test (exact steps)

Use these steps on a machine that already has BetterDiscord **or** Vencord:

1. Copy `MidnightPulse.theme.css` into that loader’s themes folder (paths above).
2. Restart Discord / Vesktop completely.
3. Enable **MidnightPulse** in the loader Themes UI; set Appearance → Dark.
4. Confirm: guild list, channel list, chat text, composer, member list, a context menu, and User Settings remain usable and readable.
5. Confirm the night artwork (or gradient fallback) is visible behind chat without washing out messages.
6. Toggle the theme off and on; confirm disable restores default styling.
7. Optional: set `--pokemon-bg-image: linear-gradient(transparent, transparent);`, reload, confirm gradient-only atmosphere still looks intentional.

## Project layout

```text
.
├── README.md
├── MidnightPulse.theme.css      # install this file
├── QA-CHECKLIST.md
├── pokemon_discord_theme_requirements.md
├── scripts/
│   ├── qa_check.py
│   └── embed_background.py
├── preview/
│   └── index.html               # local harness only — not a Discord client
└── assets/
    ├── README.md
    ├── pokemon-discord-background.webp   # main multi-character scene
    ├── pokemon-guild-panel.webp          # server-list art
    ├── pokemon-members-panel.webp        # members-column art
    └── pokemon-chat-accent.webp          # chat edge accent
```


### Local structural preview (optional)

```bash
python3 scripts/qa_check.py
python3 -m http.server 8765 --directory .
```

Open `http://127.0.0.1:8765/preview/`. This checks tokens/atmosphere only.

## Safety

- CSS only — no JavaScript, trackers, telemetry, or credential collection.
- No external network requests unless you change `--pokemon-bg-image` to a remote URL.
