# Asset notes

| File | Format | Dimensions | Approx. size | Role |
|------|--------|------------|--------------|------|
| `pokemon-discord-background.webp` | WebP | ~1200 × 675 | ~76 KB | Main multi-character night scene |
| `pokemon-guild-panel.webp` | WebP | ~420 × 747 | ~49 KB | Server-list column art |
| `pokemon-members-panel.webp` | WebP | ~420 × 747 | ~46 KB | Members column art |
| `pokemon-chat-accent.webp` | WebP | ~1200 × 675 | ~55 KB | Dense chat-column scene |
| `mp-*-v13-source.jpg` | JPEG | original gen | larger | Regeneration sources (not required to install) |

## Loader reality

BetterDiscord and Vencord inject theme CSS without a reliable theme-file base URL. Midnight Pulse embeds each WebP as a `data:image/webp;base64,...` value. **Install only `MidnightPulse.theme.css`.**

## Regenerate embeds

```bash
python3 scripts/embed_background.py
python3 scripts/qa_check.py
```

## Optimization

Recognizable multi-character compositions converted to WebP (quality ~74–76) for a portable single-file theme.
