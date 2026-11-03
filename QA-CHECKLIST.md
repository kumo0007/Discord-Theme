# Midnight Pulse — Integration-readiness QA

Theme version under audit: **1.3.0**

## Verified (local / structural)

| Check | Result | Notes |
|-------|--------|-------|
| Meta header `@name` / `@author` / `@description` / `@version` | PASS | Version 1.3.0 |
| Filename `MidnightPulse.theme.css` | PASS | BD/Vencord convention |
| CSS brace / string balance | PASS | `scripts/qa_check.py` |
| Four embedded WebP data URIs match `assets/` sources | PASS | main / guild / members / chat |
| Embed script idempotent (second run unchanged) | PASS | Full `url("...")` match |
| Light chat wash + per-message scrims | PASS | Preserved from 1.2.0 |
| Gradient fallback + panel scrims + star-dust sizing | PASS | |
| No remote tracking / http(s) `url()` | PASS | |
| Focus-visible + reduced-motion | PASS | |
| Username role-color override absent | PASS | |
| Contrast spot-check | PASS | |
| Preview uses realistic sample chat (no QA-instruction copy) | PASS | |
| Local preview harness | PASS | Not a Discord client |

## UNVERIFIED (live client)

| Check | Result | Notes |
|-------|--------|-------|
| BetterDiscord / Vencord Themes UI | **UNVERIFIED** | Not installed here |
| Real Discord chat / menus / settings | **UNVERIFIED** | |
| Artwork recognizability in injected CSS | **UNVERIFIED** | Expected via data URIs |

## 1.3.0 changes vs 1.2.0

1. Regenerated all four artwork scenes with a broader, more recognizable Pokémon-inspired cast (distributed across main / chat / guild / members; avoid same character repeated in every panel).
2. Replaced generic fantasy humanoid leanings in the members panel with creature companions (jackal warrior, elegant guardian, night fox, ribbon fox).
3. Kept Midnight Pulse identity: navy/violet/cyan/red, message scrims, layout, responsive narrow fallback.
4. Preview copy rewritten as a realistic #general conversation; developer QA notes removed from the client-facing harness.
5. Re-optimized WebPs and re-embedded; embed remains idempotent.

## Artwork distribution (intent)

| Scene | Intended cast focus |
|-------|---------------------|
| Main | Yellow mouse, orange dragon-lizard, purple ghost, blue jackal warrior, sleepy round beast, brown fox |
| Chat | Blue ninja frog, pale psychic biped, black ringed fox, ribbon fox, gem-forehead fox, green-white guardian |
| Guild | Yellow mouse, purple ghost, brown fox |
| Members | Blue jackal warrior, green-white guardian, black ringed fox, ribbon fox |

## Re-run local QA

```bash
python3 scripts/qa_check.py
python3 scripts/embed_background.py   # only after replacing WebPs
```

## Sign-off

- Structural / asset-strategy / documentation audit: **complete**
- Live BetterDiscord or Vencord integration: **UNVERIFIED**
