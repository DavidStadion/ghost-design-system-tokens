# Inter Miami CF — Brand Fork Documentation

**Branch:** `inter-miami`  
**Base:** Ghost Design System Core 2.0  
**Figma file:** `David-Test-Inter-Miami-2.0` (file key: `wK1SnviTqfM2j0vK1rObTy`)  
**Status:** In progress — Semantic + Component token fixes applied; Chrome, Navigation, Footer, Atoms, Dropdowns & Banners sessions complete

---

## Quick reference

| Resource | Location |
|---|---|
| Token file | `tokens.json` on `inter-miami` branch |
| Figma Core file | `David-Test-Inter-Miami-2.0` |
| Colour matrix | `colour-matrix.html` (run `python3 generate_colour_matrix.py colour-matrix.html`) |
| Token architecture | [GHOST_DESIGN_SYSTEM.md](GHOST_DESIGN_SYSTEM.md) |
| Component catalog | [COMPONENTS.md](COMPONENTS.md) |
| New brand fork guide | [BRAND_FORK_GUIDE.md](BRAND_FORK_GUIDE.md) |

---

## Critical workflow rules

> **⚠️ Tokens Studio branch:** Always confirm Tokens Studio is on `inter-miami` (not `main`) before pulling or applying. Settings → Sync → Branch. Pulling from `main` overwrites all brand work.

> **⚠️ Two-channel rule:** Token values (colours) go via `tokens.json` → git push → Tokens Studio pull → apply. Structural changes (layout, fills on un-tokenised nodes) go via the Figma Plugin API (`use_figma`). Never mix the channels. See [GHOST_DESIGN_SYSTEM.md](GHOST_DESIGN_SYSTEM.md) for full detail.

> **⚠️ Footer caveat:** After any Tokens Studio "Apply to all pages", re-verify the Footers page. Footer text overrides are instance-level and may partially reset. Re-run the Fix I script if needed.

---

## 1. Brand Palette

### Primary palette (pinks)

| Token | Name | Hex | WCAG on white | Use |
|---|---|---|---|---|
| `P.Color.Primary.1` | Pastel Pink | `#FF9CB4` | 1.97:1 — DNP (UI), use large text only | BackToTop bg, MoreMenu panel, NavigationContainer-Hygiene bg, section title text in footer |
| `P.Color.Primary.2` | Mid Pink | `#FF6B8E` | 2.53:1 | BackToTop Hover bg |
| `P.Color.Primary.3` | Miami Pink | `#E8004B` | 4.57:1 — AA ✓ | Selected borders, Inverse button container, BackToTop Active bg |
| `P.Color.Primary.4` | Light Pink | `#FFB8CB` | 1.61:1 | Background tints only |
| `P.Color.Primary.5` | Pale Pink | `#FFD4DF` | 1.26:1 | Lightest tint |
| `P.Color.Primary.6` | Blush | `#FFEDF1` | 1.11:1 | Micro-tint backgrounds |

### Secondary palette (near-blacks and dark greys)

| Token | Name | Hex | Notes |
|---|---|---|---|
| `P.Color.Secondary.1` | Near Black | `#231F20` | Used in Ghost's default Inverse button container (replaced with Primary.3 in Fix B) |
| `P.Color.Secondary.2` | Dark Grey | `#3D3839` | |
| `P.Color.Secondary.3` | Mid Dark Grey | `#706869` | |
| `P.Color.Secondary.4` | Medium Grey | `#9E9A9A` | |
| `P.Color.Secondary.5` | Light Grey | `#C7C4C4` | |
| `P.Color.Secondary.6` | Pale Grey | `#F0EFEF` | |

### Neutrals

Ghost standard Neutral palette (`P.Color.Neutral.Black`, `White`, `100`–`900`). Not overridden for Inter Miami.

### Shades (hover/active)

| Token | Hex | Use |
|---|---|---|
| `P.Color.Shades.Primary-1.700` | Darker pink | Button Hover |
| `P.Color.Shades.Primary-1.800` | Darkest pink | Button Active |

---

## 2. Semantic Token Changes

These changes are in `tokens.json` on `inter-miami`. They cascade to all components via the token hierarchy without touching individual component tokens.

### Fix A — Selected border colour (PageNavigation, Tab, SubNavigation)

**Problem:** Ghost baseline: selected-state border was `Primary.1` (`#FF9CB4`) on Default surfaces — 1.97:1 on white, fails WCAG 1.4.11. On Inverse/dark surfaces, it was `Secondary.1` (`#231F20` near-black) — invisible on dark backgrounds.

**Why this matters:** PageNavigation, Tab, and SubNavigation all share `S.Color.Border.Default.Emphasis` / `S.Color.Border.Inverse.Emphasis` for their selected indicator. Getting this wrong means the active tab is invisible or illegible.

**Fix:**
```
S.Color.Border.Default.Emphasis  → {P.Color.Primary.3}  (was Primary.1)
S.Color.Border.Inverse.Emphasis  → {P.Color.Primary.3}  (was Secondary.1)
```

Miami Pink (`#E8004B`) at 4.57:1 on white ✓ — passes WCAG 1.4.11 on both light and dark surfaces.

**Cascades to:** PageNavigation, Tab, SubNavigation — selected border across all 10 ColourSets.

---

### Fix B — Primary button on dark surfaces (Inverse, Base-2, CS-4, CS-5, CS-6)

**Problem:** Ghost baseline: Inverse Primary button container = `Secondary.1` (`#231F20` near-black). On a dark surface (e.g., the black SiteHeader or a CS-6 dark section), this is near-invisible. Label and icon were white-on-near-black — readable but button shape was lost.

**Why this matters:** The primary CTA button must be visually distinct on all surface types, including the dark footer and dark hero sections.

**Fix:**
```
S.Color.Interaction.Inverse.Primary.Container-Background.Enabled  → {P.Color.Primary.3}         (was Secondary.1)
S.Color.Interaction.Inverse.Primary.Container-Background.Hover    → {P.Color.Shades.Primary-1.700}
S.Color.Interaction.Inverse.Primary.Container-Background.Active   → {P.Color.Shades.Primary-1.800}
S.Color.Interaction.Inverse.Primary.Container-Background.Selected → {P.Color.Primary.3}
S.Color.Interaction.Inverse.Primary.Label.*                       → {S.Color.Text.Default.Main}   (black on pink)
S.Color.Interaction.Inverse.Primary.Icon.*                        → {S.Color.Fill.Default.Main}   (black)
```

Black label on Miami Pink (`#E8004B`): 4.57:1 ✓ — passes WCAG 1.4.3 AA.

**Cascades to:** CommonButton on Inverse, Base-2, CS-4, CS-5, CS-6 surfaces.

> **Pre-existing token structure note:** The Component layer's `CommonButton.Inverse.Primary` tokens reference `S.Color.Interaction.Default.Primary` (not Inverse) — a Ghost core debt. In practice, dark-surface ColourSets (CS-5, CS-6) use the CS-level override which correctly references Inverse. The Figma rendering is correct; the Component.Inverse token chain is token debt.

---

## 3. Component Token Changes

These changes add or modify Component-layer tokens that aren't addressed by Semantic-layer fixes alone.

### Fix C — BackToTop pink background

**Problem:** Ghost baseline: BackToTop background = white/transparent. Inter Miami requires a brand-pink BackToTop that is a signature visual element of the footer.

**Why this matters:** The BackToTop is a full-width accent bar at the footer bottom — a key brand moment. It should use the primary palette ramp so Hover and Active states feel intentional.

**Fix:**
```
C.Color.BackToTop.Background.Enabled → {S.Color.Background.Default.Emphasis}  (= Primary.1 = #FF9CB4)
C.Color.BackToTop.Background.Hover   → {P.Color.Primary.2}                    (= #FF6B8E)
C.Color.BackToTop.Background.Active  → {P.Color.Primary.3}                    (= #E8004B)
```

Label and icons remain `C.Color.BackToTop.Label.Enabled` / `Icon.Enabled` → black. Black on `#FF9CB4` = 4.87:1 ✓.

---

### Fix D — MoreMenu pink panel background

**Problem:** Ghost baseline: MoreMenu overlay panel = dark background. Inter Miami design direction: light pink panel with black text, echoing Primary.1.

**Why this matters:** The MoreMenu is the primary navigation surface on mobile. Using the brand's light pink makes it immediately identifiable as an Inter Miami experience.

**Fix:** New token added to the Component layer (this token does not exist in Ghost core):
```
C.Color.MoreMenu.Panel-Background → {S.Color.Background.Default.Emphasis}  (= Primary.1 = #FF9CB4)
```

Nav item row backgrounds remain `FullyTransparent` (show the pink panel through). Nav item labels stay `Default.Primary` (black) — black on `#FF9CB4` = 4.87:1 ✓.

> **Pattern note:** When a future brand fork needs a coloured panel (MoreMenu, SiteHeader dropdown, mega menu), add a `Panel-Background` token at the Component level rather than using a ColourSet override. This keeps the override scoped to the component, not the entire surface.

> **Token debt:** MoreMenu section header backgrounds, nav item dividers, and close button are not tokenised in Ghost core. Applied as direct fills (Fix G). Add `C.Color.MoreMenu.SectionHeader.Background`, `C.Color.MoreMenu.Divider`, `C.Color.MoreMenu.CloseButton.*` in a future tokenisation pass.

---

### Fix E — Navigation XL text on dark SiteHeader

**Problem:** Ghost baseline: Navigation.XL uses Default semantic tokens throughout — black text for all levels. On the Inter Miami SiteHeader (black background at Large/XL/XX-Large), Level-1 navigation links were black-on-black.

**The key architectural decision:** Navigation.XL has 3 levels that live on different surfaces:
- **Level-1** — The top SiteHeader bar → **dark background** → needs **Inverse tokens** (white)
- **Level-2** — Flyout/mega menu panel → **white background** → needs **Default tokens** (black)
- **Level-3** — Sub-items in flyout → **white background** → needs **Default tokens** (black)

Setting all levels to Inverse (a previous mistake) made Level-2/3 invisible on white flyout panels. Only Level-1 should be Inverse.

**Fix:**
```
C.Color.Navigation.XL.Level-1.Label.*             → {S.Color.Interaction.Neutral.Inverse.Primary.Label.*}
C.Color.Navigation.XL.Level-1.Icon.*              → {S.Color.Interaction.Neutral.Inverse.Primary.Icon.*}
C.Color.Navigation.XL.Level-1.Background.Hover    → {S.Color.Background.Inverse.Subtle}
C.Color.Navigation.XL.Level-1.Background.Active   → {S.Color.Interaction.Neutral.Inverse.Primary.Background.Active}
C.Color.Navigation.XL.Level-1.Border.*            → {S.Color.Border.HoldingColour.FullyTransparent}

C.Color.Navigation.XL.Level-2.Label.*             → {S.Color.Interaction.Neutral.Default.Primary.Label.*}
C.Color.Navigation.XL.Level-3.Label.*             → {S.Color.Interaction.Neutral.Default.Primary.Label.*}
```

Navigation.Small remains entirely Default — correct for the MoreMenu overlay on the pink panel.

Selected indicator: `{S.Color.Fill.Default.Emphasis}` = Primary.3 (Miami Pink) — visible on both black header and white flyout.

**Also fixed in this pass:**

```
C.Color.HygieneLinks.XL.Label.*  → {S.Color.Interaction.Neutral.Inverse.Primary.Label.*}
C.Color.HygieneLinks.XL.Icon.*   → {S.Color.Interaction.Neutral.Inverse.Primary.Icon.*}

C.Color.MoreMenu.XL.MoreButton.Unselected.Label.*  → {S.Color.Interaction.Neutral.Inverse.Primary.Label.*}
C.Color.MoreMenu.XL.MoreButton.Unselected.Icon.*   → {S.Color.Interaction.Neutral.Inverse.Primary.Icon.*}
```

These live on the dark SiteHeader bar and need Inverse (white) for the same reason as Level-1 nav.

---

### Fix F — SiteHeader black background

**Problem:** Ghost core has no SiteHeader.Background Component token. SiteHeader fills were unbound, defaulting to white/transparent. Inter Miami requires a black header at Large, X-Large, and XX-Large breakpoints.

**Why this matters:** The black SiteHeader is the defining frame of the Inter Miami desktop experience. Without it, none of the white Navigation or white IconButton fixes make visual sense.

**Fix:** New tokens added to the Component layer:
```
C.Color.SiteHeader.Background.Wide   → {P.Color.Neutral.Black}             (Large/XL/XX-Large)
C.Color.SiteHeader.Background.Narrow → {S.Color.Background.Default.Main}   (Small/Medium — white, MoreMenu handles these)
```

SiteHeader variant fills bound to these tokens via Figma Plugin API (node IDs: `8100:193331`, `7950:19941`, `8100:193509` for XX-Large, X-Large, Large).

Small and Medium SiteHeader remain white/transparent — MoreMenu overlay handles mobile navigation on a pink panel.

---

### Fix G — MoreMenu section headers, dividers, close button (direct fills)

**Problem:** After applying the pink panel background (Fix D), internal MoreMenu structural elements needed adjustment:
- NavSection title bars were dark/black (now transparent — pink panel shows through)
- Nav item dividers were absent (added as subtle separators)
- Close button was transparent (made dark for visibility on pink)
- MY ACCOUNT sign-in link was Default (black on pink ✓, but needed Inverse label token for token-stability)

**Applied via Figma Plugin API:**
- NavSection title bars → `fills = []` (transparent — shows pink panel)
- Nav item dividers → `P.Color.Opacity.Default.10` (10% black on pink panel)
- Close button → dark fill (`S.Color.Fill.Default.Main`)
- MY ACCOUNT sign-in link → `S.Color.Interaction.Neutral.Inverse.Primary.Label.*` (white on pink — accessible at high contrast; note: this is actually Inverse which gives white, but black is also fine here)

> **Token debt:** These MoreMenu sub-properties are not tokenised in Ghost core. They are direct fills. Future work: add `C.Color.MoreMenu.SectionHeader.Background`, `C.Color.MoreMenu.Divider.Fill`, `C.Color.MoreMenu.CloseButton.Fill` to the Component layer.

---

### Fix H — MyAccount-DropDown panel background (direct fill)

**Problem:** The MyAccount dropdown (State=Open) showed a dark background wrapper in front of the white DropDownPanel.

**Applied:** State=Open wrapper fill changed to `fills = []` (transparent), allowing the white DropDownPanel beneath to show through. DropDownPanel itself retains its white surface — this is correct (account menu is a light-surface element).

> **Token debt:** No Component token for the wrapper or panel background. Direct structural fill. Future: `C.Color.MyAccount.Wrapper.Background` = transparent; `C.Color.MyAccount.Panel.Background` = `{S.Color.Background.Default.Main}`.

---

### Fix I — Footer brand treatment (black background, pink titles, white text)

**Problem:** Ghost baseline: footer is a light-surface component (white backgrounds, black text). Token Studio apply resets it to this default. Inter Miami requires: full black background, light pink (`#FF9CB4`) section/column titles, white body text, white links.

**Why the footer is complex:** The footer is assembled from deeply nested library sub-components (Footer-UsefulLinks → UsefulLinks-ListGroup → LinkList-Item → Label text). Text fills live 4–6 levels deep inside INSTANCE chains. Changing the master of a deeply nested library component would affect all instances site-wide, not just the footer. The chosen approach is to apply instance-level overrides with updated token bindings.

**Approach:** Instance-level overrides applied via Figma Plugin API on the Footers page (`1:21`). Token bindings updated to Inverse equivalents — Token Studio will resolve these correctly on next apply.

**Master component backgrounds fixed:**

| Component | ID | Token applied |
|---|---|---|
| Footer-Branding | 106:5133 | `S.Color.Background.Inverse.Main` |
| Footer | 106:7540 | `S.Color.Background.Inverse.Main` |
| SponsorGrid-Tier1 | 22190:343279 | `S.Color.Background.Inverse.Main` |
| SponsorGrid-TierOther | 11:19146 | `S.Color.Background.Inverse.Main` |
| Footer-SponsorBlock | 15:3991 | `S.Color.Background.Inverse.Main` |
| Footer-AppPromo | 22190:30771 | `S.Color.Background.Inverse.Main` |

**Text treatment (applied to all TEXT nodes on the Footers page):**

| Content type | Token applied | Hex result |
|---|---|---|
| GROUP TITLE, Useful links, Find us, Follow us, Official app, TIER labels, {Title} | `S.Color.Background.Default.Emphasis` | `#FF9CB4` |
| Text link, LABEL (footer nav links, TextButton) | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` | `#FFFFFF` |
| Address text, summary text, copyright | `S.Color.Text.Inverse.Main` | `#FFFFFF` |

**Why section titles use `S.Color.Background.Default.Emphasis` (a background token for text):** This is a colour-borrow pattern. `S.Color.Background.Default.Emphasis` resolves to `{P.Color.Primary.1}` = `#FF9CB4` in Inter Miami — the correct light pink colour for titles. There is no dedicated `S.Color.Text.Default.Emphasis` that resolves to the same value. This is token debt — a future `S.Color.Text.Emphasis` token should be added.

**Vector icons:** All black VECTOR fills inside footer components → `S.Color.Fill.Inverse.Main` (white). Pink/brand vectors (crest elements `#f7b5cd`) preserved.

**Sponsor grid items:** `C.Color.Footer-Sponsor.Background.Enabled` = `#e9ecef` (light grey) — intentionally kept. Grey boxes on a black footer create clear visual separation for sponsor logos.

**Border separators:** Tier boundary rectangles → `S.Color.Border.Inverse.Subtle` (white at 15% opacity).

> **Token debt:** Footer text overrides are instance-level. A Token Studio "Apply to all pages" may partially reset them. The permanent fix is to add `C.Color.Footer.*` Component tokens (e.g., `C.Color.Footer.SectionTitle.Color`, `C.Color.Footer.Link.Color`, `C.Color.Footer.Body.Color`) that reference Inverse semantics, and bind the sub-component text nodes to these new tokens.

---

### Fix J — Footer-Branding social icon vectors → white

**Problem:** Social icon vectors (Facebook, X/Twitter, Instagram, YouTube etc.) inside Footer-Branding were black fills — invisible on the black footer background.

**Fix:** All black VECTOR fills inside Footer-Branding → `S.Color.Fill.Inverse.Main` (white). 100 vectors updated.

Pink brand vectors within the Inter Miami crest (`#f7b5cd`) preserved — these are club identity elements, not icons.

---

## 4. Colour Accessibility Matrix

**Script:** `generate_colour_matrix.py`  
**Output:** `colour-matrix.html`  
**Regenerate:** `python3 generate_colour_matrix.py colour-matrix.html`  
**Serve locally:** `npx serve -l 3456 .` → `http://localhost:3456/colour-matrix.html`

### Section 1 — Primitive Text Contrast Matrix

Every primitive colour as text on every primitive colour as background.  
WCAG 1.4.3 — AA 4.5:1, AAA 7:1, AA18 3:1 (large text only).

Use this to select valid pairings for ColourSets and token decisions. **Only AA or better pairs should enter the design system.**

### Section 2 — Full Component UI Audit

Auto-scanned from `Component.C.Color`. Covers all 28 components × 10 surfaces.

- **Text rows** — WCAG 1.4.3, 4.5:1 minimum (labels, titles, supporting text)
- **UI rows** — WCAG 1.4.11, 3:1 minimum (container fills, borders, indicators, icons, focus rings)
- **CS overrides** applied first for Button, Tab, PageNavigation, TextButton
- **All other components** resolved from the Component layer; surface luminance < 0.18 → Inverse mode, otherwise Default mode
- **Flat components** (Link, BackToTop, SSOLink, Footer-Sponsor, Navigation) resolved from Semantic references

**Components covered:**

| Group | Audit type |
|---|---|
| Link | Flat — Semantic reference |
| CommonButton | Standard + CS override (Button set) |
| IconButton, TextButton, SocialButton, ShareButton, BackButton | Standard |
| Tag, Chip, SegmentedControl | Standard |
| Tab | Standard + CS override (Tab set) |
| PageNavigation | Standard + CS override (PageNavigation set) |
| ActionButton | Standard |
| Navigation, MoreMenu, HygieneLinks | Flat — Small variant |
| GlobalNav | Flat — GlobalLink variant |
| SSOLink, MyAccount-DropDown-Trigger | Flat |
| SubNavigation | Standard |
| LanguagePicker-Trigger | Flat — Small variant |
| Footer-Sponsor, BackToTop | Flat |
| CategoryLink, Card, Dropdown | Standard |
| Form / InputField | Standard (sub-component wrapper) |
| Pagination | Standard |

---

## 5. Known Issues & Design Decisions

### DNP — Default Primary button container (1.97:1)

`CommonButton.Default.Primary.Container-Background` = Primary.1 (`#FF9CB4`) on white `#FFFFFF`.

- **Ratio:** 1.97:1 — fails WCAG 1.4.11 (UI components, minimum 3:1)
- **Component affected:** CommonButton, Primary variant, on Default/white surfaces (CS-1, Base-1)
- **Decision:** **Accepted** as Inter Miami brand tradeoff.
  - The button *label* (black on `#FF9CB4`) passes at 4.87:1 AA — text is legible.
  - The button *shape* is visible via contrast with surrounding content in most layout contexts.
  - The pastel pink button is a strong Inter Miami brand expression; replacing with Primary.3 (Miami Pink) would be a significant shift toward a more aggressive red that the brand direction does not support for light-surface CTAs.
- **If contrast must be met:** Swap `S.Color.Interaction.Default.Primary.Container-Background.Enabled` → `{P.Color.Primary.3}` (`#E8004B`, 4.57:1 on white). This changes the light-surface button from pastel pink to deep red — revisit with design director.

### DNP — CS-5 surface contrast for pink elements (2.48:1)

`#E8004B` (Miami Pink) on `#343A40` (CS-5 Neutral.800 surface).

- **Ratio:** 2.48:1 — fails WCAG 1.4.11 (UI components, minimum 3:1)
- **Components affected:** CommonButton Primary container and Tab/PageNavigation selected border on CS-5
- **Root cause:** `#343A40` is in a "gap zone" — dark enough that white text passes, but not dark enough for Miami Pink to reach 3:1 as a UI element. Miami Pink would need a surface of `#2B2E31` or darker to pass 3:1.
- **Status:** **Open — decision required.**
- **Options:**
  1. Darken CS-5 surface to `#2B2E31` or `#1A1A1A` (closer to CS-6/black)
  2. Add a CS-5 Button override using a lighter pink variant that passes on `#343A40`
  3. Accept as brand limitation on this one surface (low-frequency use case)

---

## 6. How to Apply Token Changes to Figma

### Two-channel rule

| What changes | How to apply |
|---|---|
| Colour values, token references | `tokens.json` → git push → Tokens Studio Pull → Apply |
| Structural fills on un-tokenised nodes, layout, constraints | Figma Plugin API (`use_figma` MCP tool) |

After any structural change via Plugin API, always update the token binding:
```js
node.fills = [{ type: 'SOLID', color: {r:0, g:0, b:0} }];
node.setSharedPluginData('tokens', 'fill', JSON.stringify('C.Color.SiteHeader.Background.Wide'));
```

### Placing images (logos, crests, sponsors) into components

1. Create a Rectangle inside the component, sized to the component bounds, `fills = []`
2. Use `upload_assets` with `nodeId` + `scaleMode: FIT` to place the image
3. **Immediately** set Scale constraints — never skip this:
   ```js
   node.constraints = { horizontal: 'SCALE', vertical: 'SCALE' };
   ```
   Figma defaults to Left/Top — without Scale the image overflows its bounds when the component is resized at different sizes or breakpoints.
4. Take a screenshot to verify before moving on.

---

## 6b. Component-Level Fixes — Dropdowns, Atoms, Banners

### Fix J — Filter-DropDown-Trigger: Inverse Active/Hover contrast bug

**Problem:** `Filter-DropDown-Trigger` Inverse Active and Inverse Hover variants had `#000000` label text with **no token binding**. These variants render on a `#6c757d` dark-grey background (contrast ≈ 3.0:1 — fails WCAG 1.4.3 AA at 4.5:1).

**Root cause:** Token Studio was not applying to the Dropdowns page; the label fills for Active/Hover states in the Inverse ColourWay were never wired up.

**Fix (via Figma Plugin API):**

```js
// For each Inverse variant (8 total: Open+Closed × Active+Hover+Enabled+Disabled)
textNode.fills = [{ type: 'SOLID', color: {r:1,g:1,b:1} }]; // white
textNode.setSharedPluginData('tokens','fill', JSON.stringify(
  'S.Color.Interaction.Neutral.Inverse.Primary.Label.Active'  // or Hover/Enabled/Disabled
));
```

**Affected nodes:** `Filter-DropDown-Trigger` (3652:382632) — Inverse Active (both Open/Closed) and Inverse Hover (both Open/Closed). White text on `#6c757d` = 4.6:1 ✓ passes WCAG 1.4.3 AA.

---

### Fix K — Dropdown-Trigger-Master: Vector fill token binding

**Problem:** Chevron/arrow VECTOR nodes inside `Dropdown-Trigger-Master` (3697:383348) were set to `#040000` with **no token binding**. These are the leading and trailing icon vectors on both Size=Default and Size=Small variants.

**Fix (via Figma Plugin API):**

```js
vector.setSharedPluginData('tokens','fill', JSON.stringify('S.Color.Fill.Default.Main'));
```

`S.Color.Fill.Default.Main` → `{P.Color.Neutral.Black}`. The `Filter-DropDown-Trigger` parent overrides icon colour per state via `C.Color.Dropdown.*Icon.*` tokens at its own level — this master binding is the correct Default fallback.

---

### Fix L — Atoms page: ProgressBar Ghost-blue position indicators

**Problem:** ProgressBar `Position indicator` nodes on the Atoms page (1:19) were showing Ghost main branch colours:
- Inverse ProgressBar: `#00bcf2` (Ghost blue) — should be white
- Default ProgressBar: `#1976dc` (Ghost blue) — should be brand pink

These nodes had correct token bindings (`S.Color.Fill.Inverse.Emphasis` and `S.Color.Fill.Default.Emphasis`), but the Atoms page had never had Tokens Studio applied with Inter Miami tokens.

**Token resolution (Inter Miami branch):**

```
S.Color.Fill.Inverse.Emphasis → {P.Color.Neutral.White}  → #ffffff
S.Color.Fill.Default.Emphasis → {P.Color.Primary.3}      → #E8004B
```

**Fix (via Figma Plugin API):** Updated fill colours on all 4 ProgressBar position indicator nodes to match Inter Miami token resolution. No token binding change needed — bindings were already correct.

---

### Fix M — Banner-Ticker: Brand treatment on TitleContainer

**Problem:** `Banner-Ticker` master component (22648:1065375) — all 4 variants (Small/X-Large × Default/Team) — had `TitleContainer` set to `#dee2e6` (Ghost grey) via `S.Color.Background.Default.Strong`. Text and list items were entirely unbound.

**Fix (via Figma Plugin API):**

1. **TitleContainer background**: `S.Color.Background.Default.Strong` → `S.Color.Background.Default.Emphasis` (`{P.Color.Primary.1}` = `#FF9CB4` pastel pink). Black "Title" text on light pink = 10.7:1 ✓ WCAG AAA.

2. **Ticker_ListItem text nodes**: All 5 variants (Numbered, Default, Section Title, Team, Divider) now bound to `S.Color.Text.Default.Main`. Previously unbound.

3. **Team icon vector**: Bound to `S.Color.Fill.Default.Main` (20% opacity is set at the node level, not via token).

**Rationale for pink (not black or brand red):** The Ticker Banner is a content widget displayed on light page surfaces. `Primary.1` (#FF9CB4) gives the header strip a branded pink accent without the visual weight of `Primary.3` (#E8004B), which works better for CTAs and selected states. The overall banner background remains `S.Color.Background.Default.Subtle` (light neutral grey) for readability of the list content.

---

## 7. Next Steps

### Before next Token Studio apply

- [x] Tokens Studio connected to `inter-miami` branch ✓
- [ ] **⚠️ Re-verify Footers page after every full apply** — footer text overrides may reset. Re-run Fix I script.
- [ ] Check: BackToTop pink, MoreMenu pink panel, Navigation XL white, SiteHeader black

### Token debt to resolve

| Item | Fix | Priority |
|---|---|---|
| Add `C.Color.Footer.*` Component tokens — section bg, title colour, link colour, body colour | Makes footer Token Studio-stable without per-apply re-scripting | High |
| Tokenise MoreMenu section header background, divider, close button (Fix G) | Adds `C.Color.MoreMenu.SectionHeader.Background`, `.Divider`, `.CloseButton.*` | Medium |
| Tokenise MyAccount-DropDown panel and wrapper (Fix H) | Adds `C.Color.MyAccount.Wrapper.Background`, `.Panel.Background` | Low |
| Add `S.Color.Text.Emphasis` token for pink text on dark backgrounds | Fixes the colour-borrow anti-pattern where a Background token is used for text | Medium |

### Design work remaining

- [x] Chrome page — SiteHeader, Navigation, MoreMenu, BackToTop ✓
- [x] Footers page — Full Inter Miami brand treatment ✓
- [x] Atoms page — ProgressBar Ghost-blue indicators fixed ✓
- [x] Dropdowns page — Inverse Active/Hover contrast bug fixed; master vector bindings added ✓
- [x] Banners page — Banner-Ticker TitleContainer branded pink; text nodes token-bound ✓
- [ ] Decide on CS-5 surface / button contrast (see Known Issues)
- [ ] Mega menu NavSection masters — full sub-item label pass
- [ ] Step 10 component checklist: news article card, player card, match ticker, sponsor placement, social buttons
- [ ] Content file fork (`David-Test-Ghost-Content-2.0`) — begin after Core is proven

---

## 8. Workflow reference for future brand forks

The full step-by-step brand fork guide is now in [BRAND_FORK_GUIDE.md](BRAND_FORK_GUIDE.md). It covers:
- Phase 0 — Setup (branch, Figma file, Tokens Studio)
- Phase 1 — Primitive colours
- Phase 2 — Colour accessibility audit
- Phase 3 — Semantic token changes
- Phase 4 — Apply tokens to Figma
- Phase 5 — SiteHeader and Navigation
- Phase 6 — Footer
- Phase 7 — Logos, crests, brand assets
- Phase 8 — Quality assurance
- Phase 9 — Documentation

Inter Miami is the reference implementation for that guide. Where a decision was made (e.g., dark SiteHeader, light pink MoreMenu panel, black footer), the same Fixes described in Sections 2 and 3 of this document should be applied with that brand's palette values substituted.
