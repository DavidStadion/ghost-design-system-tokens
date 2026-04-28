# Ghost Design System — Token Repository

This repository holds all design tokens for the Ghost Design System and its brand forks. Tokens are managed via [Tokens Studio for Figma](https://tokens.studio/) and stored as a single JSON file (`tokens.json`) versioned by branch.

---

## What this repository does

Every colour, spacing, radius, and typography value in the Ghost design system flows through this file. When a token value changes here and is pulled into Figma via Tokens Studio, every component that references that token updates automatically. No manual layer selection, no hunting through components.

**One source of truth. One file. One pull.**

---

## Repository structure

```
ghost-design-system-tokens/
├── tokens.json                  # All token layers for the active brand
├── README.md                    # This file — repo overview and setup
├── GHOST_DESIGN_SYSTEM.md       # Token architecture: layers, naming, ColourSets
├── COMPONENTS.md                # Component catalog: what each component is, tokens it uses
├── BRAND_FORK_GUIDE.md          # How to fork Ghost for a new brand (step-by-step)
├── INTER_MIAMI_BRAND_FORK.md    # Inter Miami CF brand-specific changes and decisions
└── generate_colour_matrix.py    # Accessibility audit script (see below)
```

---

## Branches

| Branch | Purpose |
|---|---|
| `main` | Ghost Design System baseline — no brand customisation |
| `inter-miami` | Inter Miami CF brand fork — active development |

Each new brand gets its own branch forked from `main`. Token values on `main` are never edited directly for brand work — always branch.

---

## How tokens flow into Figma

```
tokens.json (this repo)
      │
      │  git push
      ▼
GitHub (inter-miami branch)
      │
      │  Tokens Studio "Pull" 
      ▼
Figma file — token values updated on all bound nodes
```

**Tokens Studio settings (must be correct before every session):**

1. Open the Tokens Studio panel in Figma
2. Go to **Settings → Sync → GitHub**
3. Confirm:
   - **Repository:** `DavidStadion/ghost-design-system-tokens`
   - **Branch:** `inter-miami` (or the correct brand branch — never `main` for brand work)
   - **File path:** `tokens.json`
4. Click **Pull** to sync the latest token values into Figma
5. Click **Apply to…** and choose the pages to update

> ⚠️ **Always verify the branch field before pulling.** Pulling from `main` overwrites brand customisations with Ghost defaults.

---

## Two-channel rule

There are exactly two ways to change how Figma looks. Use the right channel for each type of change:

| Change type | Correct channel |
|---|---|
| Colour, radius, typography values | `tokens.json` → git push → Tokens Studio pull |
| Layout, spacing, corner radius on a specific node, variant properties, image fills | Figma Plugin API (`use_figma` MCP tool) |

**Never** edit token-bound properties by manually selecting layers in Figma. Those changes are overwritten on the next Tokens Studio apply.

---

## Colour accessibility matrix

The repo includes a Python script that generates a full WCAG contrast audit across all primitive colours and all components.

```bash
# Regenerate the matrix (run from repo root)
python3 generate_colour_matrix.py colour-matrix.html

# Serve locally for review
npx serve -l 3456 .
# → open http://localhost:3456/colour-matrix.html
```

**Section 1** — Every primitive colour as text on every primitive colour as background.  
**Section 2** — All 28 components × 10 surfaces, with WCAG 1.4.3 (text, 4.5:1) and 1.4.11 (UI, 3:1) results.

Regenerate the matrix every time primitives or semantic tokens change. No token value should enter the system without passing this audit.

---

## Key documents

| Document | Read when |
|---|---|
| [GHOST_DESIGN_SYSTEM.md](GHOST_DESIGN_SYSTEM.md) | You want to understand the token architecture before making any changes |
| [COMPONENTS.md](COMPONENTS.md) | You need to know which tokens control a specific component property |
| [BRAND_FORK_GUIDE.md](BRAND_FORK_GUIDE.md) | You are starting a new brand fork |
| [INTER_MIAMI_BRAND_FORK.md](INTER_MIAMI_BRAND_FORK.md) | You are working on the Inter Miami CF fork |

---

## Quick-start: editing token values

```bash
# 1. Clone the repo
git clone https://github.com/DavidStadion/ghost-design-system-tokens.git
cd ghost-design-system-tokens

# 2. Check out the brand branch
git checkout inter-miami

# 3. Edit tokens.json (use your editor or a script)
#    Token paths use dot notation in the file — see GHOST_DESIGN_SYSTEM.md

# 4. Commit and push
git add tokens.json
git commit -m "Inter Miami — [describe change]"
git push origin inter-miami

# 5. In Figma, open Tokens Studio → Pull → Apply to pages
```

---

## Quick-start: new brand fork

See [BRAND_FORK_GUIDE.md](BRAND_FORK_GUIDE.md) for the full walkthrough. The short version:

```bash
git checkout main
git checkout -b new-brand-name
# Edit Primitive.P.Color.* in tokens.json
# Run the colour matrix
# Work through BRAND_FORK_GUIDE.md checklist
```
