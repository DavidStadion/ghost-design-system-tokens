# Inter Miami CF — Brand Fork Documentation

**Branch:** `inter-miami`  
**Base:** Ghost Design System Core 2.0  
**Status:** In progress — token fixes applied, colour matrix generated

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

All changes are in `tokens.json` on the `inter-miami` branch. None of these touch the Primitive layer (which stays brand-specific). All fixes target the **Semantic** layer so they cascade to all components automatically.

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

---

## 6. Next Steps

- [ ] Decide on CS-5 surface / button contrast (see Known Issues §4)
- [ ] Footers page — apply Inter Miami brand treatment
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
