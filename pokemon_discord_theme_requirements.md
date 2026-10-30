# Pokémon Discord Theme — Requirements & Implementation Specification

## 1. Project Overview

Build a polished, custom Pokémon-inspired theme for Discord. The client has given the developer creative discretion and wants the design to be a surprise.

**Target deliverable:** A working Discord theme stylesheet with any required original/generated visual assets, setup instructions, and a short QA checklist.

**Agreed initial budget:** $30 for AI-generated artwork and custom CSS implementation. Keep the scope focused; discuss any substantial extra features before implementing them.

## 2. Important Platform Constraint

Discord's official client does not generally support arbitrary custom CSS themes through its standard settings. The implementation must not claim otherwise.

1. First inspect the repository and identify the intended supported theme mechanism.
2. If the project already targets a theme loader or client mod (for example, a compatible theme system), follow that project's current format and document the required loader.
3. If there is no existing target, create a standalone theme CSS file intended for a compatible third-party theme loader, plus clear installation notes and a warning that third-party client modifications may violate Discord's terms or create account/security risks.
4. Do not automate Discord login, collect credentials, bypass authentication, or modify Discord binaries.
5. Do not promise compatibility with every Discord update. State the tested environment and known limitations.

## 3. Creative Direction

Create a distinctive, cohesive Pokémon-inspired aesthetic. The developer has artistic discretion, so do not pause for approval on routine visual choices.

### Visual concept
- Premium dark interface with midnight navy / deep violet foundations.
- Electric cyan and Poké Ball red as restrained accent colors.
- Soft glow, subtle gradients, clean borders, and comfortable contrast.
- Pokémon/anime atmosphere without making the UI cluttered or difficult to read.
- Use an original composition and layout treatment rather than copying an existing theme.
- Keep the interface readable at common desktop window sizes.

### Artwork
- Create or source a suitable AI-generated background artwork, ideally wide/landscape.
- Suggested composition: an atmospheric Pokémon-inspired night scene with a luminous Poké Ball motif, stars, and a few Pokémon-like focal elements arranged away from high-density text areas.
- Artwork should be visually appealing but subdued enough behind UI elements.
- Prefer original generated artwork. Do not use official logos or imply the theme is official or endorsed by Nintendo, The Pokémon Company, or Discord.
- Keep large background images optimized; avoid unnecessarily huge files.
- If an image-generation tool is unavailable, create a CSS-gradient fallback and document the missing asset.

## 4. Functional Requirements

### Theme stylesheet
- Deliver one primary `.theme.css` file, or the repository's established equivalent.
- Follow the target theme loader's required metadata/header format, if applicable.
- Use CSS variables/design tokens for:
  - Main background
  - Secondary/surface backgrounds
  - Primary and secondary text
  - Muted text
  - Primary accent
  - Secondary accent
  - Borders/dividers
  - Focus/hover states
- Prefer scoped selectors and supported Discord theme variables where practical.
- Avoid broad selectors that accidentally break modals, popovers, menus, or settings.
- Add comments for major sections and any fragile selectors.
- Avoid unnecessary `!important`; use it only where the theme system requires it.
- Do not inject JavaScript, trackers, telemetry, external requests, or credential collection.
- Do not add dependencies unless they are genuinely needed.

### Areas to style
Style as many of these as the chosen loader reliably supports:
- Main app background and content surfaces
- Server/guild list
- Channel list and selected/hovered channels
- Chat messages and message hover states
- Message composer and attachment area
- Top bars and headers
- Member list and user panels
- Buttons, links, badges, and interactive states
- Settings screens
- Context menus, popovers, and modals
- Scrollbars
- Search UI and tooltips

### Usability and accessibility
- Maintain readable contrast for body text and secondary text.
- Preserve visible keyboard focus indicators.
- Keep hover and selected states distinguishable without color alone.
- Do not obscure message content with decorative backgrounds.
- Ensure controls remain recognizable and clickable.
- Respect reduced-motion preferences; avoid aggressive flashing or continuous animations.
- Ensure the theme degrades gracefully if the background image fails to load.

### Responsive behavior
- Work at typical desktop Discord window sizes.
- Avoid fixed widths/heights that cause core interface sections to disappear.
- Do not make the background interfere with mobile/narrow layouts; if mobile is outside the target loader's support, state that limitation.

## 5. Asset Requirements

Create an `assets/` directory if appropriate. Include:
- Main background image, e.g. `pokemon-discord-background.webp` or optimized PNG/JPEG.
- Any additional artwork only if it adds clear value.
- A brief note documenting asset format and dimensions.

Use relative asset paths when supported by the theme loader. Verify that the path remains valid after installation. Do not reference local development-only absolute paths.

## 6. Repository Workflow

Before coding:
1. Inspect the current repository, package files, existing CSS, README, and target theme-loader requirements.
2. Identify the expected file structure and compatibility format.
3. Preserve existing project conventions and avoid unrelated refactors.
4. If the repository is empty, create a minimal, organized structure.

During implementation:
1. Define the design tokens.
2. Add the artwork or a gradient fallback.
3. Implement the CSS in logical, commented sections.
4. Add installation and troubleshooting instructions.
5. Keep the theme easy to customize by changing variables.

Do not overwrite unrelated user files. If an implementation choice depends on a missing repository detail, choose a safe, documented default rather than inventing unsupported platform capabilities.

## 7. Suggested Deliverable Structure

Adapt to the repository if it already has a structure. Otherwise, use something similar to:

```text
pokemon-discord-theme/
├── README.md
├── theme.css
├── assets/
│   └── pokemon-discord-background.webp
└── QA-CHECKLIST.md
```

## 8. README Requirements

The README must explain:
- What the theme is and what it changes.
- The supported Discord client/theme-loader setup.
- The fact that this is an unofficial, fan-made theme.
- Installation steps specific to the chosen loader.
- How to enable/disable the theme.
- How to customize accent colors and background artwork.
- Known compatibility limitations and troubleshooting.
- A concise warning that third-party client modifications may carry account, security, or terms-of-service risks.
- No claims that the theme is officially supported by Discord or Pokémon rights holders.

Do not provide vague instructions such as “put this somewhere in Discord.” Give concrete steps for the selected target, and do not fabricate menu names or settings.

## 9. Quality Assurance

Run available checks and inspect the final result in the target environment where possible.

Checklist:
- [ ] Theme file parses and loads without CSS errors.
- [ ] All referenced assets exist and resolve after installation.
- [ ] Main chat text and secondary text remain readable.
- [ ] Channel selected/hover states are clear.
- [ ] Composer, buttons, menus, popovers, and modals remain usable.
- [ ] Settings and member list are not hidden or broken.
- [ ] Background artwork does not overpower message readability.
- [ ] Keyboard focus is visible.
- [ ] Reduced-motion preference is respected.
- [ ] No external tracking, telemetry, credential collection, or unexpected network calls.
- [ ] Installation and removal instructions have been checked.
- [ ] Tested client/loader versions and limitations are documented.

If the theme cannot be launched in a real compatible client in the current environment, clearly state that visual integration testing remains unverified. Do not claim it was tested when it was not.

## 10. Acceptance Criteria

The work is complete when:
1. A usable theme stylesheet is present.
2. The visual design feels cohesive and distinctly Pokémon-inspired.
3. The artwork is included or a documented fallback is provided.
4. The core Discord interface remains readable and functional.
5. Setup, customization, and removal instructions are clear.
6. QA findings and any unverified compatibility claims are documented.
7. No unrelated files or behavior have been changed.

## 11. Cursor's First Task

Inspect the repository and report:
- Existing project type and relevant files
- Whether a theme-loader format is already established
- Which files should be created or modified
- Any platform compatibility concerns

Then implement the complete scoped deliverable. Make sensible creative decisions independently. Do not stop to ask the client about routine colors, layout, or artwork choices. Only ask a question if a missing technical detail blocks a safe, functional implementation.
