#!/usr/bin/env python3
"""
generate_colour_matrix.py
Reads tokens.json from the current directory and writes colour-matrix.html.

Section 1 — Primitive text-on-background matrix (WCAG 1.4.3, AA 4.5:1 / AAA 7:1)
Section 2 — Full component UI audit (WCAG 1.4.11 non-text 3:1 + WCAG 1.4.3 text 4.5:1)
             Auto-scans every component in Component.C.Color, uses CS overrides where they
             exist and falls back to Component layer (mode chosen by surface luminance).
"""

import json, sys

# ── Load & navigation ─────────────────────────────────────────────────────────

def _load(path="tokens.json"):
    with open(path) as f:
        return json.load(f)

T = _load()

PREFIX = {"P": ["Primitive","P"], "S": ["Semantic","S"],
          "C": ["Component","C"], "CS": ["Colour-Sets","CS"]}

def dig(obj, *keys):
    for k in keys:
        obj = obj.get(k, {}) if isinstance(obj, dict) else None
        if obj is None:
            return None
    return obj

def resolve(ref, depth=0):
    if depth > 14 or not isinstance(ref, str):
        return None
    ref = ref.strip()
    if ref.startswith("#"):
        return ref.upper()
    if not (ref.startswith("{") and ref.endswith("}")):
        return None
    path = ref.strip("{}").split(".")
    prefix = path[0]
    actual = (PREFIX[prefix] + path[1:]) if prefix in PREFIX else path
    node = dig(T, *actual)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"], depth + 1)
    return None

# ── Contrast ──────────────────────────────────────────────────────────────────

def _lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def luminance(hx):
    h = hx.lstrip("#")
    if len(h) == 3: h = "".join(c*2 for c in h)
    r,g,b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    return 0.2126*_lin(r) + 0.7152*_lin(g) + 0.0722*_lin(b)

def contrast(h1, h2):
    if not h1 or not h2: return 0
    try:
        l1,l2 = luminance(h1), luminance(h2)
        return round((max(l1,l2)+0.05)/(min(l1,l2)+0.05), 2)
    except Exception: return 0

# ── Badges ────────────────────────────────────────────────────────────────────

def text_badge(r):
    if r >= 7:   return "AAA","#1a7a4a","#fff"
    if r >= 4.5: return "AA", "#555",   "#fff"
    if r >= 3:   return "AA18","#7a6000","#fff"
    return "DNP","#c0392b","#fff"

def ui_badge(r):
    if r >= 7:   return "AAA","#1a7a4a","#fff"
    if r >= 4.5: return "AA+","#1a5e7a","#fff"
    if r >= 3:   return "AA", "#555",   "#fff"
    return "DNP","#c0392b","#fff"

def badge_span(lbl, bg, fg):
    return (f'<span style="display:inline-block;font-size:9px;font-weight:800;padding:2px 5px;'
            f'border-radius:4px;background:{bg};color:{fg};letter-spacing:0.04em;">{lbl}</span>')

# ── Surfaces ──────────────────────────────────────────────────────────────────

def _surf_hex(path_in_cs):
    node = dig(T, "Colour-Sets", "CS", *path_in_cs, "Background", "Main")
    if isinstance(node, dict):
        return resolve(node.get("value",""))
    return None

def _sem_hex(path):
    node = dig(T, "Semantic", "S", *path.split("."))
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

SURFACES = {
    "Default":    _sem_hex("Color.Background.Default.Main") or "#FFFFFF",
    "Inverse":    _sem_hex("Color.Background.Inverse.Main") or "#000000",
    "Base-1":     _surf_hex(["Base-1"])     or "#FFFFFF",
    "Base-2":     _surf_hex(["Base-2"])     or "#000000",
    "ColorSet-1": _surf_hex(["ColorSet-1"]) or "#FFFFFF",
    "ColorSet-2": _surf_hex(["ColorSet-2"]) or "#FFFFFF",
    "ColorSet-3": _surf_hex(["ColorSet-3"]) or "#FF9CB4",
    "ColorSet-4": _surf_hex(["ColorSet-4"]) or "#FF6B8E",
    "ColorSet-5": _surf_hex(["ColorSet-5"]) or "#343A40",
    "ColorSet-6": _surf_hex(["ColorSet-6"]) or "#000000",
}
for k in SURFACES:
    if not SURFACES[k]: SURFACES[k] = "#FFFFFF"

CS_ORDER  = ["Default","Inverse","Base-1","Base-2",
             "ColorSet-1","ColorSet-2","ColorSet-3","ColorSet-4","ColorSet-5","ColorSet-6"]
CS_LABELS = {"Default":"Default","Inverse":"Inverse","Base-1":"Base-1","Base-2":"Base-2",
             "ColorSet-1":"CS-1","ColorSet-2":"CS-2","ColorSet-3":"CS-3",
             "ColorSet-4":"CS-4","ColorSet-5":"CS-5","ColorSet-6":"CS-6"}

# Which CS name is "dark" (uses Inverse mode for Component fallback)
def _is_dark(cs): return luminance(SURFACES[cs]) < 0.18

# ── Component → CS key mapping (only 5 components have CS overrides) ──────────

COMP_TO_CS = {
    "CommonButton": "Button",
    "Tab":          "Tab",
    "PageNavigation":"PageNavigation",
    "TextButton":   "TextButton",
    # Accordion is in CS but has no Component entry — handled separately
}

# ── Property classification ────────────────────────────────────────────────────

TEXT_PROPS      = {"Label","TitleText","SupportingText","NumberText","ForenameText",
                   "SurnameText","ShirtNumber"}
UI_FILL_PROPS   = {"Background","Container-Background","Icon-Background"}
UI_BORDER_PROPS = {"Border","Container-Border","Indicator"}
ICON_PROPS      = {"Icon"}
SKIP_PROPS      = {"Contents-Background","Contents-Border","Icon-Border",
                   "Overlay","Divider","ImageOverlay","Active-copy"}
AUDIT_STATES    = {"Enabled","Selected","Filled"}

# ── Auto-scan: walk Component.C.Color and build check rows ───────────────────

def _resolve_leaf(comp_path, prop, state, cs_name):
    """
    Resolve a token to hex for a given CS surface.
    comp_path = list of path parts inside comp_data (e.g. ['Default','Primary','Label'])
    Tries CS override first, then Component layer.
    """
    comp_name = comp_path[0]  # first element is the component name
    mode      = comp_path[1]  # 'Default' or 'Inverse'

    # 1. Try CS override (only for mapped components)
    cs_key = COMP_TO_CS.get(comp_name)
    if cs_key and cs_name not in ("Default", "Inverse"):
        # Build CS path: CS.{cs_name}.{cs_key}.{middle_parts}.{prop}.{state}
        middle = comp_path[2:]   # e.g. ['Primary'] for CommonButton, [] for Tab
        cs_path_parts = [cs_key] + middle + [prop, state]
        node = dig(T, "Colour-Sets", "CS", cs_name, *cs_path_parts)
        if isinstance(node, dict) and "value" in node:
            val = resolve(node["value"])
            if val: return val

    # 2. For Default/Inverse CS columns, or if CS had no override, use Component layer
    # Determine which mode to use
    if cs_name == "Default":
        use_mode = "Default"
    elif cs_name == "Inverse":
        use_mode = "Inverse"
    else:
        use_mode = "Inverse" if _is_dark(cs_name) else "Default"

    # Replace mode in path
    actual_path = [comp_name, use_mode] + comp_path[2:]
    node = dig(T, "Component", "C", "Color", *actual_path, prop, state)
    if isinstance(node, dict) and "value" in node:
        return resolve(node["value"])
    return None

def _resolve_container(comp_path, state, cs_name):
    """Try to resolve the Background or Container-Background for a component (for label-vs-container checks)."""
    for container_prop in ("Container-Background", "Background"):
        val = _resolve_leaf(comp_path, container_prop, state, cs_name)
        if val and "transparent" not in val.lower():
            return val
    return None

def _make_row(comp_name, path_parts, prop, state, comp_path, row_type="standard"):
    mid_parts = [p for p in path_parts if p]
    label_mid = " / ".join(mid_parts) + " / " if mid_parts else ""
    is_text = prop in TEXT_PROPS
    if prop in UI_FILL_PROPS:
        wcag_type, against = "ui", "surface"
    elif prop in UI_BORDER_PROPS:
        wcag_type, against = "ui", "surface"
    elif prop in TEXT_PROPS:
        wcag_type, against = "text", "container_or_surface"
    elif prop in ICON_PROPS:
        wcag_type, against = "ui", "container_or_surface"
    else:
        return None
    return {
        "group": comp_name,
        "label": f"{label_mid}{prop} · {state}",
        "comp_path": comp_path,
        "prop": prop, "state": state,
        "wcag_type": wcag_type, "against": against,
        "row_type": row_type,
    }

def _walk_comp(comp_name, comp_data, mode, path_parts, rows, containers):
    """Walk a mode-based component tree (has Default/Inverse at root)."""
    for key, node in (comp_data or {}).items():
        if not isinstance(node, dict):
            continue
        new_path = path_parts + [key]
        if "value" in node and "type" in node:
            if len(new_path) < 2:
                continue
            prop  = new_path[-2]   # path_parts[-1]
            state = new_path[-1]   # key
            if state not in AUDIT_STATES or prop in SKIP_PROPS:
                continue
            if prop in ICON_PROPS and state != "Enabled":
                continue
            # path_parts[-1] == prop; strip it so comp_path ends at the parent group
            mid = path_parts[:-1]
            full_comp_path = [comp_name, mode] + mid
            row = _make_row(comp_name, mid, prop, state, full_comp_path)
            if row:
                rows.append(row)
        else:
            _walk_comp(comp_name, node, mode, new_path, rows, containers)

def _walk_flat(comp_name, comp_data, path_parts, rows):
    """Walk a flat/variant component tree (no Default/Inverse; resolves via Semantic tokens directly)."""
    for key, node in (comp_data or {}).items():
        if not isinstance(node, dict):
            continue
        new_path = path_parts + [key]
        if "value" in node and "type" in node:
            if len(new_path) < 2:
                continue
            prop  = new_path[-2]   # path_parts[-1]
            state = new_path[-1]   # key
            if state not in AUDIT_STATES or prop in SKIP_PROPS:
                continue
            if prop in ICON_PROPS and state != "Enabled":
                continue
            resolved_hex = resolve(node["value"])
            if not resolved_hex:
                continue
            if prop in UI_FILL_PROPS:
                wcag_type = "ui"
            elif prop in UI_BORDER_PROPS:
                wcag_type = "ui"
            elif prop in TEXT_PROPS:
                wcag_type = "text"
            elif prop in ICON_PROPS:
                wcag_type = "ui"
            else:
                continue
            # path_parts[-1] == prop; strip it for clean label
            mid_parts = [p for p in path_parts[:-1] if p]
            label_mid = " / ".join(mid_parts) + " / " if mid_parts else ""
            rows.append({
                "group": comp_name,
                "label": f"{label_mid}{prop} · {state}",
                "comp_path": None,
                "prop": prop, "state": state,
                "wcag_type": wcag_type, "against": "surface",
                "row_type": "flat",
                "resolved_hex": resolved_hex,
            })
        else:
            _walk_flat(comp_name, node, new_path, rows)

# First variant key to use when a component has no Default/Inverse
_VARIANT_PRIORITY = ("Small", "XL", "X-Large", "Open", "GlobalLink", "GlobalLink-Trigger",
                     "InputField", "Primary", "Default-CS")

def build_audit_rows():
    comp_tokens = dig(T, "Component", "C", "Color") or {}
    rows = []
    containers = {}

    for comp_name, comp_data in comp_tokens.items():
        if "Default" in comp_data:
            mode_data = comp_data["Default"]
            # Detect flat-under-mode: Default's children are leaves, not sub-groups
            # (e.g. Link: Default.Enabled → value/type directly)
            if any("value" in v for v in mode_data.values() if isinstance(v, dict)):
                # Treat as flat — walk Default as a prop named after comp, states are children
                for state, leaf in mode_data.items():
                    if not isinstance(leaf, dict) or "value" not in leaf:
                        continue
                    if state not in AUDIT_STATES:
                        continue
                    resolved_hex = resolve(leaf["value"])
                    if resolved_hex:
                        rows.append({
                            "group": comp_name,
                            "label": f"Label · {state}",
                            "comp_path": None, "prop": "Label", "state": state,
                            "wcag_type": "text", "against": "surface",
                            "row_type": "flat", "resolved_hex": resolved_hex,
                        })
            else:
                # Standard mode-based component
                _walk_comp(comp_name, mode_data, "Default", [], rows, containers)
        else:
            # Non-standard: check for sub-component wrapper (e.g. Form.InputField)
            sub_data = None
            for sub_key, sub_val in comp_data.items():
                if isinstance(sub_val, dict) and "Default" in sub_val:
                    # Sub-component has its own Default mode — walk it as standard
                    _walk_comp(f"{comp_name} / {sub_key}", sub_val["Default"], "Default", [], rows, containers)
                    sub_data = True
                    break

            if not sub_data:
                # Pick the first recognized variant key, else walk flat from root
                walked = False
                for vk in _VARIANT_PRIORITY:
                    if vk in comp_data:
                        _walk_flat(comp_name, comp_data[vk], [], rows)
                        walked = True
                        break
                if not walked:
                    _walk_flat(comp_name, comp_data, [], rows)

    # De-duplicate
    seen = set()
    unique_rows = []
    for r in rows:
        key = (r["group"], r["label"], r["prop"], r["state"], r["wcag_type"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(r)

    return unique_rows

# ── Per-CS resolver ────────────────────────────────────────────────────────────

def resolve_row_for_cs(row, cs_name):
    """Return (element_hex, against_hex) for a row × CS pairing."""
    surface = SURFACES[cs_name]

    # Flat rows: token is pre-resolved, always same hex regardless of CS
    if row.get("row_type") == "flat":
        element = row.get("resolved_hex")
        return element, surface

    comp_path = row["comp_path"]  # [comp_name, mode, ...middle_parts]
    prop      = row["prop"]
    state     = row["state"]

    element = _resolve_leaf(comp_path, prop, state, cs_name)
    if not element:
        return None, None

    if row["against"] == "surface":
        return element, surface

    # container_or_surface: prefer pairing against container-background
    container = _resolve_container(comp_path, "Enabled", cs_name)
    against = container if container else surface
    return element, against

# ── Primitives (Section 1) ────────────────────────────────────────────────────

def get_brand_primitives():
    out = []
    prim = dig(T, "Primitive", "P", "Color") or {}
    skip = {"Shades","Tints","Opacity"}
    for grp, items in prim.items():
        if grp in skip or not isinstance(items, dict): continue
        for shade, val in items.items():
            if isinstance(val,dict) and isinstance(val.get("value",""),str) and val.get("value","").startswith("#"):
                out.append((f"{grp} {shade}", val["value"].upper()))
    return out

# ── HTML helpers ──────────────────────────────────────────────────────────────

def contrast_cell(fg, bg, wcag_type="ui"):
    is_transparent = any("transparent" in (v or "").lower() for v in [fg, bg])
    if not fg or not bg or is_transparent:
        return ('<td style="padding:6px 3px;text-align:center;vertical-align:middle;'
                'background:#f8f8f8;border:1px solid #eee;">'
                '<span style="color:#ddd;font-size:10px;">—</span></td>')
    ratio = contrast(fg, bg)
    lbl, bbg, bfg = (text_badge if wcag_type=="text" else ui_badge)(ratio)
    b     = badge_span(lbl, bbg, bfg)
    swatch= (f'<div style="width:18px;height:18px;border-radius:50%;background:{fg};'
             f'margin:0 auto 3px;box-shadow:0 0 0 2px {bg},0 0 0 3px rgba(0,0,0,0.12);"></div>')
    return (f'<td style="padding:6px 3px;text-align:center;vertical-align:middle;'
            f'background:{bg};border:1px solid rgba(0,0,0,0.09);">'
            f'{swatch}{b}'
            f'<div style="font-size:8px;margin-top:2px;color:{fg};font-weight:600;">{ratio}:1</div>'
            f'</td>')

def text_on_bg_cell(fg_hex, bg_hex):
    if fg_hex.upper() == bg_hex.upper():
        diag = ('<div style="position:relative;width:52px;height:36px;margin:0 auto;overflow:hidden;">'
                '<div style="position:absolute;top:50%;left:50%;width:130%;height:1px;background:rgba(128,128,128,0.3);transform:translate(-50%,-50%) rotate(30deg);"></div>'
                '<div style="position:absolute;top:50%;left:50%;width:130%;height:1px;background:rgba(128,128,128,0.3);transform:translate(-50%,-50%) rotate(-30deg);"></div>'
                '</div>')
        return f'<td style="background:{bg_hex};padding:6px;text-align:center;">{diag}</td>'
    ratio = contrast(fg_hex, bg_hex)
    lbl,bbg,bfg = text_badge(ratio)
    return (f'<td style="background:{bg_hex};padding:6px 4px;text-align:center;vertical-align:middle;'
            f'border-right:1px solid rgba(0,0,0,0.07);border-bottom:1px solid rgba(0,0,0,0.07);">'
            f'<span style="display:block;font-size:12px;font-weight:700;color:{fg_hex};margin-bottom:4px;">Text</span>'
            f'{badge_span(lbl,bbg,bfg)} '
            f'<span style="font-size:9px;color:{fg_hex};opacity:0.7;font-weight:500;">{ratio}</span>'
            f'</td>')

def surface_th(cs_name):
    hx = SURFACES[cs_name]
    lum = luminance(hx)
    txt = "#111" if lum > 0.18 else "#fff"
    lbl = CS_LABELS.get(cs_name, cs_name)
    return (f'<th style="background:{hx};padding:8px 4px;text-align:center;vertical-align:bottom;'
            f'min-width:80px;border-bottom:2px solid rgba(0,0,0,0.15);">'
            f'<span style="display:block;font-size:10px;font-weight:700;color:{txt};margin-bottom:1px;">{lbl}</span>'
            f'<span style="display:block;font-size:8px;font-family:monospace;color:{txt};opacity:0.65;">{hx}</span>'
            f'</th>')

def prim_th(label, hx):
    lum = luminance(hx)
    txt = "#111" if lum > 0.18 else "#fff"
    return (f'<th style="background:{hx};padding:8px 4px;text-align:center;vertical-align:bottom;'
            f'min-width:88px;border-bottom:2px solid #e0e0e0;">'
            f'<span style="display:block;font-size:10px;font-weight:700;color:{txt};margin-bottom:1px;">{label}</span>'
            f'<span style="display:block;font-size:8px;font-family:monospace;color:{txt};opacity:0.65;">{hx}</span>'
            f'</th>')

def group_row_html(label, n_cols):
    return (f'<tr><td colspan="{n_cols+1}" style="background:#ebebeb;padding:7px 14px;'
            f'font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:0.08em;'
            f'color:#666;border-top:3px solid #d0d0d0;">{label}</td></tr>')

# ── Section 1 ─────────────────────────────────────────────────────────────────

def build_section1():
    prims = get_brand_primitives()
    if not prims: return "<p>No primitives found.</p>"

    corner = ('<th style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:2px solid #e0e0e0;'
              'padding:10px 14px;text-align:left;vertical-align:bottom;min-width:140px;">'
              '<span style="display:block;font-size:8px;color:#bbb;font-weight:700;text-transform:uppercase;'
              'letter-spacing:0.06em;text-align:right;">Text →</span>'
              '<span style="display:block;font-size:8px;color:#bbb;font-weight:700;text-transform:uppercase;'
              'letter-spacing:0.06em;margin-top:1px;">Background ↓</span></th>')
    headers = "".join(prim_th(lbl, hx) for lbl, hx in prims)

    rows_html = []
    for bg_lbl, bg_hx in prims:
        lum = luminance(bg_hx)
        rh = (f'<td style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:1px solid #eee;'
              f'padding:9px 13px;white-space:nowrap;">'
              f'<div style="display:flex;align-items:center;gap:8px;">'
              f'<div style="width:26px;height:26px;border-radius:5px;background:{bg_hx};'
              f'border:1px solid rgba(0,0,0,0.1);flex-shrink:0;"></div>'
              f'<div><div style="font-size:11px;font-weight:700;color:#111;">{bg_lbl}</div>'
              f'<div style="font-size:9px;font-family:monospace;color:#999;">{bg_hx}</div></div>'
              f'</div></td>')
        cells = "".join(text_on_bg_cell(fg_hx, bg_hx) for _, fg_hx in prims)
        rows_html.append(f'<tr>{rh}{cells}</tr>')

    return (f'<div class="wrap"><table>'
            f'<thead><tr>{corner}{headers}</tr></thead>'
            f'<tbody>{"".join(rows_html)}</tbody>'
            f'</table></div>')

# ── Section 2 ─────────────────────────────────────────────────────────────────

def build_section2():
    rows = build_audit_rows()
    n = len(CS_ORDER)

    corner = ('<th style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:2px solid #e0e0e0;'
              'padding:10px 14px;min-width:220px;font-size:10px;color:#888;font-weight:600;'
              'text-align:left;vertical-align:bottom;">Component · Property · State</th>')
    headers = "".join(surface_th(cs) for cs in CS_ORDER)

    # Group rows by component
    rows_html = []
    prev_group = None
    for row in rows:
        grp = row["group"]
        if grp != prev_group:
            rows_html.append(group_row_html(grp, n))
            prev_group = grp

        wcag_ref = "WCAG 1.4.3 · text 4.5:1" if row["wcag_type"]=="text" else "WCAG 1.4.11 · UI 3:1"
        rh = (f'<td style="background:#fff;border-right:2px solid #e0e0e0;border-bottom:1px solid #eee;'
              f'padding:6px 13px;white-space:nowrap;">'
              f'<div style="font-size:11px;font-weight:600;color:#111;">{row["label"]}</div>'
              f'<div style="font-size:8px;color:#bbb;margin-top:1px;">{wcag_ref}</div></td>')

        cells = []
        for cs in CS_ORDER:
            try:
                fg, bg = resolve_row_for_cs(row, cs)
                cells.append(contrast_cell(fg, bg, row["wcag_type"]))
            except Exception:
                cells.append('<td style="background:#f5f5f5;padding:6px;text-align:center;"><span style="color:#ccc;font-size:9px;">err</span></td>')

        rows_html.append(f'<tr>{rh}{"".join(cells)}</tr>')

    return (f'<div class="wrap"><table>'
            f'<thead><tr>{corner}{headers}</tr></thead>'
            f'<tbody>{"".join(rows_html)}</tbody>'
            f'</table></div>')

# ── Build full HTML ────────────────────────────────────────────────────────────

def build_html():
    brand = "Inter Miami CF"
    prims = get_brand_primitives()
    params = "&".join(f"n={l.replace(' ','')}&v={h.lstrip('#')}" for l,h in prims)
    toolness = f"https://toolness.github.io/accessible-color-matrix/?{params}"

    s1 = build_section1()
    s2 = build_section2()

    legend = [
        ("AAA","#1a7a4a","#fff","≥7:1 text"),
        ("AA", "#555",   "#fff","≥4.5:1 text / ≥3:1 UI"),
        ("AA+","#1a5e7a","#fff","≥4.5:1 UI element (exceeds min)"),
        ("AA18","#7a6000","#fff","≥3:1 large text only"),
        ("DNP","#c0392b","#fff","Does not pass — fix required"),
    ]
    leg_html = "".join(
        f'<span class="legend-item">{badge_span(l,bg,fg)} {desc}</span>'
        for l,bg,fg,desc in legend
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand} — Colour Accessibility Matrix</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
          background:#f0f0f0; padding:40px; }}
  h1 {{ font-size:20px; font-weight:700; margin-bottom:4px; }}
  h2 {{ font-size:15px; font-weight:700; margin:48px 0 4px; }}
  .subtitle {{ font-size:12px; color:#888; margin-bottom:28px; }}
  .subtitle a {{ color:#FF9CB4; text-decoration:none; }}
  .section-sub {{ font-size:12px; color:#888; margin-bottom:18px; line-height:1.6; }}
  .wrap {{ overflow-x:auto; margin-bottom:8px; }}
  table {{ border-collapse:collapse; background:white; border-radius:12px;
           overflow:hidden; box-shadow:0 2px 16px rgba(0,0,0,0.08); }}
  .legend {{ margin-top:20px; display:flex; gap:14px; flex-wrap:wrap;
             align-items:center; font-size:11px; color:#555; }}
  .legend-item {{ display:flex; align-items:center; gap:6px; }}
  .rules {{ margin-top:24px; background:#fff; border-radius:12px; padding:20px 24px;
            box-shadow:0 2px 12px rgba(0,0,0,0.06); font-size:12px; color:#555;
            line-height:1.7; max-width:900px; }}
  .rules h3 {{ font-size:13px; font-weight:700; color:#111; margin-bottom:8px; }}
  .rules p {{ margin-bottom:8px; }}
</style>
</head>
<body>

<h1>{brand} — Colour Accessibility Matrix</h1>
<p class="subtitle">
  WCAG 2.1 · Generated from tokens.json ·
  <a href="{toolness}" target="_blank">Open primitives in toolness ↗</a>
</p>

<h2>Section 1 — Primitive Text Contrast Matrix</h2>
<p class="section-sub">Every primitive brand colour as text on every primitive brand colour as background.<br>
WCAG 1.4.3 — AA 4.5:1 · AAA 7:1 · AA18 3:1 large text only.</p>
{s1}

<h2>Section 2 — Full Component UI Audit</h2>
<p class="section-sub">
  Auto-scanned from <strong>Component.C.Color</strong>. CS overrides applied where they exist (Button, Tab, PageNavigation, TextButton);
  remaining components resolved from Component layer using surface luminance to select Default or Inverse mode.<br>
  <strong>UI rows</strong>: WCAG 1.4.11 — 3:1 minimum for container backgrounds, borders, selected indicators, focus rings.<br>
  <strong>Text rows</strong>: WCAG 1.4.3 — 4.5:1 minimum for labels, titles, supporting text.
  Label rows compare against the component's own container background where one exists; otherwise against the page surface.
</p>
{s2}

<div class="legend"><strong>Legend:</strong> {leg_html}</div>

<div class="rules">
  <h3>How to read</h3>
  <p><strong>Section 1</strong> — diagonal = same-on-same (skip). Every other cell = text colour × background colour. Only AA+ pairs enter ColourSets.</p>
  <p><strong>Section 2</strong> — rows = one check per component property. Columns = the 10 surfaces.
     Each swatch shows the element colour on the surface it appears on.
     DNP = fix required before shipping; trace back to the lowest token layer that cascades the change (Semantic first, CS override second).</p>
  <p><strong>CS overrides</strong> — Button, Tab, PageNavigation, TextButton have per-CS token overrides and are resolved from those.
     All other components inherit the Default or Inverse semantic layer based on the surface's luminance.</p>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "colour-matrix.html"
    with open(out, "w") as f:
        f.write(build_html())
    print(f"Written → {out}")
