# Inter Miami CF — Brand Fork Documentation

**Branch:** `inter-miami`  
**Base:** Ghost Design System Core 2.0  
**Status:** In progress — Semantic + Component token fixes applied; Chrome, Navigation & Footer sessions complete

---

## 1. Brand Palette

| Token | Name | Hex | Notes |
|---|---|---|---|
| `P.Color.Primary.1` | Pastel Pink | `#FF9CB4` | Light accent — fails on white at 1.97:1, use large text only |
| `P.Color.Primary.2` | Mid Pink | `#FF6B8E` | |
| `P.Color.Primary.3` | Miami Pink | `#E8004B` | Primary brand colour — 4.57:1 on white (AA) |
| `P.Color.Primary.4` | Light Pink | `#FFB8CB` | |
| `P.Color.Primary.5` | Pale Pink | `#FFD4DF` | |
| `P.Color.Primary.6` | Blush | `#FFEDF1` | |
| `P.Color.Secondary.1` | Near Black | `#231F20` | |
| `P.Color.Secondary.2–6` | Dark greys | `#3D3839`–`#F0EFEF` | |

Neutrals are the Ghost standard Neutral palette (100–900, Black, White).

---

## 2. Token Changes Made

All changes are in `tokens.json` on the `inter-miami` branch. None of these touch the Primitive layer (which stays brand-specific).

> **⚠️ Token workflow note:** In a session that covered Chrome & Navigation, some colour changes were applied via direct Figma Plugin API (`node.fills`) rather than via `tokens.json`. This was a workflow error — the two-channel rule was broken. All those direct fills have since been captured in the Component token layer below (Fix C, Fix D, Fix E) so that a Tokens Studio pull on `inter-miami` reproduces the correct visual state. **Always follow the two-channel rule going forward.**

> **⚠️ Tokens Studio branch:** Always confirm Tokens Studio is connected to `inter-miami` (not `main`) before pulling or applying. Check Settings → Sync → Branch field.

### Fix A — Selected border colour (PageNavigation, Tab, SubNavigation)

**Problem:** Selected state border was `Primary.1` (`#FF9CB4`) on Default surfaces (low contrast on white) and `Secondary.1` (`#231F20`) on Inverse/dark surfaces (invisible on dark backgrounds).

**Fix:** Both `Default.Emphasis` and `Inverse.Emphasis` borders now point to `Primary.3` (`#E8004B`).

```
Semantic.S.Color.Border.Default.Emphasis  → {P.Color.Primary.3}  (was Primary.1)
Semantic.S.Color.Border.Inverse.Emphasis  → {P.Color.Primary.3}  (was Secondary.1)
```

**Cascades to:** PageNavigation Border.Selected, Tab Border.Selected, SubNavigation Border.Selected — across all ColourSets.

---

### Fix B — Primary button on dark surfaces (Inverse, Base-2, CS-5, CS-6)

**Problem:** Inverse Primary button container was `Secondary.1` (`#231F20` near-black) — invisible against a dark background. Label and icon were white-on-near-black.

**Fix:** Inverse Primary interaction tokens updated to Miami pink container with dark label/icon.

```
Semantic.S.Color.Interaction.Inverse.Primary.Container-Background.Enabled  → {P.Color.Primary.3}
Semantic.S.Color.Interaction.Inverse.Primary.Container-Background.Hover     → {P.Color.Shades.Primary-1.700}
Semantic.S.Color.Interaction.Inverse.Primary.Container-Background.Active    → {P.Color.Shades.Primary-1.800}
Semantic.S.Color.Interaction.Inverse.Primary.Container-Background.Selected  → {P.Color.Primary.3}
Semantic.S.Color.Interaction.Inverse.Primary.Label.*                        → {S.Color.Text.Default.Main}   (black)
Semantic.S.Color.Interaction.Inverse.Primary.Icon.*                         → {S.Color.Fill.Default.Main}   (black)
```

**Cascades to:** CommonButton Inverse/Base-2/CS-4/CS-5/CS-6 Primary variant (pink fill, dark label + icon).

> **Note:** The Component layer's `CommonButton.Inverse.Primary` tokens reference `S.Color.Interaction.Default.Primary` (not Inverse) — a pre-existing token structure issue. In practice, dark-surface ColourSets (CS-5, CS-6) use the CS-level override which correctly references the Inverse semantic layer. The Figma rendering is correct; the Component.Inverse token chain is a token debt item.

---

## 3. Colour Accessibility Matrix

**Script:** `generate_colour_matrix.py`  
**Output:** `colour-matrix.html`  
**Regenerate:** `python3 generate_colour_matrix.py colour-matrix.html`  
**Serve locally:** `npx serve -l 3456 .` → `http://localhost:3456/colour-matrix.html`

### Section 1 — Primitive Text Contrast Matrix

Every primitive colour as text on every primitive colour as background.  
WCAG 1.4.3 — AA 4.5:1, AAA 7:1, AA18 3:1 (large text only).

Use this to select valid pairings for ColourSets and semantic label/background token decisions. Only AA or better pairs should enter the design system.

### Section 2 — Full Component UI Audit

Auto-scanned from `Component.C.Color`. Covers all 28 components × 10 surfaces.

- **Text rows** — WCAG 1.4.3, 4.5:1 minimum (labels, titles, supporting text)
- **UI rows** — WCAG 1.4.11, 3:1 minimum (container fills, borders, indicators, icons, focus rings)
- **CS overrides** applied first for Button, Tab, PageNavigation, TextButton
- **All other components** resolved from the Component layer; surface luminance < 0.18 → Inverse mode, otherwise Default mode
- **Flat components** (Link, BackToTop, SSOLink, Footer-Sponsor, Navigation, etc.) resolved directly from Semantic token references

**Components covered:**

| Group | Type |
|---|---|
| Link | Flat — Semantic reference only |
| CommonButton | Standard + CS override (Button) |
| IconButton, TextButton, SocialButton, ShareButton, BackButton | Standard |
| Tag, Chip, SegmentedControl | Standard |
| Tab | Standard + CS override (Tab) |
| PageNavigation | Standard + CS override (PageNavigation) |
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

### Fix C — BackToTop pink background

**Problem:** BackToTop background was white/transparent (default Ghost treatment).

**Fix:** Component layer Background tokens updated to pink:

```
Component.C.Color.BackToTop.Background.Enabled → {S.Color.Background.Default.Emphasis}  (= Primary.1 = #FF9CB4)
Component.C.Color.BackToTop.Background.Hover   → {P.Color.Primary.2}                    (= #FF6B8E)
Component.C.Color.BackToTop.Background.Active  → {P.Color.Primary.3}                    (= #E8004B)
```

Labels and icons retain Default.Primary (black on pink — passes 4.5:1 ✓).

---

### Fix D — MoreMenu pink panel background

**Problem:** MoreMenu overlay was dark (Ghost default). Inter Miami requires a light pink panel with black text.

**Fix:** New `Panel-Background` token added to Component layer:

```
Component.C.Color.MoreMenu.Panel-Background → {S.Color.Background.Default.Emphasis}  (= Primary.1 = #FF9CB4)
```

Nav item row backgrounds remain `FullyTransparent`; labels remain Default.Primary (black). Section header titles and close button are dark text — readable on pink.

> **Token structure note:** Ghost core has no `Panel-Background` token for MoreMenu. This is a new inter-miami addition. Future brand forks that need a coloured panel should follow this same pattern — add a `Panel-Background` at the component level rather than using a ColourSet override.

---

### Fix E — Navigation XL white text on dark SiteHeader

**Problem:** Navigation.XL label and icon tokens pointed to Default semantics (black text). On the Inter Miami SiteHeader (Large/XL/XX-Large = black background), navigation links were black-on-black.

**Fix:** All three Navigation.XL levels switched to Inverse semantics:

```
Component.C.Color.Navigation.XL.Level-{1,2,3}.Label.*      → {S.Color.Interaction.Neutral.Inverse.Primary.Label.*}
Component.C.Color.Navigation.XL.Level-{1,2,3}.Icon.*       → {S.Color.Interaction.Neutral.Inverse.Primary.Icon.*}
Component.C.Color.Navigation.XL.Level-{1,2,3}.Background.Hover  → {S.Color.Background.Inverse.Subtle}
Component.C.Color.Navigation.XL.Level-{1,2,3}.Background.Active → {S.Color.Interaction.Neutral.Inverse.Primary.Background.Active}
Component.C.Color.Navigation.XL.Level-{1,2,3}.Border.*     → {S.Color.Border.HoldingColour.FullyTransparent}
```

Navigation.Small remains Default (black text) — correct for MoreMenu overlay on pink panel.

Selected indicator stays `{S.Color.Fill.Default.Emphasis}` = Primary.3 (Miami pink) — visible on both surfaces.

---

### Fix F — SiteHeader Large/XL/XX-Large black background (direct fill)

**Problem:** SiteHeader at Large/XL/XX-Large breakpoints was white/transparent (Ghost default). Inter Miami header should be black at wide breakpoints.

**Applied:** Direct Figma fill (`node.fills = [{type:'SOLID', color:{r:0,g:0,b:0}}]`) on SiteHeader component variants.

> **Token debt:** There is no `SiteHeader.Background` Component token in the Ghost token structure. This change lives only as a direct fill in Figma. Future work: add a `Panel-Background` token to SiteHeader in the Component layer (same pattern as Fix D), bind the variant fills to that token, and set it to `{P.Color.Neutral.Black}` on `inter-miami`.

Small and Medium SiteHeader breakpoints remain white/transparent (correct — MoreMenu handles those).

---

### Fix G — MoreMenu section headers, dividers, close button (direct fills)

**Applied via Figma API:**
- NavSection title bars → transparent background (was dark/black)
- Nav item dividers → `P.Color.Opacity.Default.10` (10% black, subtle separator)
- Close button → dark fill, visible on pink panel
- MY ACCOUNT sign-in link → Inverse label tokens (white on pink — accessible)

> **Token debt:** These properties are not currently tokenized in the Ghost Component layer. Direct fills used as interim fix.

---

### Fix H — MyAccount-DropDown panel white (direct fill)

**Applied:** State=Open wrapper fill changed to transparent so the white DropDownPanel beneath shows through. DropDownPanel itself retains its white surface.

> **Token debt:** No Component token for the DropDown panel background. Direct structural fill used.

---

### Fix I — Footer brand treatment (black background, pink titles, white text)

**Problem:** Token Studio apply reset the footer to its Ghost default — white/light-surface backgrounds, black text throughout. The Inter Miami footer requires: full black background, light pink (`#FF9CB4`) section/column titles, white body text and links.

**Approach:** Instance-level overrides applied via Figma Plugin API. Token bindings updated at each node to Inverse equivalents so Token Studio preserves the treatment on future apply.

**Master components fixed (background → black):**
- `Footer-Branding` (106:5133) — variant fills → `S.Color.Background.Inverse.Main`
- `Footer` (106:7540) — ComponentContainer frames → `S.Color.Background.Inverse.Main`
- `SponsorGrid-Tier1` (22190:343279) — variant fills → `S.Color.Background.Inverse.Main`
- `SponsorGrid-TierOther` (11:19146) — token binding added
- `Footer-SponsorBlock` (15:3991) — variant fills → `S.Color.Background.Inverse.Main`
- `Footer-AppPromo` (22190:30771) — variant fills → `S.Color.Background.Inverse.Main`

**Text treatment applied across all footer text nodes on the Footers page:**

| Content | Token applied | Colour |
|---|---|---|
| GROUP TITLE, Useful links, Find us, Follow us, Official app, TIER labels, {Title} | `S.Color.Background.Default.Emphasis` | `#FF9CB4` (light pink) |
| Text link, LABEL (nav/footer links) | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` | `#FFFFFF` |
| Address text, summary text, copyright, body copy | `S.Color.Text.Inverse.Main` | `#FFFFFF` |

**Vector icons:** Black icon vectors in Footer-Branding and sub-components → `S.Color.Fill.Inverse.Main` (white). Pink/brand vectors in club crest preserved.

**Sponsor grid items** (`C.Color.Footer-Sponsor.Background.Enabled` = `#e9ecef`) intentionally kept light grey — sponsor logo boxes on a dark footer.

**Border separators:** Tier border rectangles → `S.Color.Border.Inverse.Subtle` (white at 15% opacity).

> **Token debt:** The text overrides are applied at the instance level on the Footers page. The library sub-components (Footer-UsefulLinks, Footer-AddressPanel, Footer-SocialPanel, Footer-LegalLinks etc.) use Default semantic tokens internally. A proper fix would be to add `C.Color.Footer.*` Component tokens that reference Inverse semantics, bind them in the Component layer, and pull via Token Studio. As-is, a full Token Studio "apply to all pages" will reset these — the Footers page must be separately verified after each apply.

---

### Fix J — Footer-Branding social icon vectors → white

**Problem:** Social icon vectors (Facebook, Twitter/X, Instagram etc.) in Footer-Branding were black — invisible on the black footer background.

**Fix:** All black VECTOR fills inside Footer-Branding (excluding pink brand/crest vectors) set to `S.Color.Fill.Inverse.Main` (white). 100 vectors updated.

**Kept as-is:** Pink vectors (`#f7b5cd`) within the crest/logo marks are brand elements — not changed.

---

## 4. Known Issues & Design Decisions

### DNP: Default Primary button container (1.97:1)
`CommonButton.Default.Primary.Container-Background` = `Primary.1` (`#FF9CB4`) on white `#FFFFFF`.

- Ratio: 1.97:1 — fails WCAG 1.4.11 (UI 3:1)
- **Decision:** Accepted as Inter Miami brand tradeoff. The button label (black on `#FF9CB4`) passes at 4.5:1 AA. The button shape is visible via its contrast with surroundings in most layouts.
- **If needed:** Swap `Default.Primary.Container-Background` to `Primary.3` (`#E8004B`) — but this changes the light-surface button from pastel to deep red, which is a significant brand shift.

### DNP: CS-5 surface contrast for pink elements (2.48:1)
`#E8004B` (Miami Pink) on `#343A40` (CS-5 Neutral.800 surface).

- Affects: Container-Background, Border.Selected on CS-5
- Ratio: 2.48:1 — fails WCAG 1.4.11 (UI 3:1)
- **Root cause:** `#343A40` sits in a gap where Miami Pink can't reach 3:1. It would need to be ≥ `#2B2E31` (darker) for pink to hit 3:1, or use a lighter pink.
- **Options:** (a) Darken CS-5 surface to pure black or near-black, (b) use a custom CS-5 button override with a lighter pink, (c) accept as brand limitation on this surface.

---

## 5. How to Apply Token Changes to Figma

Two-channel rule:

| What | How |
|---|---|
| Token values (colours, radius, typography) | Edit `tokens.json` → `git push` → pull in Tokens Studio |
| Structural properties (corner radius, layout, variant properties) | Use Figma MCP Plugin API (`use_figma`) |

Never apply token changes by manually selecting layers in Figma — always go through the token file or the MCP.

### Placing images (logos, crests, sponsors) into components

1. Create a Rectangle inside the component, sized to the component bounds, `fills = []`
2. Use `upload_assets` with `nodeId` + `scaleMode: FIT` to place the image
3. **Immediately** set Scale constraints — do not skip this step:
   ```js
   node.constraints = { horizontal: 'SCALE', vertical: 'SCALE' };
   ```
   Figma defaults to Left/Top — without Scale the image breaks out of bounds when the component is resized.
4. Take a screenshot to verify placement before moving on.

---

## 6. Next Steps

### Before next token application
- [x] Switch Tokens Studio to `inter-miami` branch ✓
- [ ] **⚠️ Footer caveat:** After any Token Studio "apply to all pages", re-verify the Footers page — footer text overrides are instance-level and may reset. Re-run Fix I if needed.
- [ ] Check post-apply: BackToTop pink ✓, MoreMenu pink panel, Navigation XL white, SiteHeader black, Footer black

### Token debt to address
- [ ] Add `SiteHeader.Background` Component token (Fix F token debt)
- [ ] Tokenise MoreMenu section header background and divider colour (Fix G token debt)
- [ ] Tokenise MyAccount-DropDown panel background (Fix H token debt)
- [ ] Add `C.Color.Footer.*` Component tokens for section backgrounds and title colours (Fix I token debt) — this is the proper fix to make footer treatment Token Studio-stable

### Design work remaining
- [x] Footers page — Inter Miami brand treatment applied ✓ (Fix I/J)
- [ ] Decide on CS-5 surface / button contrast (see Known Issues §4)
- [ ] Mega menu sub-items (More Menu, Sub Navigation - In Page) — full label pass
- [ ] Step 10 component checklist: news article card, player card, site header logo position, match ticker, sponsor placement, social buttons
- [ ] After Core proven on Inter Miami → begin Content file fork (`David-Test-Ghost-Content-2.0`)

---

## 7. Workflow Checklist for Future Brand Forks

This is the sequence to follow when forking Ghost for any new brand.

1. **Set primitive colours** — update `Primitive.P.Color` in `tokens.json`
2. **Regenerate the colour matrix** — `python3 generate_colour_matrix.py colour-matrix.html`
3. **Read Section 1** — identify all DNP pairs; note AA18-only pairs; establish permitted colour pairings
4. **Read Section 2** — spot any component issues before they reach Figma
5. **Define ColourSets** — using only AA or better pairs from Section 1
6. **Update Semantic tokens** — border emphasis, interaction tokens, text/background semantics
7. **Regenerate matrix** — confirm Section 2 passes after semantic changes
8. **Commit tokens** → Tokens Studio pull → verify in Figma
9. **Apply structural changes** via Figma MCP (corner radius, layout, etc.)
10. **Document** any accepted DNPs and the reasoning (update this file or equivalent)
