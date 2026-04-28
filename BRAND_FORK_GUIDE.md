# Ghost Design System — Brand Fork Guide

This guide walks through every step to fork the Ghost Design System for a new football club brand. Follow it in order. Each step builds on the last — skipping ahead creates rework.

The goal of this document is to be comprehensive enough that a new brand fork can be completed from start to finish using only this guide, `tokens.json`, and the Figma file.

---

## Prerequisites

Before starting, you need:

- [ ] Access to the `DavidStadion/ghost-design-system-tokens` GitHub repo
- [ ] Tokens Studio installed in Figma (Plugins → Tokens Studio for Figma)
- [ ] The Figma Core file for the brand (duplicate from the Ghost Core master)
- [ ] The brand's colour palette (primary, secondary, neutral) with confirmed hex values
- [ ] Python 3 installed locally (for the colour matrix script)
- [ ] The MCP Figma plugin configured (for structural Figma changes)

---

## Phase 0 — Setup

### 0.1 Create the branch

```bash
git clone https://github.com/DavidStadion/ghost-design-system-tokens.git
cd ghost-design-system-tokens
git checkout main
git checkout -b [brand-slug]   # e.g. arsenal, tottenham, lfc
git push -u origin [brand-slug]
```

### 0.2 Duplicate the Figma Core file

In Figma: open the Ghost Core master file → right-click → Duplicate. Rename it `[Studio]-[ClubName]-Core-[Version]` (e.g. `David-Test-Arsenal-Core-2.0`).

Note down the Figma file key from the URL (the string after `/design/`). You'll need it for Figma MCP tool calls.

### 0.3 Connect Tokens Studio to the branch

In the duplicated Figma file:

1. Tokens Studio → Settings → Sync → GitHub
2. Set:
   - **Repository:** `DavidStadion/ghost-design-system-tokens`
   - **Branch:** `[brand-slug]`
   - **File path:** `tokens.json`
3. Click **Save**
4. Click **Pull** — confirm you get the Ghost baseline token values
5. **Do not Apply yet.** The primitives aren't set to the brand palette yet.

### 0.4 Create the brand fork documentation file

Copy `INTER_MIAMI_BRAND_FORK.md` to `[BRAND]_BRAND_FORK.md` (e.g. `ARSENAL_BRAND_FORK.md`). Clear the fix sections and Known Issues. Update the palette table. Commit the empty shell to the branch now — add to it as you work.

```bash
cp INTER_MIAMI_BRAND_FORK.md ARSENAL_BRAND_FORK.md
# Edit the file — update name, palette, clear old fixes
git add ARSENAL_BRAND_FORK.md
git commit -m "[Brand] — brand fork doc initialised"
git push
```

---

## Phase 1 — Primitive colours

**Goal:** Set the brand's raw colour values. This is the only time you edit the Primitive layer directly.

### 1.1 Identify the brand palette

You need (at minimum):
- 6 shades of the primary brand colour (Primary.1 lightest → Primary.6 is a tint/accent)
- 6 shades of the secondary brand colour (if the brand has one; use neutrals if not)
- Confirm whether the brand uses the Ghost standard neutrals or has its own black/dark

**Primary.3 is the key value** — it must pass WCAG 1.4.11 (3:1) against white for use on buttons and selected indicators. If the brand's hero colour doesn't pass 3:1 on white, it cannot be Primary.3; it must be a darker variant.

**Shade generation:** Use a tool like [Colorbox](https://colorbox.io/) or a custom script to generate a consistent 6-stop ramp from the brand colour. The ramp should be:
- Primary.1 — very light (pastel/tint) — around 90-95% lightness
- Primary.2 — light
- Primary.3 — the actual brand colour (or darkened to pass 3:1 on white)
- Primary.4 — medium light
- Primary.5 — pale
- Primary.6 — palest blush (for subtle backgrounds)

Additionally create hover/active shades for button states:
- `P.Color.Shades.Primary-1.700` — hover (slightly darker than Primary.3)
- `P.Color.Shades.Primary-1.800` — active (darker still)
- `P.Color.Shades.Primary-1.900` — pressed

### 1.2 Update tokens.json

In `tokens.json`, locate `Primitive.P.Color.Primary` and update the values:

```json
"Primitive": {
  "P": {
    "Color": {
      "Primary": {
        "1": { "value": "#[lightest]", "type": "color" },
        "2": { "value": "#[light]", "type": "color" },
        "3": { "value": "#[brand-colour]", "type": "color" },
        "4": { "value": "#[medium-light]", "type": "color" },
        "5": { "value": "#[pale]", "type": "color" },
        "6": { "value": "#[blush]", "type": "color" }
      },
      "Secondary": {
        "1": { "value": "#[near-black]", "type": "color" },
        ...
      },
      "Shades": {
        "Primary-1": {
          "700": { "value": "#[hover]", "type": "color" },
          "800": { "value": "#[active]", "type": "color" },
          "900": { "value": "#[pressed]", "type": "color" }
        }
      }
    }
  }
}
```

### 1.3 Commit and document

```bash
git add tokens.json
git commit -m "[Brand] — Set primitive colour palette"
git push
```

In the brand fork doc, fill in the palette table (hex values + WCAG notes for Primary.1 and Primary.3 on white).

---

## Phase 2 — Colour accessibility audit

**Goal:** Before touching any Semantic or Component token, know exactly which colour pairings are safe. This is the source of truth for all decisions.

### 2.1 Pull tokens into Figma

Tokens Studio → Pull. Do not Apply yet — just confirming the file is synced.

### 2.2 Run the colour matrix

```bash
python3 generate_colour_matrix.py colour-matrix.html
npx serve -l 3456 .
# Open http://localhost:3456/colour-matrix.html
```

### 2.3 Read Section 1 — Primitive text contrast matrix

For each pairing:
- ✅ **AA (4.5:1+)** — safe for body text, labels, link text
- ✅ **AA18 (3:1–4.49:1)** — safe for large text (18pt+, or 14pt+ bold) only
- ❌ **DNP** — do not use as text/background pairing

**Record the permitted pairings for ColourSet decisions.** The key questions:

1. What colour can Primary.3 (brand colour) be used on as a background? (text on brand bg)
2. Can Primary.1 (light pink) be used as a button background? (label on Primary.1 bg)
3. What are the valid text colours on Primary.3?

### 2.4 Read Section 2 — Component UI audit

Look for ❌ in the component rows. Common issues on new brand forks:

- **Selected border on Default surface** — if Primary.3 doesn't reach 3:1 on white, Fix A is needed
- **Primary button container on Inverse surface** — if Secondary.1 (near-black) can't hold a visible button on dark bg, Fix B is needed
- **CS-5 surface** — dark grey surfaces where Primary colours often fail at 3:1

### 2.5 Document DNPs

In the brand fork doc, record any DNP pairings that are accepted as brand tradeoffs, with the ratio, the component affected, and the decision.

---

## Phase 3 — Semantic token changes

**Goal:** Update the Semantic layer so the brand's colours flow correctly into all components.

Work through each of the following checks. Only edit tokens that need changing — most Semantic tokens are inherited correctly from the Ghost baseline.

### Fix A — Selected border colour

**Check:** In Section 2 of the colour matrix, do PageNavigation, Tab, and SubNavigation show a passing selected border on Default and Inverse surfaces?

**If failing:** Update both border emphasis tokens:

```json
"S.Color.Border.Default.Emphasis": { "value": "{P.Color.Primary.3}" },
"S.Color.Border.Inverse.Emphasis": { "value": "{P.Color.Primary.3}" }
```

**Cascades to:** PageNavigation, Tab, SubNavigation — selected state borders across all ColourSets.

### Fix B — Primary button on dark surfaces

**Check:** Does `CommonButton.Inverse.Primary` show as visible on Inverse/Base-2/CS-5/CS-6 surfaces?

**If the Ghost default (Secondary.1 near-black container on dark bg) is invisible:**

```json
"S.Color.Interaction.Inverse.Primary.Container-Background.Enabled": { "value": "{P.Color.Primary.3}" },
"S.Color.Interaction.Inverse.Primary.Container-Background.Hover": { "value": "{P.Color.Shades.Primary-1.700}" },
"S.Color.Interaction.Inverse.Primary.Container-Background.Active": { "value": "{P.Color.Shades.Primary-1.800}" },
"S.Color.Interaction.Inverse.Primary.Container-Background.Selected": { "value": "{P.Color.Primary.3}" },
"S.Color.Interaction.Inverse.Primary.Label.Enabled": { "value": "{S.Color.Text.Default.Main}" },
"S.Color.Interaction.Inverse.Primary.Label.Hover": { "value": "{S.Color.Text.Default.Main}" },
"S.Color.Interaction.Inverse.Primary.Label.Active": { "value": "{S.Color.Text.Default.Main}" },
"S.Color.Interaction.Inverse.Primary.Icon.Enabled": { "value": "{S.Color.Fill.Default.Main}" }
```

**Cascades to:** CommonButton Inverse/Base-2/CS-4/CS-5/CS-6 Primary variant.

### Fix C — BackToTop background

**Default Ghost treatment:** white/transparent. Most brands want a brand-coloured BackToTop.

```json
"C.Color.BackToTop.Background.Enabled": { "value": "{S.Color.Background.Default.Emphasis}" },
"C.Color.BackToTop.Background.Hover": { "value": "{P.Color.Primary.2}" },
"C.Color.BackToTop.Background.Active": { "value": "{P.Color.Primary.3}" }
```

Verify that the BackToTop label (black) passes 4.5:1 on the Enabled background colour.

### Fix D — MoreMenu panel background

**Default Ghost treatment:** dark panel. If the brand needs a light/brand-coloured panel:

```json
"C.Color.MoreMenu.Panel-Background": { "value": "{S.Color.Background.Default.Emphasis}" }
```

This is a new token (not in Ghost core) — it must be added to the Component section of `tokens.json`.

### Review — ColourSet overrides

After Semantic changes, re-run the colour matrix. Review CS-3 and CS-4 (brand-coloured surfaces) in Section 2:

- Text on brand-coloured surfaces should be white if the brand colour is dark
- Button Primary on brand-coloured surfaces should be readable

Add or adjust `ColourSet.Button.*` and `ColourSet.Tab.*` entries as needed.

---

## Phase 4 — Apply tokens to Figma

### 4.1 Commit all token changes

```bash
git add tokens.json
git commit -m "[Brand] — Semantic and Component token fixes (A–D)"
git push
```

### 4.2 Pull in Tokens Studio

Tokens Studio → Pull. Confirm "You have unsaved changes" does not appear (if it does, discard and re-pull from the branch).

### 4.3 Apply to pages

Tokens Studio → Apply to → Select all pages → Apply.

### 4.4 Verify in Figma

After applying, check in this order:

- [ ] Selected borders (Tab, PageNavigation, SubNavigation) — brand pink, both Default and Inverse surfaces
- [ ] Primary button on Default surface — correct brand colour
- [ ] Primary button on Inverse/dark surfaces — brand pink, not black/invisible
- [ ] BackToTop — brand pink background
- [ ] MoreMenu panel — brand colour (if Fix D was applied)

---

## Phase 5 — SiteHeader and Navigation

This phase handles the desktop SiteHeader and how navigation renders on dark vs. light headers.

### 5.1 Decide: is the SiteHeader dark or light?

| Header style | Navigation.XL.Level-1 treatment |
|---|---|
| Dark (black/brand colour) | Inverse tokens → white text, white icons |
| Light (white) | Default tokens → black text, black icons (Ghost baseline — no changes needed) |

### 5.2 Dark SiteHeader — token updates

If the SiteHeader is dark:

**Add SiteHeader.Background tokens** (new — not in Ghost core):
```json
"C.Color.SiteHeader.Background.Wide": { "value": "{P.Color.Neutral.Black}" },
"C.Color.SiteHeader.Background.Narrow": { "value": "{S.Color.Background.Default.Main}" }
```

**Update Navigation.XL.Level-1** to Inverse:
```json
"C.Color.Navigation.XL.Level-1.Label.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled}" },
"C.Color.Navigation.XL.Level-1.Label.Hover": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Hover}" },
"C.Color.Navigation.XL.Level-1.Label.Active": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Active}" },
"C.Color.Navigation.XL.Level-1.Label.Selected": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Selected}" },
"C.Color.Navigation.XL.Level-1.Icon.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Icon.Enabled}" },
"C.Color.Navigation.XL.Level-1.Icon.Selected": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Icon.Selected}" },
"C.Color.Navigation.XL.Level-1.Background.Hover": { "value": "{S.Color.Background.Inverse.Subtle}" },
"C.Color.Navigation.XL.Level-1.Background.Active": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Background.Active}" }
```

**Keep Navigation.XL.Level-2 and Level-3 as Default** (they appear in white flyout panels):
```json
"C.Color.Navigation.XL.Level-2.Label.Enabled": { "value": "{S.Color.Interaction.Neutral.Default.Primary.Label.Enabled}" },
"C.Color.Navigation.XL.Level-3.Label.Enabled": { "value": "{S.Color.Interaction.Neutral.Default.Primary.Label.Enabled}" }
```

**Update HygieneLinks.XL** to Inverse (they're also on the dark SiteHeader bar):
```json
"C.Color.HygieneLinks.XL.Label.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled}" },
"C.Color.HygieneLinks.XL.Icon.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Icon.Enabled}" }
```

**Update MoreMenu.XL.MoreButton** to Inverse:
```json
"C.Color.MoreMenu.XL.MoreButton.Unselected.Label.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled}" },
"C.Color.MoreMenu.XL.MoreButton.Unselected.Icon.Enabled": { "value": "{S.Color.Interaction.Neutral.Inverse.Primary.Icon.Enabled}" }
```

### 5.3 Structural changes via Figma Plugin API

After tokens are applied, use `use_figma` to set the SiteHeader variant fills:

```js
// Set SiteHeader Large/XL/XX-Large background to black
// and bind to the new Component token
const variants = ['8100:193331', '7950:19941', '8100:193509']; // node IDs
for (const id of variants) {
  const node = figma.getNodeById(id);
  node.fills = [{ type: 'SOLID', color: {r:0,g:0,b:0} }];
  node.setSharedPluginData('tokens', 'fill', '"C.Color.SiteHeader.Background.Wide"');
}
```

Node IDs are file-specific — find them by running a scan or using get_metadata.

### 5.4 Mega menu / flyout panels

For NavigationContainer panels (white bg for Level-2 content, brand-pink bg for hygiene links):

```js
// NavigationContainer-Level1 instances — white background
for (const node of level1Instances) {
  node.fills = [{ type: 'SOLID', color: {r:1,g:1,b:1} }];
  node.setSharedPluginData('tokens', 'fill', '"S.Color.Background.Default.Main"');
}

// NavigationContainer-Hygiene instances — light pink background
for (const node of hygieneInstances) {
  node.fills = [{ type: 'SOLID', color: {r:1,g:0.612,b:0.706} }]; // Primary.1
  node.setSharedPluginData('tokens', 'fill', '"S.Color.Background.Default.Emphasis"');
}
```

---

## Phase 6 — Footer

The footer always requires brand treatment — Ghost's default is light-surface; most clubs want a dark footer.

### 6.1 Footer token approach

The footer background, section titles, and link colours need to be updated. There are two approaches:

**Option A — Instance overrides (current practice):**
- Apply via Figma Plugin API directly on the Footers page
- Set token bindings to Inverse equivalents
- Fast, works immediately
- ⚠️ Caveat: Token Studio re-apply may reset these; re-run the script after each full apply

**Option B — Component token layer (recommended for future):**
- Add `C.Color.Footer.*` tokens to `tokens.json`
- Bind ComponentContainer and text nodes to these new tokens
- Token Studio will always preserve the values
- Requires more upfront token architecture work

For a new brand fork, use Option A to establish the visual direction quickly, then convert to Option B before shipping.

### 6.2 Applying the footer treatment (Option A)

Run the following via `use_figma`. Adapt hex values for the brand.

**1. Fix all footer sub-component master backgrounds to black:**

Master component IDs to fix (these are file-specific — scan the Footers page for COMPONENT_SET nodes):
- Footer-Branding
- Footer
- SponsorGrid-Tier1
- SponsorGrid-TierOther
- Footer-SponsorBlock
- Footer-AppPromo

For each:
```js
master.findAll(n => n.type === 'COMPONENT').forEach(v => {
  v.fills = [{ type: 'SOLID', color: {r:0,g:0,b:0} }];
  v.setSharedPluginData('tokens', 'fill', '"S.Color.Background.Inverse.Main"');
});
```

**2. Apply text colour overrides across the entire Footers page:**

```js
const footerPage = figma.root.children.find(p => p.id === '[FOOTERS_PAGE_ID]');
const allTexts = footerPage.findAll(n => n.type === 'TEXT');

const PINK_CHARS = new Set(['GROUP TITLE', 'Useful links', 'Find us', 'Follow us', 'Official app', 'Back to top', '{Title}', 'TIER 1', 'TIER OTHER']);
const PINK = {r:1, g:0.612, b:0.706}; // Primary.1
const WHITE = {r:1, g:1, b:1};

for (const t of allTexts) {
  const chars = (typeof t.characters === 'string') ? t.characters.trim() : '';
  const token = t.getSharedPluginData('tokens', 'fill') || '';
  
  if (PINK_CHARS.has(chars) || chars.startsWith('TIER')) {
    t.fills = [{ type: 'SOLID', color: PINK }];
    t.setSharedPluginData('tokens', 'fill', '"S.Color.Background.Default.Emphasis"');
  } else if (token.includes('Interaction.Neutral.Default.Primary.Label') || token.includes('TextButton.Default')) {
    t.fills = [{ type: 'SOLID', color: WHITE }];
    t.setSharedPluginData('tokens', 'fill', '"S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled"');
  } else if (token.includes('Text.Default')) {
    t.fills = [{ type: 'SOLID', color: WHITE }];
    t.setSharedPluginData('tokens', 'fill', '"S.Color.Text.Inverse.Main"');
  }
}
```

**3. Fix icon vectors (black → white):**

```js
const vectors = footerPage.findAll(n => n.type === 'VECTOR');
for (const v of vectors) {
  if (!v.fills || !Array.isArray(v.fills)) continue;
  const hasBlack = v.fills.some(f => f.type === 'SOLID' && f.color.r < 0.15 && f.color.g < 0.15 && f.color.b < 0.15);
  const hasPink = v.fills.some(f => f.type === 'SOLID' && f.color.r > 0.85 && f.color.g < 0.8);
  if (hasBlack && !hasPink) {
    v.fills = [{ type: 'SOLID', color: WHITE }];
    v.setSharedPluginData('tokens', 'fill', '"S.Color.Fill.Inverse.Main"');
  }
}
```

**4. Restore BackToTop pink** (it may have been overwritten by the background sweep):

```js
const backToTopNodes = footerPage.findAll(n => n.name && n.name.includes('BackToTop'));
for (const n of backToTopNodes) {
  const token = n.getSharedPluginData('tokens', 'fill') || '';
  if (token.includes('BackToTop.Background')) {
    n.fills = [{ type: 'SOLID', color: PINK }];
  }
}
```

### 6.3 Verify the footer

After running the scripts, screenshot the Footer XL and Small variants. Check:

- [ ] Full black background throughout
- [ ] Section titles (Find us, Useful links, GROUP TITLE, TIER labels) — brand pink
- [ ] All text links and body text — white on black
- [ ] Social icon vectors — white
- [ ] Club crest / brand vectors — preserved (do not change pink/brand colour vectors)
- [ ] BackToTop bar — brand Primary.1 background, black label
- [ ] SponsorGridItem boxes — light grey (intentional — creates separation on dark footer)
- [ ] Language picker trigger — white border outline on dark background (correct)

---

## Phase 7 — Logos, crests, and brand assets

### 7.1 Placing images in Figma

All raster assets (logos, crests, sponsor images) are placed using the Figma Plugin API. Follow this sequence exactly — skipping steps causes layout breakage at different component sizes.

```js
// 1. Create a Rectangle inside the component, sized to the component bounds
const rect = figma.createRectangle();
rect.resize(componentWidth, componentHeight);
rect.fills = []; // transparent fill — image will go here

// 2. Upload and place the image
await figma.uploadAsset(nodeId, imageBytes, { scaleMode: 'FIT' });

// 3. IMMEDIATELY set Scale constraints — do this in the same operation
rect.constraints = { horizontal: 'SCALE', vertical: 'SCALE' };
// Figma defaults to Left/Top — without Scale the image breaks when the component resizes

// 4. Take a screenshot to verify before moving on
```

**Why Scale constraints matter:** Figma defaults to Left/Top constraints on new rectangles. When the parent component is resized (e.g., displayed at different breakpoints or scales), a Left/Top image stays pinned to the corner instead of scaling with the container. This causes the crest/logo to overflow its bounds or leave empty space in smaller sizes.

### 7.2 Asset checklist per brand

- [ ] Club crest / primary logo (PNG, transparent background, high resolution)
- [ ] Secondary logo / wordmark (if separate from crest)
- [ ] Kit sponsor logo
- [ ] Front-of-shirt sponsor
- [ ] Sleeve sponsor(s)
- [ ] Kit manufacturer logo
- [ ] Global partner / shirt sponsor logos for footer Tier 1
- [ ] Other sponsor logos for footer Tier Other

---

## Phase 8 — Quality assurance

### 8.1 Re-run the colour matrix

```bash
python3 generate_colour_matrix.py colour-matrix.html
```

Review Section 2 with all fixes applied. Confirm:
- No unexpected ❌ failures in components that were passing before
- All documented DNPs match the brand fork doc (no undocumented failures)

### 8.2 Visual review checklist

Go through the Chrome and Footers pages in Figma and verify:

**Chrome page:**
- [ ] SiteHeader — correct background colour for each breakpoint
- [ ] SiteHeader — logo/crest placed correctly with Scale constraints
- [ ] Navigation XL — visible text (white on dark, or black on light) at all states
- [ ] Navigation flyout/mega menu — white panel with black text, hygiene panel with brand colour
- [ ] MoreMenu — correct panel colour, all items readable
- [ ] HygieneLinks — visible on SiteHeader bar
- [ ] IconButtons (search, basket, account) — visible on SiteHeader bar
- [ ] BackToTop — brand pink, correct hover/active states
- [ ] Tabs — brand-pink selected border visible on Default and Inverse surfaces
- [ ] PageNavigation — brand-pink selected border
- [ ] SubNavigation — brand-pink selected border

**Footers page:**
- [ ] Full footer XL — black background, pink titles, white text, white icons
- [ ] Full footer Small — same treatment at mobile size
- [ ] Sponsor grids — grey boxes on black background
- [ ] BackToTop strip — pink, full width

**ColourSets page:**
- [ ] Button Primary — visible and correctly coloured on each of the 10 surfaces
- [ ] Button Secondary — check for contrast issues
- [ ] Tab selected — pink border visible on all surfaces
- [ ] Text contrast — no black text on dark surfaces

### 8.3 Accessibility sign-off

All DNPs must be in the brand fork doc with:
- The ratio (e.g., 1.97:1)
- The component and property (e.g., CommonButton.Default.Primary.Container-Background on white)
- The decision (Accepted / Mitigated / Reject)
- The mitigation if accepted (e.g., "button label passes at 4.5:1 AA; shape visible in context")

---

## Phase 9 — Documentation

### 9.1 Update the brand fork doc

By end of Phase 8, the brand fork MD file should contain:

- [ ] Palette table with all hex values and WCAG notes
- [ ] Every Fix applied (A–Z as needed) with: Problem, Fix, Token changes, Cascades-to, Token debt notes
- [ ] Known Issues / DNPs section with ratio, component, and decision for each
- [ ] Next Steps section with outstanding work

### 9.2 Commit everything

```bash
git add tokens.json [BRAND]_BRAND_FORK.md
git commit -m "[Brand] — Phase 1–8 complete: palette, semantic fixes, SiteHeader, Navigation, Footer"
git push origin [brand-slug]
```

### 9.3 Final Tokens Studio pull and apply

Do a final pull and apply to all pages to confirm the committed `tokens.json` matches what's in Figma.

---

## Common mistakes and how to avoid them

| Mistake | Consequence | Prevention |
|---|---|---|
| Tokens Studio connected to `main` not the brand branch | Brand changes applied to Ghost baseline, overwrites main | Always check Settings → Sync → Branch before pulling |
| Applying token changes to all pages before footer treatment | Footer treatment gets overwritten by Default tokens | Apply tokens to all pages first, then run the footer script |
| Setting fills directly without updating token bindings | Next Tokens Studio apply overwrites the fill | Always call `setSharedPluginData('tokens', 'fill', ...)` after setting any fill |
| Changing Navigation.XL.Level-2 to Inverse | Level-2 appears in white flyout panels — Inverse makes text invisible | Level-2 and Level-3 always stay Default; only Level-1 is Inverse on dark headers |
| Not setting Scale constraints on image rectangles | Logo/crest breaks at different component sizes | Set constraints immediately after upload — never as a separate step |
| Running the colour matrix before committing token changes | Matrix runs against old values | Always commit and pull into Tokens Studio before running the matrix |
| Accepting a DNP without documenting it | Accessibility debt is invisible | Document every DNP in the brand fork MD before marking a phase complete |

---

## Appendix — Key token reference

### Semantic tokens most likely to change per brand

```
S.Color.Border.Default.Emphasis            Selected borders → Primary.3
S.Color.Border.Inverse.Emphasis            Selected borders on dark surfaces → Primary.3
S.Color.Background.Default.Emphasis        Light accent bg → Primary.1
S.Color.Interaction.Inverse.Primary.*      Buttons on dark surfaces → Primary.3
```

### Component tokens added in Inter Miami (add to any brand using dark SiteHeader)

```
C.Color.SiteHeader.Background.Wide         Black header at Large/XL/XX-Large
C.Color.SiteHeader.Background.Narrow       White header at Small/Medium
C.Color.MoreMenu.Panel-Background          Light pink MoreMenu overlay
C.Color.MoreMenu.XL.MoreButton.Unselected.Label.*   White MoreButton on dark header
C.Color.MoreMenu.XL.MoreButton.Unselected.Icon.*    White MoreButton icon
C.Color.Navigation.XL.Level-1.Label.*     White nav links on dark header
C.Color.Navigation.XL.Level-1.Icon.*      White nav icons on dark header
C.Color.HygieneLinks.XL.Label.*           White hygiene links on dark header
C.Color.HygieneLinks.XL.Icon.*            White hygiene icons on dark header
```

### BackToTop tokens

```
C.Color.BackToTop.Background.Enabled   → {S.Color.Background.Default.Emphasis}  (Primary.1)
C.Color.BackToTop.Background.Hover     → {P.Color.Primary.2}
C.Color.BackToTop.Background.Active    → {P.Color.Primary.3}
C.Color.BackToTop.Label.Enabled        → Black (verify contrast on Primary.1)
C.Color.BackToTop.Icon.Enabled         → Black
```

### Footer text token mapping

| Content type | Token to apply |
|---|---|
| Section headers (Find us, GROUP TITLE, etc.) | `S.Color.Background.Default.Emphasis` |
| Text links in footer | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` |
| Body text, addresses, copyright | `S.Color.Text.Inverse.Main` |
| Icon vectors on dark footer | `S.Color.Fill.Inverse.Main` |
| Footer background frames | `S.Color.Background.Inverse.Main` |
