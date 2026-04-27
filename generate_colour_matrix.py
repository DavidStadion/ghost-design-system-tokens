#!/usr/bin/env python3
"""
generate_colour_matrix.py
Reads tokens.json from the current directory and writes colour-matrix.html.

Section 1 — Primitive text-on-background matrix (WCAG AA/AAA, 4.5:1 / 7:1)
Section 2 — Component UI element audit (WCAG 1.4.11 non-text, 3:1 minimum)
             Source: Component + ColourSet token layers
"""

import json, math, os, sys

# ── Load tokens ───────────────────────────────────────────────────────────────

def load_tokens(path="tokens.json"):
    with open(path) as f:
        return json.load(f)

T = load_tokens()

# Short-key prefixes → actual JSON path prefixes
PREFIX = {
    "P":  ["Primitive",    "P"],
    "S":  ["Semantic",     "S"],
    "C":  ["Component",    "C"],
    "CS": ["Colour-Sets",  "CS"],
}

# ── Navigation helpers ────────────────────────────────────────────────────────

def dig(obj, *keys):
    for k in keys:
        if isinstance(obj, dict) and k in obj:
            obj = obj[k]
        else:
            return None
    return obj

def resolve(ref, depth=0):
    """Follow a token reference chain to a hex string. Returns None if unresolvable."""
    if depth > 14 or ref is None:
        return None
    if not isinstance(ref, str):
        return None
    ref = ref.strip()
    if ref.startswith("#"):
        return ref.upper()
    if not (ref.startswith("{") and ref.endswith("}")):
        return None

    path = ref.strip("{}").split(".")
    prefix = path[0]
    actual = (PREFIX.get(prefix, [prefix]) + path[1:]) if prefix in PREFIX else path

    node = dig(T, *actual)
    if node is None:
        return None
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"], depth + 1)
    return None

# ── Contrast ratio ─────────────────────────────────────────────────────────────

def _lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def luminance(hex_c):
    h = hex_c.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(h1, h2):
    if not h1 or not h2:
        return 0
    try:
        l1, l2 = luminance(h1), luminance(h2)
        hi, lo = max(l1, l2), min(l1, l2)
        return round((hi + 0.05) / (lo + 0.05), 2)
    except Exception:
        return 0

# ── WCAG badges ────────────────────────────────────────────────────────────────

def text_badge(ratio):
    if ratio >= 7:    return "AAA", "#1a7a4a", "#fff"
    if ratio >= 4.5:  return "AA",  "#555555", "#fff"
    if ratio >= 3:    return "AA18","#7a6000",  "#fff"
    return "DNP", "#c0392b", "#fff"

def ui_badge(ratio):
    """WCAG 1.4.11 — 3:1 for non-text elements."""
    if ratio >= 7:    return "AAA", "#1a7a4a", "#fff"
    if ratio >= 4.5:  return "AA+", "#1a5e7a", "#fff"
    if ratio >= 3:    return "AA",  "#555555", "#fff"
    return "DNP", "#c0392b", "#fff"

def badge_span(label, bg, fg):
    return (f'<span style="display:inline-block;font-size:9px;font-weight:800;'
            f'padding:2px 5px;border-radius:4px;background:{bg};color:{fg};'
            f'letter-spacing:0.04em;">{label}</span>')

# ── Token resolution helpers ───────────────────────────────────────────────────

def cs_button(cs_name, tier, prop, state="Enabled"):
    """Resolve a ColourSet button token to hex. cs_name = 'Base-1', 'ColorSet-5', etc."""
    node = dig(T, "Colour-Sets", "CS", cs_name, "Button", tier, prop, state)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

def cs_nav(cs_name, component, prop, state="Enabled"):
    node = dig(T, "Colour-Sets", "CS", cs_name, component, prop, state)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

def comp_button(mode, tier, prop, state="Enabled"):
    """Resolve a Component-layer button token (Default / Inverse modes)."""
    node = dig(T, "Component", "C", "Color", "CommonButton", mode, tier, prop, state)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

def comp_nav(component, mode, prop, state="Enabled"):
    node = dig(T, "Component", "C", "Color", component, mode, prop, state)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

def sem(path):
    """Resolve a semantic token path like 'Color.Focus.Default'."""
    node = dig(T, "Semantic", "S", *path.split("."))
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

# ── Surfaces ──────────────────────────────────────────────────────────────────

SURFACES = {
    "Default":    sem("Color.Background.Default.Main") or "#FFFFFF",
    "Inverse":    sem("Color.Background.Inverse.Main") or "#000000",
    "Base-1":     resolve(dig(T, "Colour-Sets","CS","Base-1",    "Background","Main","value") or ""),
    "Base-2":     resolve(dig(T, "Colour-Sets","CS","Base-2",    "Background","Main","value") or ""),
    "ColorSet-1": resolve(dig(T, "Colour-Sets","CS","ColorSet-1","Background","Main","value") or ""),
    "ColorSet-2": resolve(dig(T, "Colour-Sets","CS","ColorSet-2","Background","Main","value") or ""),
    "ColorSet-3": resolve(dig(T, "Colour-Sets","CS","ColorSet-3","Background","Main","value") or ""),
    "ColorSet-4": resolve(dig(T, "Colour-Sets","CS","ColorSet-4","Background","Main","value") or ""),
    "ColorSet-5": resolve(dig(T, "Colour-Sets","CS","ColorSet-5","Background","Main","value") or ""),
    "ColorSet-6": resolve(dig(T, "Colour-Sets","CS","ColorSet-6","Background","Main","value") or ""),
}
# Fallback for anything that didn't resolve
for k in SURFACES:
    if not SURFACES[k]:
        SURFACES[k] = "#FFFFFF"

CS_ORDER = ["Default", "Inverse", "Base-1", "Base-2",
            "ColorSet-1", "ColorSet-2", "ColorSet-3", "ColorSet-4",
            "ColorSet-5", "ColorSet-6"]

CS_LABELS = {
    "Default":    "Default",
    "Inverse":    "Inverse",
    "Base-1":     "Base-1",
    "Base-2":     "Base-2",
    "ColorSet-1": "CS-1",
    "ColorSet-2": "CS-2",
    "ColorSet-3": "CS-3",
    "ColorSet-4": "CS-4",
    "ColorSet-5": "CS-5",
    "ColorSet-6": "CS-6",
}

# ── Row definitions for Section 2 ─────────────────────────────────────────────
# Each row: (group, label, wcag_type, fn_that_returns_two_hex_strings_per_cs)
# fn receives cs_name, returns (element_hex, against_hex)

def button_container(tier):
    def fn(cs):
        surface = SURFACES[cs]
        if cs in ("Default", "Inverse"):
            mode = cs
            fg = comp_button(mode, tier, "Container-Background")
        else:
            fg = cs_button(cs, tier, "Container-Background")
        return fg, surface
    return fn

def button_label_on_container(tier):
    def fn(cs):
        if cs in ("Default", "Inverse"):
            mode = cs
            fg   = comp_button(mode, tier, "Label")
            bg   = comp_button(mode, tier, "Container-Background")
        else:
            fg = cs_button(cs, tier, "Label")
            bg = cs_button(cs, tier, "Container-Background")
        return fg, bg
    return fn

def button_border(tier):
    """Container-Border vs surface — used for Secondary (outlined) and Tertiary (ghost)."""
    def fn(cs):
        surface = SURFACES[cs]
        if cs in ("Default", "Inverse"):
            fg = comp_button(cs, tier, "Container-Border")
        else:
            fg = cs_button(cs, tier, "Container-Border")
        return fg, surface
    return fn

def button_label_on_surface(tier):
    """Label vs surface — meaningful for Secondary/Tertiary (transparent bg)."""
    def fn(cs):
        surface = SURFACES[cs]
        if cs in ("Default", "Inverse"):
            fg = comp_button(cs, tier, "Label")
        else:
            fg = cs_button(cs, tier, "Label")
        return fg, surface
    return fn

def nav_selected_border(component):
    def fn(cs):
        surface = SURFACES[cs]
        if cs in ("Default", "Inverse"):
            fg = comp_nav(component, cs, "Border", "Selected")
        else:
            fg = cs_nav(cs, component, "Border", "Selected")
        return fg, surface
    return fn

def nav_label(component):
    def fn(cs):
        surface = SURFACES[cs]
        if cs in ("Default", "Inverse"):
            fg = comp_nav(component, cs, "Label")
        else:
            fg = cs_nav(cs, component, "Label")
        return fg, surface
    return fn

def focus_ring():
    focus_default  = sem("Color.Focus.Default")
    focus_inverse  = sem("Color.Focus.Inverse")
    def fn(cs):
        surface = SURFACES[cs]
        # Determine if dark surface
        lum = luminance(surface)
        fg = focus_inverse if lum < 0.18 else focus_default
        return fg, surface
    return fn

# Row spec: (group_label, row_label, wcag_type, resolver_fn)
# wcag_type: 'text' (4.5:1) or 'ui' (3:1)

AUDIT_ROWS = [
    # ── Buttons ──────────────────────────────────────────────────────────────
    ("Buttons — Primary",    "Container vs Surface",   "ui",   button_container("Primary")),
    ("Buttons — Primary",    "Label vs Container",     "text", button_label_on_container("Primary")),
    ("Buttons — Secondary",  "Border vs Surface",      "ui",   button_border("Secondary")),
    ("Buttons — Secondary",  "Label vs Surface",       "text", button_label_on_surface("Secondary")),
    ("Buttons — Tertiary",   "Border vs Surface",      "ui",   button_border("Tertiary")),
    ("Buttons — Tertiary",   "Label vs Surface",       "text", button_label_on_surface("Tertiary")),
    # ── Navigation indicators ─────────────────────────────────────────────────
    ("Selected Indicators",  "PageNav Border · Selected", "ui",   nav_selected_border("PageNavigation")),
    ("Selected Indicators",  "PageNav Label · Enabled",   "text", nav_label("PageNavigation")),
    ("Selected Indicators",  "Tab Border · Selected",     "ui",   nav_selected_border("Tab")),
    ("Selected Indicators",  "Tab Label · Enabled",       "text", nav_label("Tab")),
    # ── Focus rings ───────────────────────────────────────────────────────────
    ("Focus",                "Focus ring vs Surface",  "ui",   focus_ring()),
]

# ── Primitives for Section 1 ──────────────────────────────────────────────────

def get_brand_primitives():
    """Return [(label, hex)] filtering out Shades, Tints, Opacity groups."""
    out = []
    prim = dig(T, "Primitive", "P", "Color") or {}
    skip_groups = {"Shades", "Tints", "Opacity"}
    for grp, items in prim.items():
        if grp in skip_groups or not isinstance(items, dict):
            continue
        for shade, val in items.items():
            if isinstance(val, dict) and "value" in val and isinstance(val["value"], str) and val["value"].startswith("#"):
                out.append((f"{grp} {shade}", val["value"].upper()))
    return out

# ── HTML helpers ──────────────────────────────────────────────────────────────

def contrast_cell(fg, bg, wcag_type="text"):
    if not fg or not bg or "transparent" in (fg or "").lower() or "transparent" in (bg or "").lower():
        return ('<td style="padding:8px;text-align:center;vertical-align:middle;'
                'background:#f5f5f5;"><span style="color:#ccc;font-size:11px;">—</span></td>')
    ratio = contrast(fg, bg)
    if wcag_type == "text":
        label, bbg, bfg = text_badge(ratio)
    else:
        label, bbg, bfg = ui_badge(ratio)

    swatch = (f'<div style="width:20px;height:20px;border-radius:50%;background:{fg};'
              f'margin:0 auto 4px;box-shadow:0 0 0 2px {bg},0 0 0 3px rgba(0,0,0,0.15);"></div>')
    b = badge_span(label, bbg, bfg)
    ratio_str = f'<div style="font-size:9px;margin-top:3px;color:{fg};font-weight:600;">{ratio}:1</div>'
    return (f'<td style="padding:8px 4px;text-align:center;vertical-align:middle;background:{bg};'
            f'border:1px solid rgba(0,0,0,0.08);">{swatch}{b}{ratio_str}</td>')

def text_on_bg_cell(fg_hex, bg_hex):
    """Cell for the primitive matrix (Section 1)."""
    if fg_hex.upper() == bg_hex.upper():
        diag = ('<div style="position:relative;width:56px;height:40px;margin:0 auto;overflow:hidden;">'
                '<div style="position:absolute;top:50%;left:50%;width:130%;height:1px;'
                'background:rgba(128,128,128,0.35);transform:translate(-50%,-50%) rotate(30deg);"></div>'
                '<div style="position:absolute;top:50%;left:50%;width:130%;height:1px;'
                'background:rgba(128,128,128,0.35);transform:translate(-50%,-50%) rotate(-30deg);"></div>'
                '</div>')
        return f'<td style="background:{bg_hex};padding:8px;text-align:center;">{diag}</td>'
    ratio = contrast(fg_hex, bg_hex)
    label, bbg, bfg = text_badge(ratio)
    b = badge_span(label, bbg, bfg)
    sample = f'<span style="display:block;font-size:12px;font-weight:700;color:{fg_hex};margin-bottom:5px;">Text</span>'
    ratio_str = f'<span style="font-size:9px;color:{fg_hex};opacity:0.75;font-weight:500;">{ratio}</span>'
    return (f'<td style="background:{bg_hex};padding:8px;text-align:center;vertical-align:middle;'
            f'border-right:1px solid rgba(0,0,0,0.07);border-bottom:1px solid rgba(0,0,0,0.07);">'
            f'{sample}{b} {ratio_str}</td>')

def surface_header_cell(cs_name, surface_hex):
    lum = luminance(surface_hex)
    txt = "#111" if lum > 0.18 else "#fff"
    label = CS_LABELS.get(cs_name, cs_name)
    return (f'<th style="background:{surface_hex};padding:10px 6px;text-align:center;'
            f'vertical-align:bottom;min-width:90px;border-bottom:2px solid rgba(0,0,0,0.15);">'
            f'<span style="display:block;font-size:11px;font-weight:700;color:{txt};margin-bottom:2px;">{label}</span>'
            f'<span style="display:block;font-size:9px;font-family:monospace;color:{txt};opacity:0.65;">{surface_hex}</span>'
            f'</th>')

def group_row(label, col_count):
    return (f'<tr><td colspan="{col_count+1}" style="background:#f0f0f0;padding:8px 14px;'
            f'font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;'
            f'color:#666;border-top:3px solid #ddd;">{label}</td></tr>')

# ── Section 1: Primitive text matrix ─────────────────────────────────────────

def build_section1():
    prims = get_brand_primitives()
    if not prims:
        return "<p>No primitive colours found.</p>"

    # Header row
    header_cells = []
    for label, hex_c in prims:
        lum = luminance(hex_c)
        txt_col = "#111" if lum > 0.18 else "#fff"
        header_cells.append(
            f'<th style="background:{hex_c};padding:10px 6px 8px;text-align:center;'
            f'vertical-align:bottom;min-width:90px;border-bottom:2px solid #e0e0e0;">'
            f'<span style="display:block;font-size:10px;font-weight:700;color:{txt_col};margin-bottom:2px;">{label}</span>'
            f'<span style="display:block;font-size:9px;font-family:monospace;color:{txt_col};opacity:0.65;">{hex_c}</span>'
            f'</th>'
        )

    rows = []
    for bg_label, bg_hex in prims:
        lum = luminance(bg_hex)
        txt_col = "#111" if lum > 0.18 else "#fff"
        row_header = (
            f'<td style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:1px solid #eee;'
            f'padding:10px 14px;white-space:nowrap;min-width:150px;">'
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<div style="width:28px;height:28px;border-radius:5px;background:{bg_hex};'
            f'border:1px solid rgba(0,0,0,0.1);flex-shrink:0;"></div>'
            f'<div><div style="font-size:11px;font-weight:700;color:#111;">{bg_label}</div>'
            f'<div style="font-size:9px;font-family:monospace;color:#999;">{bg_hex}</div></div>'
            f'</div></td>'
        )
        cells = [text_on_bg_cell(fg_hex, bg_hex) for _, fg_hex in prims]
        rows.append(f'<tr>{row_header}{"".join(cells)}</tr>')

    corner = ('<th style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:2px solid #e0e0e0;'
              'padding:10px 14px;text-align:left;vertical-align:bottom;min-width:150px;">'
              '<span style="display:block;font-size:8px;color:#bbb;font-weight:700;text-transform:uppercase;'
              'letter-spacing:0.06em;text-align:right;">Text →</span>'
              '<span style="display:block;font-size:8px;color:#bbb;font-weight:700;text-transform:uppercase;'
              'letter-spacing:0.06em;margin-top:2px;">Background ↓</span></th>')

    return (f'<div class="wrap"><table>'
            f'<thead><tr>{corner}{"".join(header_cells)}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            f'</table></div>')

# ── Section 2: Component UI audit ────────────────────────────────────────────

def build_section2():
    n = len(CS_ORDER)

    # Header
    header_cells = [surface_header_cell(cs, SURFACES[cs]) for cs in CS_ORDER]
    corner = ('<th style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:2px solid #e0e0e0;'
              'padding:10px 14px;min-width:200px;font-size:10px;color:#888;font-weight:600;'
              'text-align:left;vertical-align:bottom;">Component · Element · Check</th>')

    rows = []
    prev_group = None
    for (group, row_label, wcag_type, resolver) in AUDIT_ROWS:
        if group != prev_group:
            rows.append(group_row(group, n))
            prev_group = group

        wcag_note = "text 4.5:1" if wcag_type == "text" else "UI 3:1"
        row_header = (
            f'<td style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:1px solid #eee;'
            f'padding:8px 14px;white-space:nowrap;">'
            f'<div style="font-size:11px;font-weight:600;color:#111;">{row_label}</div>'
            f'<div style="font-size:9px;color:#aaa;margin-top:1px;">WCAG 1.4.{"3" if wcag_type == "text" else "11"} · {wcag_note}</div>'
            f'</td>'
        )
        cells = []
        for cs in CS_ORDER:
            try:
                fg, bg = resolver(cs)
                cells.append(contrast_cell(fg, bg, wcag_type))
            except Exception:
                cells.append('<td style="background:#f5f5f5;padding:8px;text-align:center;"><span style="color:#ccc;font-size:10px;">err</span></td>')

        rows.append(f'<tr>{row_header}{"".join(cells)}</tr>')

    return (f'<div class="wrap"><table>'
            f'<thead><tr>{corner}{"".join(header_cells)}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            f'</table></div>')

# ── Main HTML ─────────────────────────────────────────────────────────────────

def build_html():
    brand = "Inter Miami CF"  # Could be read from token metadata

    prims = get_brand_primitives()
    prim_hexes = [h for _, h in prims]

    s1 = build_section1()
    s2 = build_section2()

    legend_items = [
        ("AAA",  "#1a7a4a", "#fff", "≥7:1 — text only"),
        ("AA",   "#555",    "#fff", "≥4.5:1 text / ≥3:1 UI"),
        ("AA18", "#7a6000", "#fff", "≥3:1 — large text only"),
        ("AA+",  "#1a5e7a", "#fff", "≥4.5:1 — UI element (exceeds)"),
        ("DNP",  "#c0392b", "#fff", "Does not pass — fix required"),
    ]
    legend_html = "".join(
        f'<span class="legend-item"><span class="badge" style="background:{bg};color:{fg}">{lbl}</span> {desc}</span>'
        for lbl, bg, fg, desc in legend_items
    )

    toolness_params = "&".join(
        f"n={lbl.replace(' ','')}&v={h.lstrip('#')}" for lbl, h in prims
    )
    toolness_url = f"https://toolness.github.io/accessible-color-matrix/?{toolness_params}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand} — Colour Accessibility Matrix</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: #f0f0f0; padding: 40px; }}
  h1 {{ font-size: 20px; font-weight: 700; margin-bottom: 4px; }}
  h2 {{ font-size: 15px; font-weight: 700; margin: 48px 0 4px; }}
  .subtitle {{ font-size: 12px; color: #888; margin-bottom: 28px; }}
  .subtitle a {{ color: #FF9CB4; text-decoration: none; }}
  .section-sub {{ font-size: 12px; color: #888; margin-bottom: 20px; }}
  .wrap {{ overflow-x: auto; margin-bottom: 8px; }}
  table {{ border-collapse: collapse; background: white; border-radius: 12px;
           overflow: hidden; box-shadow: 0 2px 16px rgba(0,0,0,0.08); }}
  .legend {{ margin-top: 20px; display: flex; gap: 16px; flex-wrap: wrap;
             align-items: center; font-size: 11px; color: #555; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .badge {{ display:inline-block; font-size:9px; font-weight:800; padding:2px 5px;
            border-radius:4px; letter-spacing:0.04em; }}
  .rules {{ margin-top: 24px; background:#fff; border-radius:12px; padding:22px 26px;
            box-shadow:0 2px 12px rgba(0,0,0,0.06); font-size:12px; color:#555;
            line-height:1.7; }}
  .rules h3 {{ font-size:13px; font-weight:700; color:#111; margin-bottom:8px; }}
  .rules p {{ margin-bottom:10px; }}
</style>
</head>
<body>

<h1>{brand} — Colour Accessibility Matrix</h1>
<p class="subtitle">
  WCAG 2.1 · Generated from tokens.json ·
  <a href="{toolness_url}" target="_blank">Open primitives in toolness ↗</a>
</p>

<h2>Section 1 — Primitive Text Contrast Matrix</h2>
<p class="section-sub">Every primitive brand colour as text on every primitive brand colour as background. WCAG 1.4.3 (text) — AA requires 4.5:1, AAA requires 7:1.</p>
{s1}

<h2>Section 2 — Component UI Element Audit</h2>
<p class="section-sub">
  Reads directly from the Component + ColourSet token layers. Each cell shows the element colour on its surface.
  <strong>Text rows</strong>: WCAG 1.4.3 — 4.5:1 minimum.
  <strong>UI rows</strong>: WCAG 1.4.11 (non-text contrast) — 3:1 minimum for borders, focus rings, and selected indicators.
</p>
{s2}

<div class="legend">
  <strong>Legend:</strong>
  {legend_html}
</div>

<div class="rules">
  <h3>How to read this matrix</h3>
  <p><strong>Section 1</strong> — Each cell is the text colour (column) rendered on the row's background colour.
     Use this to validate which primitive colour pairings are safe for text content. Only AA or AAA pairings enter ColourSets and semantic tokens.</p>
  <p><strong>Section 2</strong> — Each row is a specific component UI element check across all 10 surfaces (ColourSets).
     <em>UI rows</em> test whether an element (border, button container, focus ring) is distinguishable from its surface — minimum 3:1 per WCAG 1.4.11.
     <em>Text rows</em> test whether label/body text inside components meets the 4.5:1 minimum.</p>
  <p><strong>DNP (Does Not Pass)</strong> — this pairing must not be used. Fix at the lowest token layer that cascades the change everywhere (Semantic first, ColourSet override second, Component override last).</p>
</div>

</body>
</html>
"""

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "colour-matrix.html"
    html = build_html()
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Written → {out_path}")
