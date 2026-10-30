# Midnight Pulse — Pokémon-inspired Discord Theme

Unofficial, fan-made Discord theme: midnight navy / deep violet, electric cyan accents, restrained Poké Ball red, and a soft night atmosphere behind translucent panels.

**Not affiliated with, endorsed by, or officially supported by Discord, Nintendo, Game Freak, or The Pokémon Company.**

> **Warning:** Third-party Discord client modifications can violate Discord’s Terms of Service and may carry account, security, or stability risks. Use at your own discretion. This theme is CSS-only: no login automation, credential collection, telemetry, or Discord binary modification.

## What it changes

- App atmosphere (embedded artwork + CSS gradient fallback)
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

Midnight Pulse therefore **embeds** `assets/pokemon-discord-background.webp` as a `data:image/webp;base64,...` value in `--pokemon-bg-image`. That keeps a single portable `.theme.css` file working offline without inventing a hosted CDN URL.

- Source artwork remains in `assets/` for regeneration (`python scripts/embed_background.py`).
- If the image layer is disabled or fails, `--pokemon-bg-overlay` + `--pokemon-bg-fallback` still paint a cohesive atmosphere.

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
| `--pokemon-bg-image` | Artwork (`data:` URI by default) |
| `--pokemon-bg-fallback` | Pure CSS atmosphere if art is off |

Disable artwork (keep gradient atmosphere):

```css
--pokemon-bg-image: linear-gradient(transparent, transparent);
```

Use your own hosted image (you must supply a real URL you control — this project does not ship a CDN link):

```css
--pokemon-bg-image: url("https://example.com/your-image.webp");
```

Regenerate the embedded artwork from `assets/` after replacing the WebP:

```bash
python scripts/embed_background.py
python scripts/qa_check.py
```

## Verified vs unverified

### Verified in this repository

- BetterDiscord/Vencord meta header (`@name`, `@author`, `@description`, `@version`) and `*.theme.css` filename
- CSS brace/string balance and required design tokens
- Embedded WebP data URI matches `assets/pokemon-discord-background.webp`
- Gradient overlay + fallback present; no remote tracking URLs
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
| No background artwork | Embedded data URI should show by default. If you cleared `--pokemon-bg-image`, restore via `python scripts/embed_background.py`, or set a URL you host. Gradient fallback should still appear |
| Artwork too strong / chat hard to read | Increase opacity in `--pokemon-bg-overlay`, or disable artwork (transparent gradient trick above) |
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
    └── pokemon-discord-background.webp   # source for embed; not required at install time
```

### Local structural preview (optional)

```bash
python scripts/qa_check.py
python -m http.server 8765 --directory .
```

Open `http://127.0.0.1:8765/preview/`. This checks tokens/atmosphere only.

## Safety

- CSS only — no JavaScript, trackers, telemetry, or credential collection.
- No external network requests unless you change `--pokemon-bg-image` to a remote URL.
