# Ghost Design System — Architecture Reference

This document explains how the Ghost Design System token architecture works. Read this before making any token changes or starting a brand fork. Understanding the layers and naming conventions here is the foundation for everything else.

---

## Overview

Ghost uses a **4-layer token hierarchy**. Each layer references the layer above it. Changing a value at any layer cascades down to every component that references it.

```
Layer 1 — Primitive      Raw colour values. Brand-specific. Lives in tokens.json.
     ↓ references
Layer 2 — Semantic       Intent-based tokens ("what is this for?"). References Primitives.
     ↓ references
Layer 3 — ColourSet      Surface-context overrides. References Semantics.
     ↓ references
Layer 4 — Component      Per-component, per-state tokens. References Semantics or ColourSets.
```

A component like `CommonButton` never references a raw hex value. It references a Component token, which references a Semantic token, which references a Primitive. Swapping a brand's Primitive colours cascades the change through all three layers automatically.

---

## Layer 1 — Primitive (`Primitive.P.*`)

**Purpose:** Store raw values. No meaning, just values.

**Who edits this:** Brand fork setup only. Once set for a brand, never change mid-project.

**Key namespaces:**

```
P.Color.Primary.1–6          Brand primary palette (lightest → darkest)
P.Color.Secondary.1–6        Brand secondary palette
P.Color.Neutral.Black        #000000
P.Color.Neutral.White        #FFFFFF
P.Color.Neutral.100–900      Standard neutral scale
P.Color.Shades.Primary-1.*   Extended hover/active shades derived from Primary
P.Color.Opacity.Default.10   10% black (for overlays, dividers)
P.Color.Opacity.Inverse.10   10% white
```

**Example (Inter Miami):**
```json
"P.Color.Primary.1": { "value": "#FF9CB4" },   // Pastel pink — light accent
"P.Color.Primary.2": { "value": "#FF6B8E" },   // Mid pink
"P.Color.Primary.3": { "value": "#E8004B" },   // Miami Pink — primary brand colour
"P.Color.Primary.4": { "value": "#FFB8CB" },
"P.Color.Primary.5": { "value": "#FFD4DF" },
"P.Color.Primary.6": { "value": "#FFEDF1" },   // Blush
"P.Color.Secondary.1": { "value": "#231F20" }  // Near black
```

**Rules:**
- Primary.1 is always the lightest accent (used for backgrounds, BackToTop, MoreMenu panel)
- Primary.3 is always the primary brand colour (used for emphasis fills, selected borders)
- Neutrals are inherited from Ghost `main` branch — only override if the brand replaces them

---

## Layer 2 — Semantic (`Semantic.S.*`)

**Purpose:** Assign intent. A Semantic token says *what this colour is for*, not what it looks like.

**Who edits this:** When a Semantic token's default Ghost mapping needs to change for a brand (e.g., a border that was Ghost-blue becomes brand-pink).

**Structure: surface × intent**

Every Semantic token has two dimensions:
1. **Surface context** — `Default` (light surface) or `Inverse` (dark surface)
2. **Intent** — what the colour is used for

```
S.Color.Background.Default.Main          Primary background on light surfaces
S.Color.Background.Default.Subtle        Secondary/muted background on light surfaces
S.Color.Background.Default.Emphasis      Accent background on light surfaces → Primary.1
S.Color.Background.Inverse.Main          Primary background on dark surfaces → Black
S.Color.Background.Inverse.Subtle        Hover state on dark surfaces
S.Color.Background.HoldingColour.*       Fully transparent (structure placeholder)

S.Color.Text.Default.Main                Primary text on light surfaces → Black
S.Color.Text.Default.Supporting          Secondary text on light surfaces → Neutral.700
S.Color.Text.Inverse.Main                Primary text on dark surfaces → White
S.Color.Text.Inverse.Supporting          Secondary text on dark surfaces → Neutral.300

S.Color.Fill.Default.Main                Icon fill on light surfaces → Black
S.Color.Fill.Inverse.Main                Icon fill on dark surfaces → White

S.Color.Border.Default.Main              Standard border on light surfaces
S.Color.Border.Default.Subtle            Muted border on light surfaces
S.Color.Border.Default.Emphasis          Accent/selected border on light surfaces → Primary.3
S.Color.Border.Inverse.Main              Standard border on dark surfaces
S.Color.Border.Inverse.Emphasis          Accent/selected border on dark surfaces → Primary.3

S.Color.Interaction.Default.Primary.*    Interactive element (button/link) on light surfaces
S.Color.Interaction.Inverse.Primary.*    Interactive element on dark surfaces
S.Color.Interaction.Neutral.Default.*    Neutral interactive (ghost button, nav item) on light
S.Color.Interaction.Neutral.Inverse.*    Neutral interactive on dark
S.Color.Interaction.Destructive.*        Destructive/error states
```

**Interaction tokens sub-structure (all interaction tokens follow this pattern):**
```
*.Container-Background.Enabled
*.Container-Background.Hover
*.Container-Background.Active
*.Container-Background.Selected
*.Container-Background.Disabled
*.Label.Enabled / .Hover / .Active / .Selected / .Disabled
*.Icon.Enabled / .Hover / .Active / .Selected / .Disabled
*.Border.Enabled / .Hover / .Active / .Selected / .Disabled
```

**Brand fork changes that typically hit Semantic layer:**

| Token | Ghost default | Why a brand would change it |
|---|---|---|
| `S.Color.Border.Default.Emphasis` | Ghost accent | → `{P.Color.Primary.3}` for brand-pink selected borders |
| `S.Color.Border.Inverse.Emphasis` | Ghost inverse accent | → `{P.Color.Primary.3}` for brand-pink on dark surfaces |
| `S.Color.Interaction.Inverse.Primary.Container-Background.*` | Dark near-black | → `{P.Color.Primary.3}` for brand-pink buttons on dark surfaces |
| `S.Color.Background.Default.Emphasis` | Ghost accent | → `{P.Color.Primary.1}` for light pink backgrounds |

---

## Layer 3 — ColourSet (`ColourSet.*`)

**Purpose:** Override Semantic tokens for specific surface colour contexts. When a component is placed on a branded surface (e.g., a dark-charcoal section), the ColourSet ensures its tokens resolve correctly for that surface.

**ColourSets in Ghost:**

| ColourSet | Surface type | Typical use |
|---|---|---|
| `Default` / `Base-1` | White/light surface | Page body, cards, standard sections |
| `Base-2` | Off-white / light-brand surface | Subtle tinted sections |
| `Inverse` | Dark surface (near-black) | Inverted hero sections |
| `CS-1` | Brand Primary.6 (very light) | Light brand tinted section |
| `CS-2` | Brand Primary.5 | Light-medium brand section |
| `CS-3` | Brand Primary.3 (primary) | Full primary colour section |
| `CS-4` | Brand Secondary colour | Secondary brand section |
| `CS-5` | Neutral.800 (dark grey) | Dark neutral section |
| `CS-6` | Neutral.900 / Black | Darkest neutral section |

**How ColourSets work:**

A ColourSet token overrides a specific Semantic token for that surface context. Example:

```json
"ColourSet.CS-3.S.Color.Text.Default.Main": {
  "value": "{P.Color.Neutral.White}"
}
```

This means: on a CS-3 surface (brand primary colour background), what would normally be `S.Color.Text.Default.Main` (black) is instead white — because black text on a saturated primary background often fails contrast.

**ColourSet overrides that typically need brand review:**

- Text colours on CS-3 and CS-4 (primary colour surfaces) — often need white instead of black
- Button Primary container colours on CS-5/CS-6 (dark surfaces) — brand Primary.3 must reach 3:1 on the surface
- Border.Emphasis on all surfaces

**Important:** ColourSet tokens cascade to components that reference Semantic tokens — you do not need to update every Component token when a ColourSet changes. The component just re-resolves its Semantic reference through the active ColourSet.

---

## Layer 4 — Component (`Component.C.*`)

**Purpose:** Map specific component properties (background of a button in its hover state) to a Semantic or ColourSet token. This is the layer you edit when a single component needs special treatment that can't be handled by a Semantic change alone.

**Naming pattern:**
```
C.Color.[ComponentName].[Part].[State]
```

Examples:
```
C.Color.CommonButton.Container-Background.Enabled
C.Color.CommonButton.Container-Background.Hover
C.Color.Navigation.XL.Level-1.Label.Enabled
C.Color.BackToTop.Background.Enabled
C.Color.MoreMenu.Panel-Background
C.Color.SiteHeader.Background.Wide
C.Color.SiteHeader.Background.Narrow
C.Color.Footer-Sponsor.Background.Enabled
C.Color.BackToTop.Label.Enabled
C.Color.BackToTop.Icon.Enabled
```

**Component layer edits for brand forks:**

Most brand fork changes flow through Primitive and Semantic layers and cascade to all components. You only need to touch the Component layer when:

1. A specific component needs a different treatment on a specific surface (e.g., Navigation.XL on a dark header bar vs. a white flyout)
2. A new token needs to be added because Ghost core didn't tokenise a property (e.g., `SiteHeader.Background.Wide` was added for Inter Miami)
3. A component has a panel/overlay that needs brand colouring independently of its trigger (e.g., `MoreMenu.Panel-Background`)

---

## Token naming conventions

**Full token path structure:**
```
[Layer].[Namespace].[Category].[Surface].[Intent].[State]
```

- **Layer prefix:** `P.` (Primitive) / `S.` (Semantic) / `C.` (Component)
- **Namespace prefix in file:** `Primitive` / `Semantic` / `ColourSet` / `Component` (used as Tokens Studio token set names)
- **Surface:** `Default` or `Inverse` in Semantic; breakpoint or level in Component
- **State:** `Enabled`, `Hover`, `Active`, `Selected`, `Disabled`

**Tokens Studio token set names (correspond to JSON top-level keys):**
```
Primitive     → P.Color.*  
Semantic      → S.Color.*
ColourSet     → ColourSet.* (multiple sets: Default, CS-1 … CS-6, Inverse, Base-1, Base-2)
Component     → C.Color.*
```

**Figma shared plugin data (token bindings):**

Token bindings are stored on each Figma node as shared plugin data:
```js
node.getSharedPluginData('tokens', 'fill')     // fill colour token
node.getSharedPluginData('tokens', 'stroke')   // stroke/border token
node.getSharedPluginData('tokens', 'fontSize') // typography token
```

The value is a JSON-stringified token path: `"C.Color.BackToTop.Background.Enabled"`

---

## Two-channel rule (full detail)

Changes to the Figma file go through exactly two channels. Mixing them causes overwrite conflicts.

### Channel 1 — Token values → `tokens.json`

Use for: colour values, opacity, radius values, font sizes, font weights.

```
Edit tokens.json → git commit + push → Tokens Studio Pull → Apply to pages
```

This updates the *value* of a token. Every Figma node bound to that token gets the new value.

### Channel 2 — Structural changes → Figma Plugin API

Use for: corner radius on a specific node, layout direction, padding, width/height, variant property changes, image fills, constraints.

```
use_figma MCP tool → runs JS against Figma Plugin API → immediate effect in Figma
```

This edits Figma node properties directly. Token Studio does not control these properties (unless they're token-bound).

### What goes wrong when you mix the channels

If you set a node's fill colour directly via the Figma Plugin API without also updating the token binding (`setSharedPluginData`), that node's fill is no longer token-controlled. The next Tokens Studio apply will either:
- Leave it alone (if it has no binding), or
- Overwrite it with the old token value (if it has a stale binding)

**Rule:** Any time you set a fill via the Plugin API on a token-bound node, you must also call `node.setSharedPluginData('tokens', 'fill', JSON.stringify('NewToken.Path'))` to update the binding.

---

## Figma file structure

The Ghost design system lives across two Figma files:

| File | Purpose |
|---|---|
| **Ghost Core** (`David-Test-Ghost-Core-2.0` or brand equivalent) | All component masters, design system pages |
| **Ghost Content** (`David-Test-Ghost-Content-2.0`) | Page layouts using Core components |

**Core file pages:**

| Page | Contains |
|---|---|
| Components | Master component sets for all 28+ components |
| Chrome | SiteHeader, Navigation, MoreMenu, GlobalNav — all breakpoints and states |
| Footers | Footer, Footer-Branding, SponsorGrid, BackToTop, AppPromo — all variants |
| ColourSets | Colour context preview — each component × each ColourSet |
| Colour Matrix | Auto-generated WCAG audit output (also available as HTML from the script) |
| Brand Elements | Logo, crest, sponsor assets |

---

## ColourSet application in Figma

ColourSets are applied by wrapping a component instance in a frame that has the ColourSet token applied to its fill. Tokens Studio resolves token references through the ColourSet context of the nearest ancestor frame.

In practice this means:
- A `CommonButton` placed inside a `CS-3` surface frame will use CS-3-overridden token values
- The same `CommonButton` placed inside a `Default` surface frame uses Default values
- No changes to the component itself are needed — only the wrapper surface

**ColourSets that override the Button token:**

The `Component.C.Color.CommonButton.*` tokens are overridden at the ColourSet level for Button, Tab, and PageNavigation — these components have explicit per-ColourSet overrides because their primary colours vary significantly across surfaces.

```
ColourSet.Button.*        → overrides for CommonButton on each surface
ColourSet.Tab.*           → overrides for Tab on each surface
ColourSet.PageNavigation.* → overrides for PageNavigation on each surface
ColourSet.TextButton.*    → overrides for TextButton on each surface
```

---

## Accessibility standard

All token pairings must meet WCAG 2.1:

| Use | Standard | Minimum ratio |
|---|---|---|
| Body text, labels, link text | 1.4.3 AA | 4.5:1 |
| Large text (18pt+ or 14pt+ bold) | 1.4.3 AA18 | 3:1 |
| UI components (buttons, inputs, focus rings, borders) | 1.4.11 | 3:1 |

**DNP (Does Not Pass)** — A pairing that fails its applicable standard. DNPs must be explicitly accepted and documented in the brand fork file before being shipped. See the Known Issues section of each brand fork document.
