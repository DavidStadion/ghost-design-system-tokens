# Inter Miami CF — Session Handover & Context Document

> **How to use this file:** At the start of a new session, tell Claude:
> *"Please read `/tmp/ghost-tokens-work/SESSION_HANDOVER.md` before we begin — it contains full context for the Inter Miami design system work."*
> Or if the repo has been re-cloned: read `SESSION_HANDOVER.md` from `DavidStadion/ghost-design-system-tokens` on the `inter-miami` branch.

---

## Project Overview

This is the **Inter Miami CF brand fork** of the Ghost Design System. The work spans:
1. Token value edits in a GitHub-hosted JSON file (`tokens.json`)
2. Direct Figma node changes via the Figma Plugin API (`use_figma` MCP tool)
3. The two must never be confused — see **Two-Channel Rule** below.

---

## Key Files & Repositories

| Item | Location |
|---|---|
| Token repo (local) | `/tmp/ghost-tokens-work/` |
| Token repo (GitHub) | `DavidStadion/ghost-design-system-tokens` — branch `inter-miami` |
| Token file | `/tmp/ghost-tokens-work/tokens.json` |
| Architecture reference | `/tmp/ghost-tokens-work/GHOST_DESIGN_SYSTEM.md` |
| Component catalogue | `/tmp/ghost-tokens-work/COMPONENTS.md` |
| Brand fork guide | `/tmp/ghost-tokens-work/BRAND_FORK_GUIDE.md` |
| Inter Miami decisions | `/tmp/ghost-tokens-work/INTER_MIAMI_BRAND_FORK.md` |
| Figma file | `wK1SnviTqfM2j0vK1rObTy` (David-Test-Inter-Miami-2.0) |
| Creative references | `/Users/dhstadion/projects/ai-david-ghost-test/assets/inter-miami/creative/` |

---

## Brand Palette

| Token | Hex | Usage |
|---|---|---|
| `P.Color.Primary.1` | `#FF9CB4` | Light pink — backgrounds, dividers, hover states |
| `P.Color.Primary.2` | `#FF6B8E` | Mid pink |
| `P.Color.Primary.3` | `#E8004B` | **Miami Pink — primary brand colour, CTAs, emphasis** |
| `P.Color.Primary.4` | `#FFB8CB` | — |
| `P.Color.Primary.5` | `#FFD4DF` | — |
| `P.Color.Primary.6` | `#FFEDF1` | Blush — very light tinted surfaces |
| `P.Color.Secondary.1` | `#231F20` | Near-black — inverse card backgrounds, dark surfaces |
| `P.Color.Shades.Primary-1.600` | `#E8638A` | Mid-pink — hover/active on dark surfaces |
| `P.Color.Shades.Secondary-1.600` | `#1A1718` | Dark near-black — hover/active on inverse cards |

**Font family:** Inter — styles used: Regular, Bold, Extra Bold

---

## Two-Channel Rule (CRITICAL — never mix these)

| What you're changing | Channel | How |
|---|---|---|
| Colour values, typography, radius | **Channel 1 — tokens.json** | Edit file → `git commit + push` → Tokens Studio Pull in Figma |
| Layout, variant props, image fills, structural | **Channel 2 — Figma Plugin API** | `use_figma` MCP tool with JS |

**Token binding rule:** Any time you set a fill via Plugin API on a token-bound node, you MUST also update the binding:
```js
node.setSharedPluginData('tokens', 'fill', JSON.stringify('Token.Path.Here'));
```

---

## Tokens Studio Setup

- **Repository:** `DavidStadion/ghost-design-system-tokens`
- **Branch:** `inter-miami` ⚠️ NEVER pull from `main` — it overwrites all brand changes
- **File path:** `tokens.json`
- After every `git push`: Figma → Tokens Studio → Pull → Apply to pages

---

## Token Architecture (4 Layers)

```
Layer 1 — Primitive      P.Color.*         Raw hex values. Brand-specific.
     ↓
Layer 2 — Semantic       S.Color.*         Intent-based ("what is this for?")
     ↓
Layer 3 — ColourSet      ColourSet.*       Surface-context overrides
     ↓
Layer 4 — Component      C.Color.*         Per-component, per-state tokens
```

---

## Committed Token Changes (inter-miami branch)

| Commit | Token changed | Old value | New value | Reason |
|---|---|---|---|---|
| `14735b7` | `S.Color.Interaction.Inverse.Link.Enabled` | `{P.Color.Secondary.1}` (#231F20 — near-invisible on black) | `{P.Color.Primary.1}` (#FF9CB4) | Fix contrast fail on dark video cards — was 1.24:1, now 15:1 |
| `14735b7` | `S.Color.Interaction.Inverse.Link.Hover/Active` | `{P.Color.Shades.Secondary-1.600}` | `{P.Color.Shades.Primary-1.600}` | Match enabled fix |
| `2f76c61` | `C.Color.Card.SearchResult-player.ShirtNumber.*` | `{C.Color.Card.Default.SupportingText.*}` | `{P.Color.Primary.3}` | Brand pink shirt numbers on player cards |
| `24648d7` | `C.Color.CategoryLink.Default.Label.Enabled` | `{S.Color.Interaction.Default.Link.Enabled}` (light pink) | `{P.Color.Primary.3}` (#E8004B) | Dark pink category labels on all article cards |
| `24648d7` | `C.Color.CategoryLink.Default.Label.Hover/Active` | via Semantic chain | `{P.Color.Shades.Primary-1.600}` | Match enabled fix |
| `3ac8499` | `C.Color.Card.Inverse.Background.Enabled` | `{S.Color.Interaction.Neutral.Inverse.Primary.Background.Enabled}` → pure black | `{P.Color.Secondary.1}` (#231F20) | Inverse card BG = brand near-black, not pure black |
| `3ac8499` | `C.Color.Card.Inverse.Background.Hover/Active` | via Semantic chain | `{P.Color.Shades.Secondary-1.600}` | Match enabled fix |

---

## Figma Changes Applied Directly (not via tokens.json)

### Search Page Pink Theme (applied to 3 pages)
Affected pages: Results Lists `23052:35679`, Results Carousel `23065:81746`, Base Page - Search `23066:178566`

| What | Token binding | Colour applied |
|---|---|---|
| Section headings | `CS.ColorSet-1.Text.Main` | `#E8004B` + Inter Extra Bold |
| Result counts ("XX Results") | `S.Color.Text.Default.Supporting` | `#E8004B` |
| CTA labels | `CS.ColorSet-1.TextButton.Label.Enabled` | `#E8004B` |
| Text links / page links | `S.Color.Interaction.Neutral.Default.Primary.Label.Enabled` | `#E8004B` + Bold |
| Page link arrows | `S.Color.Interaction.Neutral.Default.Primary.Icon.*` | `#E8004B` |
| TextButton icons | `C.Color.TextButton.Default.Icon.*` | `#E8004B` |
| Article dividers | `C.Color.Card.SearchResult-article.Divider.*` | `#FF9CB4` |
| Player shirt numbers | `C.Color.Card.SearchResult-player.ShirtNumber.*` | `#E8004B` |
| 252 CategoryLink.Default.Label nodes | `C.Color.CategoryLink.Default.Label.Enabled` | `#E8004B` |
| 222 Video card background nodes | `C.Color.Card.SearchResult-video.Background.Enabled` | `#231F20` |

### Structural Changes
- **ContentHoldingItem** (`2619:1121` main component): fill `#E9ECEF` → `#FFFFFF`, token bound to `S.Color.Background.Default.Main` — removes off-brand grey carousel placeholders
- **Search-Video Master** `23009:505377`: Image instance `23009:505191` variant switched from `Aspect ratio=16x9` → `Aspect ratio=1x1`

---

## Search Section Node IDs (Figma)

| Artboard | Node ID |
|---|---|
| Search page (full overview) | `6203:43068` |
| Search - Video Article Cards master | `23009:505377` |
| Search - Gallery Article Cards master | `23009:498841` |
| Search-ResultsCarousel-Master | `23063:54372` |
| Results Lists page | `23052:35679` |
| Results Carousel page | `23065:81746` |
| Results Carousel (instances) | `23065:69850` |
| Base Page - Search | `23066:178566` |

---

## ColourSet Tokens Relevant to Search

The Results Carousel uses `CS.ColorSet-1.*` tokens for its surface context:

| Token | Current value | Notes |
|---|---|---|
| `CS.ColorSet-1.Text.Main` | → section titles | Currently `#E8004B` (set via Figma direct) |
| `CS.ColorSet-1.TextButton.Label.Enabled` | → CTA label | Currently `#E8004B` |
| `CS.ColorSet-1.Button.Primary.Container-Background.Enabled` | → paddle buttons | Currently `#FF9CB4` |

---

## NEXT TASK — Creative Inspiration → Search Section Styling

**Status: NOT STARTED**

### The brief
Use the Inter Miami creative references as an inspiration board and implement changes across the Search section — both master components and Component/ColourSet tokens in Tokens Studio.

### Creative reference files
Location: `/Users/dhstadion/projects/ai-david-ghost-test/assets/inter-miami/creative/`

| File | Content |
|---|---|
| `screencapture-intermiamicf-2026-04-28-23_24_21.png` | Homepage — dark nav, pink accents, editorial hero |
| `screencapture-intermiamicf-club-2026-04-28-23_24_50.png` | Club page — full-bleed image tiles on dark background |
| `screencapture-intermiamicf-schedule-2026-04-28-23_25_18.png` | Schedule page — clean white/light with pink accents |
| `screencapture-intermiamicf-club-roster-2026-04-28-23_25_57.png` | Roster page — 1x1 player photos, pink hero, dark footer |
| `EzRuB87VEAkuwmi.jpg` | Team lineups graphic — **core aesthetic**: dark charcoal bg, hot pink labels, white bold type |
| `*.webp` files | Social/brand imagery |

### Key creative observations (already analysed)
1. **Dark surfaces dominate** — near-black charcoal (`#231F20`) is the primary background on content-heavy pages
2. **Hot pink `#E8004B` is a pure accent** — used for labels, category chips, borders, CTAs — NOT as fills
3. **Bold uppercase typography** — section headers Extra Bold or all-caps; player names in heavy weight
4. **Player cards** — 1x1 square crops, dark overlay text panel at bottom with white name, pink number/position
5. **Image-led layouts** — full-bleed images with dark overlays rather than coloured backgrounds
6. **The lineup graphic aesthetic** = target reference for the dark search theme: charcoal ground, pink position labels, white player names in bold

### Recommended implementation approach for next session

**Step 1 — Read references**
```
Read each image in /Users/dhstadion/projects/ai-david-ghost-test/assets/inter-miami/creative/
```

**Step 2 — Audit current Search section**
Take screenshots of:
- `6203:43068` (full Search page)
- `23052:35679` (Results Lists)
- `23065:81746` (Results Carousel)
- `23066:178566` (Base Page - Search)

**Step 3 — Identify gaps vs creative**
Key likely gaps:
- Search input bar styling (border colour, focus state)
- Article card image overlays (currently no dark overlay on news/gallery cards)
- Section header typography (uppercase treatment)
- Player card dark panel / number treatment
- Overall page background tone (currently white — should it have a dark hero/header area?)

**Step 4 — Update tokens.json**
Focus on `CS.ColorSet-1.*` (Results Carousel surface), Component card tokens, and any Semantic overrides needed.

**Step 5 — Apply Figma changes**
Structural/visual changes (image overlays, layout, variant swaps) via `use_figma`.

---

## Known Caveats / Plugin API Gotchas

```js
// Always skip these node types when scanning fills:
const SKIP = new Set(['GROUP', 'BOOLEAN_OPERATION', 'VECTOR', 'LINE']);

// Never access fontSize/fontName on non-TEXT nodes:
if (node.type === 'TEXT') { node.fontSize = ...; }

// Instance override node IDs use semicolon paths:
// 'I{base};{comp1};{comp2}'

// Load fonts before setting them:
await figma.loadFontAsync({ family: 'Inter', style: 'Extra Bold' });
```

---

## Git Workflow Reminder

```bash
cd /tmp/ghost-tokens-work
git checkout inter-miami       # always verify branch first
# ... edit tokens.json ...
git add tokens.json
git commit -m "Inter Miami — [describe change]"
git push origin inter-miami
# Then: Figma → Tokens Studio → Pull → Apply to pages
```

---

*Last updated: 2026-04-29 | Branch: inter-miami | Latest commit: `3ac8499`*
