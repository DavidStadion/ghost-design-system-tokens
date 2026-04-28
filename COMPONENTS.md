# Ghost Design System — Component Catalog

This document describes every component in the Ghost Design System: its purpose, Figma structure, token bindings, variant properties, and brand fork considerations. Use this to understand which tokens control which visual properties, and to know what to check when building or verifying a brand fork.

All token paths refer to the Component layer (`C.Color.*`) unless prefixed otherwise.

---

## How to read this document

Each component entry covers:

- **Purpose** — what the component does and where it's used
- **Figma structure** — component type (flat / standard), how it's nested
- **Variant properties** — the Figma variant axes (Breakpoint, State, ColourWay, etc.)
- **Token bindings** — which C.Color tokens control which visual parts
- **Brand fork notes** — what typically changes per brand, what to check

**Component types:**

- **Standard** — Has a ComponentContainer with explicit fills; uses the full Component token stack
- **Flat** — Resolves directly from Semantic tokens; no independent background fill; inherits surface colour from parent

---

## Navigation components

### SiteHeader

**Purpose:** The full-width top bar of the site. Contains the club logo, primary navigation, utility icons (search, basket, account), and the MoreButton that opens the MoreMenu on mobile.

**Figma structure:** COMPONENT_SET with variants for Breakpoint (Small, Medium, Large, X-Large, XX-Large). Small and Medium show a simplified bar with MoreButton; Large+ show the full navigation.

**Variant properties:**
- `Breakpoint` — Small | Medium | Large | X-Large | XX-Large

**Token bindings:**

| Part | Token | Notes |
|---|---|---|
| Background (Large+) | `C.Color.SiteHeader.Background.Wide` | Added for Inter Miami — resolves to Black on dark-header brands |
| Background (Small, Medium) | `C.Color.SiteHeader.Background.Narrow` | Resolves to White (MoreMenu handles mobile context) |

> **Token debt (Ghost core):** Ghost core has no SiteHeader.Background token. `Wide` and `Narrow` were added in the Inter Miami fork. If applying to a new brand, these tokens must be in the Component layer of `tokens.json`.

**Brand fork notes:**
- Light-header brands: `Wide` → `{S.Color.Background.Default.Main}` (white)
- Dark-header brands: `Wide` → `{P.Color.Neutral.Black}` or `{P.Color.Secondary.1}`
- Navigation links inside SiteHeader must use Inverse tokens on dark headers (see Navigation component)

---

### Navigation

**Purpose:** Primary navigation links in the SiteHeader. Renders at two sizes: `Small` (inside MoreMenu overlay on mobile) and `XL` (horizontal bar on desktop).

**Figma structure:** Flat — inherits surface from its parent (SiteHeader or MoreMenu).

**Variant properties:**
- `Size` — Small | XL
- `Level` — 1 | 2 | 3 (hierarchy depth in mega/flyout menus)
- `State` — Enabled | Hover | Active | Selected

**Token bindings:**

| Part | Token | Notes |
|---|---|---|
| XL Level-1 Label (all states) | `C.Color.Navigation.XL.Level-1.Label.*` | Top bar links — Inverse on dark headers |
| XL Level-1 Icon (all states) | `C.Color.Navigation.XL.Level-1.Icon.*` | Chevrons, indicators |
| XL Level-1 Background Hover | `C.Color.Navigation.XL.Level-1.Background.Hover` | Hover fill behind nav item |
| XL Level-1 Background Active | `C.Color.Navigation.XL.Level-1.Background.Active` | |
| XL Level-2 Label (all states) | `C.Color.Navigation.XL.Level-2.Label.*` | Flyout/mega menu items — Default (white bg) |
| XL Level-3 Label (all states) | `C.Color.Navigation.XL.Level-3.Label.*` | Sub-items in flyout |
| Small Level-1/2/3 Label | `S.Color.Interaction.Neutral.Default.Primary.Label.*` | Mobile MoreMenu — Default (pink panel bg) |
| Selected indicator border | `S.Color.Fill.Default.Emphasis` | Miami Pink — visible on both surfaces |

**Brand fork notes:**
- The key decision per brand is: **is the SiteHeader dark or light?**
  - Dark header → Level-1 uses `Interaction.Neutral.Inverse.Primary.*` (white text)
  - Light header → Level-1 uses `Interaction.Neutral.Default.Primary.*` (black text)
- Level-2 and Level-3 are always in flyout panels (white background) → always Default tokens
- Small size is always in the MoreMenu panel (light pink or white background) → always Default tokens

---

### MoreMenu

**Purpose:** The slide-in or overlay menu that appears on Small/Medium breakpoints. Contains all navigation links, hygiene links, utility icons, social links, and a close button.

**Figma structure:** Standard. Has a panel background that's brand-specific.

**Variant properties:**
- `State` — Closed | Open
- `Breakpoint` — Small | Medium

**Token bindings:**

| Part | Token | Notes |
|---|---|---|
| Panel background | `C.Color.MoreMenu.Panel-Background` | Added for Inter Miami — light pink (`{S.Color.Background.Default.Emphasis}`) |
| MoreButton Label (XL, Unselected) | `C.Color.MoreMenu.XL.MoreButton.Unselected.Label.*` | White on dark SiteHeader |
| MoreButton Icon (XL, Unselected) | `C.Color.MoreMenu.XL.MoreButton.Unselected.Icon.*` | White on dark SiteHeader |
| Nav item backgrounds | `S.Color.Background.HoldingColour.FullyTransparent` | Transparent — shows panel colour |
| Nav item labels | Inherit from Navigation.Small | Default (black on pink panel) |
| Section headers | Direct fill (token debt — see notes) | Transparent background |
| Dividers | Direct fill — `P.Color.Opacity.Default.10` (10% black) | Subtle separator on light panel |
| Close button | Direct fill (token debt) | Dark fill, visible on pink |

> **Token debt:** MoreMenu section header backgrounds, dividers, and close button are not tokenised in Ghost core. Currently direct fills for Inter Miami. For future brands: add `C.Color.MoreMenu.SectionHeader.Background`, `C.Color.MoreMenu.Divider`, `C.Color.MoreMenu.CloseButton.*`.

**Brand fork notes:**
- `Panel-Background` is the primary brand decision for MoreMenu — light pink for Inter Miami
- The panel colour determines whether Navigation.Small uses Default or Inverse tokens — always verify contrast
- MoreButton (on the dark SiteHeader bar) needs Inverse tokens for its label/icon

---

### GlobalNav

**Purpose:** The very top utility bar, typically containing account links, language picker, and sponsor/partner links. Sits above the SiteHeader on some layouts.

**Figma structure:** Flat — GlobalLink variant. Resolves from Semantic tokens.

**Variant properties:**
- `Variant` — GlobalLink
- `State` — Enabled | Hover | Active

**Token bindings:** Resolves directly from `S.Color.Interaction.Neutral.Default.Primary.*` (black on light surface).

**Brand fork notes:** GlobalNav rarely needs brand-specific changes unless the top bar has a coloured background.

---

### SubNavigation

**Purpose:** In-page section navigation — a row of tabs or pills used to switch between content sections within a page (e.g., Squad | Fixtures | Results).

**Figma structure:** Standard. Uses same selected-border token as Tab and PageNavigation.

**Variant properties:**
- `State` — Enabled | Hover | Active | Selected
- `ColourWay` / ColourSet surface

**Token bindings:**

| Part | Token |
|---|---|
| Selected border | `S.Color.Border.Default.Emphasis` → `{P.Color.Primary.3}` |
| Label (Default surface) | `S.Color.Interaction.Neutral.Default.Primary.Label.*` |
| Label (Inverse surface) | `S.Color.Interaction.Neutral.Inverse.Primary.Label.*` |

**Brand fork notes:** Selected border is controlled by Fix A in the brand fork — `S.Color.Border.Default.Emphasis` → Primary.3.

---

### HygieneLinks

**Purpose:** Secondary utility navigation — links like "Shop", "Tickets", "Foundation" that appear in the SiteHeader or GlobalNav.

**Figma structure:** Flat.

**Variant properties:**
- `Size` — Small (mobile/MoreMenu) | XL (desktop SiteHeader)
- `State` — Enabled | Hover | Active

**Token bindings:**

| Part | Token |
|---|---|
| XL Label (all states) | `C.Color.HygieneLinks.XL.Label.*` | Inverse on dark SiteHeader |
| XL Icon (all states) | `C.Color.HygieneLinks.XL.Icon.*` | Inverse on dark SiteHeader |
| Small Label | `S.Color.Interaction.Neutral.Default.Primary.Label.*` | Default in MoreMenu |

**Brand fork notes:** XL variant needs Inverse tokens when SiteHeader is dark (same logic as Navigation.XL.Level-1).

---

### PageNavigation

**Purpose:** Pagination/section navigation at the top of content pages — e.g., "Home / News / Match Report". Shows current context and allows jumping between sections.

**Figma structure:** Standard + ColourSet override (PageNavigation set in ColourSet layer).

**Token bindings:**

| Part | Token |
|---|---|
| Selected border | Cascades from `S.Color.Border.Default.Emphasis` |
| Label | `S.Color.Interaction.Neutral.Default.Primary.Label.*` / Inverse |
| Background | Surface-context resolved |

---

### Tab

**Purpose:** Tab bar for switching between views — e.g., Squad tabs (Men | Women | Academy).

**Figma structure:** Standard + ColourSet override (Tab set in ColourSet layer).

**Variant properties:**
- `State` — Enabled | Hover | Selected
- `ColourSet` — overridden per surface via ColourSet.Tab.*

**Token bindings:**

| Part | Token |
|---|---|
| Selected border | Cascades from `S.Color.Border.Default.Emphasis` → Primary.3 |
| Label | Interaction.Neutral.Default or Inverse depending on surface |

---

### LanguagePicker-Trigger

**Purpose:** Dropdown trigger that shows the current language and opens the language selector.

**Figma structure:** Flat. A styled button with a border outline.

**Token bindings:** Resolves from `S.Color.Interaction.Neutral.*` tokens. On dark surfaces (footer) needs Inverse variants applied.

---

## Button components

### CommonButton

**Purpose:** The primary call-to-action button. Used for key actions like "Buy Tickets", "Watch Now", "Sign Up".

**Figma structure:** Standard. Has ComponentContainer with filled background.

**Variant properties:**
- `Variant` — Primary | Secondary | Ghost | Destructive
- `Size` — Small | Medium | Large
- `State` — Enabled | Hover | Active | Disabled
- `ColourWay` — resolved via ColourSet surface

**Token bindings:**

| Part | Token |
|---|---|
| Primary container (Default surface) | `C.Color.CommonButton.Container-Background.Enabled` → `{S.Color.Interaction.Default.Primary.Container-Background.Enabled}` → `{P.Color.Primary.1}` |
| Primary container (Inverse surface) | `S.Color.Interaction.Inverse.Primary.Container-Background.*` → `{P.Color.Primary.3}` |
| Primary container Hover | `S.Color.Interaction.Inverse.Primary.Container-Background.Hover` → `{P.Color.Shades.Primary-1.700}` |
| Primary container Active | → `{P.Color.Shades.Primary-1.800}` |
| Label (Default) | `S.Color.Interaction.Default.Primary.Label.*` → Black |
| Label (Inverse) | `S.Color.Interaction.Inverse.Primary.Label.*` → `{S.Color.Text.Default.Main}` (Black on pink) |
| Icon | Mirrors Label token |

**Brand fork notes:**
- Default surface Primary button uses Primary.1 (pastel pink for Inter Miami) — this is a DNP at 1.97:1 vs white bg but accepted as brand tradeoff
- Inverse surface Primary button uses Primary.3 (Miami Pink) — passes at 4.57:1 on dark backgrounds
- ColourSet.Button.* entries override these per surface — always regenerate the colour matrix after changing

---

### IconButton

**Purpose:** A square button showing only an icon — used for search, basket, account, share actions.

**Figma structure:** Standard.

**Variant properties:**
- `Variant` — Primary | Secondary | Ghost
- `Size` — Small | Medium | Large
- `State` — Enabled | Hover | Active | Disabled
- `ColourWay` — used to switch between Default/Inverse rendering

**Token bindings:** Mirrors CommonButton structure but without a Label token; uses Icon tokens only.

**Brand fork notes:** On dark SiteHeader, IconButton ColourWay must render white icons. If the component's `componentProperties` API is unavailable for switching ColourWay, scan for black VECTOR fills within the instance and set to `S.Color.Fill.Inverse.Main`.

---

### TextButton

**Purpose:** A text-only link styled as a button with an optional arrow or icon. Used in footers, address panels, and content sections.

**Figma structure:** Flat (text + optional icon, no background fill).

**Variant properties:**
- `Variant` — Default | Inverse
- `Size` — Small | Medium
- `State` — Enabled | Hover | Active | Disabled

**Token bindings:**

| Part | Token |
|---|---|
| Label (Default) | `C.Color.TextButton.Default.Label.Enabled` → `S.Color.Interaction.Neutral.Default.Primary.Label.Enabled` |
| Label (Inverse) | `C.Color.TextButton.Inverse.Label.Enabled` → `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` |

**Brand fork notes:** In the footer (dark surface), TextButton labels need `C.Color.TextButton.Inverse.Label.Enabled` or a direct fill update to `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled`.

---

### ActionButton

**Purpose:** A secondary interactive button — used for secondary CTAs, breadcrumb actions, filter triggers.

**Figma structure:** Standard. Similar to CommonButton.

**Variant properties:** Variant, Size, State, ColourWay.

**Token bindings:** References `S.Color.Interaction.Default.Secondary.*` and Inverse equivalents.

---

### BackButton

**Purpose:** A back/return navigation button.

**Figma structure:** Standard. Often uses a left-arrow icon.

**Token bindings:** References `S.Color.Interaction.Neutral.Default.Primary.*`.

---

### SocialButton

**Purpose:** Icon buttons for social platforms (Facebook, X/Twitter, Instagram, YouTube, TikTok, etc.).

**Figma structure:** Standard. Icon-only circular or rounded button.

**Variant properties:**
- `Platform` — Facebook | X | Instagram | YouTube | TikTok | etc.
- `State` — Enabled | Hover

**Token bindings:** Platform-specific fills for icon; container uses brand or neutral background.

---

### ShareButton

**Purpose:** Share this page/content button — often triggers a share sheet or copies a URL.

**Figma structure:** Standard. Similar to SocialButton.

**Token bindings:** References `S.Color.Interaction.Neutral.Default.Primary.*`.

---

## Navigation overlay components

### MoreButton

**Purpose:** The hamburger/menu button that opens the MoreMenu. Shown on Small/Medium breakpoints in the SiteHeader.

**Figma structure:** Part of the SiteHeader component. Not a standalone component in the library.

**Token bindings:**

| Part | Token |
|---|---|
| Label/text (XL, dark header) | `C.Color.MoreMenu.XL.MoreButton.Unselected.Label.*` → Inverse |
| Icon (XL, dark header) | `C.Color.MoreMenu.XL.MoreButton.Unselected.Icon.*` → Inverse |

---

### MyAccount-DropDown-Trigger

**Purpose:** The "My Account" or avatar button that opens the account dropdown.

**Figma structure:** Flat trigger button.

**Variant properties:**
- `State` — Default | Open

**Token bindings:** References `S.Color.Interaction.Neutral.Default.Primary.*` for label/icon.

> **Token debt:** The DropDown panel background (white surface that appears when State=Open) is not tokenised. Applied via direct fill in Inter Miami fork.

---

### SSOLink

**Purpose:** Single Sign-On login link — "Sign in / Register" text link.

**Figma structure:** Flat.

**Token bindings:** References `S.Color.Interaction.Neutral.Default.Primary.*`.

---

## Content components

### Link

**Purpose:** Inline hypertext link within body copy or lists.

**Figma structure:** Flat — Semantic reference only.

**Token bindings:** `S.Color.Interaction.Neutral.Default.Primary.Label.Enabled` (underline style).

---

### Tag

**Purpose:** Category or status label — e.g., "LIVE", "BREAKING", "EXCLUSIVE". Small pill-shaped label.

**Figma structure:** Standard.

**Variant properties:** Variant (Primary | Secondary | Live | etc.), Size, State.

**Token bindings:** Container-Background, Label colour from Interaction or Text tokens.

---

### Chip

**Purpose:** Filter chip or selectable tag — used in filter bars and search facets.

**Figma structure:** Standard.

**Variant properties:** State (Enabled | Selected | Disabled), Size.

**Token bindings:** Same structure as CommonButton but smaller; Selected state uses Primary.3 fill or border.

---

### SegmentedControl

**Purpose:** A group of mutually exclusive options — e.g., switching between a list and grid view.

**Figma structure:** Standard. Group of Chip-like segments in a shared container.

**Token bindings:** Active segment uses `S.Color.Background.Default.Emphasis`; inactive uses transparent or subtle.

---

### CategoryLink

**Purpose:** A labelled link with an optional image or icon — used in category navigation grids (e.g., News | Fixtures | Shop sections).

**Figma structure:** Standard.

**Token bindings:** Label, background, border from Semantic/Interaction tokens.

---

### Card

**Purpose:** Content card — the primary unit for news articles, match listings, player profiles, products. Typically has an image area, title, metadata, and a CTA.

**Figma structure:** Standard. Variants for content type (News, Match, Player, etc.) and size.

**Variant properties:** Type, Size, State (Enabled | Hover).

**Token bindings:**
- Card background: `S.Color.Background.Default.Main`
- Title: `S.Color.Text.Default.Main`
- Supporting text: `S.Color.Text.Default.Supporting`
- Hover overlay: `S.Color.Background.Default.Subtle`
- Border (if present): `S.Color.Border.Default.Subtle`

---

### Dropdown

**Purpose:** Select menu — used in forms and filter controls.

**Figma structure:** Standard. Has a trigger and a panel.

**Token bindings:**
- Trigger background: `S.Color.Background.Default.Main`
- Trigger border: `S.Color.Border.Default.Main`
- Panel background: `S.Color.Background.Default.Main`
- Option hover: `S.Color.Background.Default.Subtle`
- Selected option: `S.Color.Background.Default.Emphasis`

---

## Form components

### Form / InputField

**Purpose:** Text input field — used in search, login, registration, contact forms.

**Figma structure:** Standard (sub-component wrapper). Contains Label, Input, HelperText sub-components.

**Variant properties:** State (Default | Focus | Error | Disabled | Filled), Size.

**Token bindings:**

| Part | Token |
|---|---|
| Input background | `S.Color.Background.Default.Main` |
| Input border (Default) | `S.Color.Border.Default.Main` |
| Input border (Focus) | `S.Color.Border.Default.Emphasis` → Primary.3 |
| Input border (Error) | `S.Color.Border.Destructive.*` |
| Label text | `S.Color.Text.Default.Main` |
| Placeholder text | `S.Color.Text.Default.Supporting` |
| Helper/error text | `S.Color.Text.Default.Supporting` / Destructive |
| Focus ring | `S.Color.Interaction.Default.Primary.Border.Focus` |

---

### Pagination

**Purpose:** Page navigation controls for content lists — Previous | 1 | 2 | 3 | Next.

**Figma structure:** Standard.

**Variant properties:** State (Enabled | Hover | Selected | Disabled).

**Token bindings:**
- Selected page: `S.Color.Interaction.Default.Primary.Container-Background.Selected` → Primary.1
- Selected label: `S.Color.Interaction.Default.Primary.Label.Selected`
- Other pages: `S.Color.Interaction.Neutral.Default.Primary.*`

---

## Footer components

The footer is composed of several independent sub-components that are assembled into the `Footer` component set.

### Footer

**Purpose:** The complete footer assembly. Contains branding, navigation columns, sponsor grids, social links, app promo, legal links, and language picker. The primary component placed at the bottom of all pages.

**Figma structure:** COMPONENT_SET with Breakpoint variants (Small, X-Large). Assembles all footer sub-components.

**Variant properties:**
- `Breakpoint` — Small | X-Large

**Token bindings (background):**

| Part | Token | Inter Miami value |
|---|---|---|
| ComponentContainer background | `S.Color.Background.Inverse.Main` | Black |

**Brand fork notes:**
- The footer typically uses `S.Color.Background.Inverse.Main` (black) as its background for Inter Miami
- Sub-component text bindings must use Inverse tokens on the dark footer (see Fix I in INTER_MIAMI_BRAND_FORK.md)
- Section/column title text uses `S.Color.Background.Default.Emphasis` (light pink) as a colour-borrow pattern — the semantic meaning is slightly mismatched but functionally correct
- ⚠️ Token Studio caveat: footer text overrides are applied at the instance level; a full Token Studio apply may require re-running the footer treatment

---

### Footer-Branding

**Purpose:** The top section of the footer containing the club logo, crest, brand mark, and optionally a tagline or social icons row.

**Figma structure:** COMPONENT_SET — Small | X-Large variants.

**Token bindings:**

| Part | Token | Notes |
|---|---|---|
| Background | `S.Color.Background.Inverse.Main` | Black |
| Social icon vectors | `S.Color.Fill.Inverse.Main` | White |
| Club crest/logo vectors | Brand-specific pink vectors — preserved as-is | |
| Bottom stroke/border | `S.Color.Border.Default.Emphasis` → Primary.3 | Pink underline under logo |

---

### Footer-UsefulLinks

**Purpose:** The main navigation column area of the footer — multiple columns of grouped links with section headers.

**Figma structure:** COMPONENT_SET. Contains UsefulLinks-ListGroup sub-components.

**Sub-components:**
- `UsefulLinks-ListGroup` — A single column with a GROUP TITLE header and list of links
- `LinkList-Item` — An individual text link with optional arrow icon
- `LinkList` — A group of LinkList-Items

**Token bindings (per brand fork — instance overrides):**

| Part | Token |
|---|---|
| "Useful links" heading | `S.Color.Background.Default.Emphasis` (pink) |
| GROUP TITLE | `S.Color.Background.Default.Emphasis` (pink) |
| Text link | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` (white) |
| Background | `S.Color.Background.Inverse.Main` (black) |

---

### Footer-AddressPanel

**Purpose:** Contact details section — club address, telephone, email, with TextButton links for directions/contact.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Sub-components:**
- `ContactBlock` — A titled group with address and links
- `ContactDetails` — Individual contact detail (address, phone, email)
- `TextButton-Master` — The "LABEL" link within each contact detail

**Token bindings (per brand fork):**

| Part | Token |
|---|---|
| "Find us" section title | `S.Color.Background.Default.Emphasis` (pink) |
| {Title} column header | `S.Color.Background.Default.Emphasis` (pink) |
| Address body text | `S.Color.Text.Inverse.Main` (white) |
| LABEL TextButton links | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` (white) |
| Background | `S.Color.Background.Inverse.Main` (black) |

---

### Footer-SocialPanel

**Purpose:** Social media follow section — "Follow us" heading with a row of social platform icons.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Token bindings:**

| Part | Token |
|---|---|
| "Follow us" heading | `S.Color.Background.Default.Emphasis` (pink) |
| "Summary text" | `S.Color.Text.Inverse.Main` (white) |
| Social icon vectors | `S.Color.Fill.Inverse.Main` (white) |
| Background | `S.Color.Background.Inverse.Main` (black) |

---

### Footer-AppPromo

**Purpose:** App download promotion — "Official app" heading with app store badge buttons.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Token bindings:**

| Part | Token |
|---|---|
| "Official app" heading | `S.Color.Background.Default.Emphasis` (pink) |
| Summary text | `S.Color.Text.Inverse.Main` (white) |
| App store button images | Direct image fills — not tokenised |
| Background | `S.Color.Background.Inverse.Main` (black) |

---

### SponsorGrid-Tier1

**Purpose:** Grid of Tier 1 sponsor logos. "TIER 1" label with a row/grid of sponsor logo boxes.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Token bindings:**

| Part | Token |
|---|---|
| "TIER 1" label | `S.Color.Background.Default.Emphasis` (pink) |
| Sponsor item background | `C.Color.Footer-Sponsor.Background.Enabled` → `{S.Color.Background.Default.Subtle}` (#e9ecef grey) |
| Section background | `S.Color.Background.Inverse.Main` (black) |
| Border separators | `S.Color.Border.Inverse.Subtle` (white at 15% opacity) |

**Brand fork notes:** Sponsor item backgrounds remain grey on a dark footer — the contrast of a light logo box against a black footer creates visual separation.

---

### SponsorGrid-TierOther

**Purpose:** Grid of additional sponsor tiers (Tier 2, Tier 3 etc.) with smaller logo boxes.

**Figma structure:** COMPONENT_SET — Small | X-Large. Similar to Tier1 but smaller grid items.

**Token bindings:** Same pattern as SponsorGrid-Tier1 with "TIER OTHER" label.

---

### Footer-SponsorBlock

**Purpose:** Container that assembles SponsorGrid-Tier1 and SponsorGrid-TierOther into a single sponsor section.

**Figma structure:** COMPONENT_SET containing instances of the two SponsorGrid components.

---

### Footer-BackToTop-Master

**Purpose:** The "Back to top" action. A full-width pink button/bar at the bottom of the footer.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Token bindings:**

| Part | Token | Inter Miami value |
|---|---|---|
| Background Enabled | `C.Color.BackToTop.Background.Enabled` | `{S.Color.Background.Default.Emphasis}` → `#FF9CB4` |
| Background Hover | `C.Color.BackToTop.Background.Hover` | `{P.Color.Primary.2}` → `#FF6B8E` |
| Background Active | `C.Color.BackToTop.Background.Active` | `{P.Color.Primary.3}` → `#E8004B` |
| Label | `C.Color.BackToTop.Label.Enabled` | Black |
| Icon | `C.Color.BackToTop.Icon.Enabled` | Black |

**Brand fork notes:** BackToTop is a high-visibility brand element. The Enabled/Hover/Active colour ramp should use the brand's Primary.1 / Primary.2 / Primary.3 palette.

---

### Footer-LegalLinks

**Purpose:** The bottom-most footer row — legal disclaimers, privacy policy, terms links, and copyright statement.

**Figma structure:** COMPONENT_SET — Small | X-Large.

**Sub-components:**
- `HygieneLink` instances for each legal link
- Copyright text node

**Token bindings:**

| Part | Token |
|---|---|
| "Text link" legal links | `S.Color.Interaction.Neutral.Inverse.Primary.Label.Enabled` (white) |
| "© Copyright statement" | `S.Color.Text.Inverse.Main` (white) |
| Background | `S.Color.Background.Inverse.Main` (black) |

---

## Indicator / label components

### BackToTop

**Purpose:** The outer wrapper component that places Footer-BackToTop-Master instances in their stateful variants (Enabled | Hover | Active).

**Figma structure:** COMPONENT_SET containing INSTANCE children.

---

## Mega menu / flyout components

### NavigationContainer-Level1

**Purpose:** The white panel background of the mega menu / flyout that opens when a top-level navigation item is clicked.

**Figma structure:** FRAME or INSTANCE used as a panel wrapper.

**Token bindings:**

| Part | Token | Inter Miami value |
|---|---|---|
| Background | `S.Color.Background.Default.Main` | White |
| Navigation Level-2 items | Default tokens | Black text on white |

---

### NavigationContainer-Hygiene

**Purpose:** The panel section within the mega/flyout menu that holds hygiene/utility links (Shop, Tickets, etc.).

**Figma structure:** FRAME or INSTANCE used as a sub-panel.

**Token bindings:**

| Part | Token | Inter Miami value |
|---|---|---|
| Background | `S.Color.Background.Default.Emphasis` | `#FF9CB4` (light pink) |
| Navigation items | Default tokens | Black text on pink |

---

## Reference: token-to-component matrix

This table shows which semantic tokens cascade to which components. Use it when changing a Semantic token to predict the blast radius.

| Semantic token changed | Components affected |
|---|---|
| `S.Color.Border.Default.Emphasis` | Tab (selected), PageNavigation (selected), SubNavigation (selected) |
| `S.Color.Border.Inverse.Emphasis` | All above, on Inverse/dark surfaces |
| `S.Color.Interaction.Inverse.Primary.Container-Background.*` | CommonButton (Inverse variant), ColourSet CS-4/5/6 buttons |
| `S.Color.Background.Default.Emphasis` | BackToTop bg, MoreMenu panel bg, NavigationContainer-Hygiene bg, Footer section titles |
| `S.Color.Background.Inverse.Main` | Footer background, SiteHeader (via SiteHeader.Background.Wide), all Inverse-context containers |
| `S.Color.Interaction.Neutral.Inverse.Primary.Label.*` | Navigation.XL.Level-1, HygieneLinks.XL, Footer text links, MoreButton |
| `S.Color.Fill.Inverse.Main` | Social icon vectors, Footer-Branding icons, IconButton on dark surfaces |

---

## Reference: adding a new Component token

When a Figma property is not tokenised in Ghost core (e.g., you need to control a new visual property per-brand):

1. Add the token to `tokens.json` under `Component.C.Color.[ComponentName].[Property]`:
```json
"C.Color.SiteHeader.Background.Wide": {
  "value": "{P.Color.Neutral.Black}",
  "type": "color"
}
```

2. In Figma, set the node's fill to the correct colour value AND update the token binding:
```js
node.fills = [{ type: 'SOLID', color: {r:0, g:0, b:0} }];
node.setSharedPluginData('tokens', 'fill', JSON.stringify('C.Color.SiteHeader.Background.Wide'));
```

3. Commit and push `tokens.json`, then pull in Tokens Studio.

4. Document the new token in the brand fork MD file under Token debt resolved.
