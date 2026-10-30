# Asset notes

| File | Format | Dimensions | Approx. size | Role |
|------|--------|------------|--------------|------|
| `pokemon-discord-background.webp` | WebP | 1280 × 720 | ~36 KB | Source artwork embedded into `MidnightPulse.theme.css` |

## Loader reality

BetterDiscord and Vencord inject theme CSS without a reliable theme-file base URL for relative `url(...)` paths. Local `file://` references are also generally unreliable.

Midnight Pulse therefore embeds this WebP as a `data:image/webp;base64,...` value in `--pokemon-bg-image`. **You do not need to copy this folder into the themes directory for installation** — only `MidnightPulse.theme.css`.

## Regenerate the embed

After replacing this WebP:

```bash
python scripts/embed_background.py
python scripts/qa_check.py
```

## Optimization

Subdued night scene converted to WebP (quality ~82) for a small embed footprint.
