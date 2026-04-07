# DESIGN SYSTEM — Дело в огне (Menu Print Series)

**Project:** Restaurant menu print materials — A4 Landscape  
**Website:** delovogne.ru  
**Format:** 297mm × 210mm, margins 10mm, usable area 277mm × 190mm  
**Variants:** v1 Инферно · v2 Уголь · v3 Крафт

---

## 1. Visual Theme

The brand identity of "Дело в огне" (The Fire Business) is built around the primal drama of live fire: heat, char, glow, and warmth. Three visual registers express this:

| Variant | Codename | Emotional Register | Audience Signal |
|---------|----------|--------------------|-----------------|
| v1 | **Инферно** | Dark, dramatic, cinematic — like embers in a pit | Modern urban diner, evening crowd |
| v2 | **Уголь** | Swiss-clean, premium, restrained — like cooling charcoal | Upscale, design-aware guests |
| v3 | **Крафт** | Warm, tactile, nostalgic — like kraft paper wrapping hot meat | Family, casual, artisan feel |

All three variants share the same structural grid and menu content. Only the visual language changes.

---

## 2. Color Palette

### Brand Base (all variants inherit from this)

| Token | Hex | Role | Usage |
|-------|-----|------|-------|
| `--color-bg` | `#0A0A0A` | Deep black background | v1 primary background |
| `--color-surface` | `#141414` | Raised surface | Cards, elevated panels |
| `--color-text` | `#F0ECE4` | Warm white | Primary text on dark bg |
| `--color-text-secondary` | `rgba(240,236,228,0.55)` | Muted text | Weights, hints, captions |
| `--color-accent-orange` | `#FF6B00` | Hot orange | Prices, accent text, icons |
| `--color-accent-red` | `#E8321A` | Fire red | Gradient start, section borders |
| `--color-cream` | `#F0DBC0` | Warm cream | Gradient highlight, warm whites |
| `--color-fire-gradient` | `linear-gradient(135deg, #E8321A, #FF6B00)` | Fire gradient | Hero text, badges |

### v1 Инферно — Dark Fire

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0A0A0A` | Page fill |
| Header title gradient | `linear-gradient(135deg, #fff 30%, #F0DBC0 70%, #E8321A 100%)` | Restaurant name |
| Section title | `#FF6B00` | Category headers |
| Section rule | `rgba(232,50,26,0.3)` | Under section titles |
| Item text | `#F0ECE4` | Dish names |
| Price | `#FF6B00` bold | Cost |
| Weight | `rgba(240,236,228,0.4)` | Gram notation |
| Separator dots | `rgba(240,236,228,0.12)` | Dotted line between name/price |
| Column divider | `rgba(255,255,255,0.05)` | Vertical column border |
| Pill bg | `rgba(255,255,255,0.05)` | Sauce/tincture tags |
| Pill border | `rgba(255,255,255,0.1)` | Sauce/tincture tags |

### v2 Уголь — Premium Minimal

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#111111` | Page fill |
| Title | `#FFFFFF` weight 300 | Restaurant name |
| Title underline | `#FF6B00` 0.5px | Below restaurant name |
| Tagline | `rgba(255,255,255,0.4)` | Descriptor under name |
| Section title | `#FFFFFF` weight 700 | Category headers |
| Section rule | `rgba(255,255,255,0.08)` | Thin horizontal between sections |
| Item text | `rgba(255,255,255,0.85)` | Dish names |
| Weight brackets | `rgba(255,255,255,0.3)` | `[250г]` notation |
| Price | `#FF6B00` weight 600 | Cost |
| Column divider | `rgba(255,255,255,0.08)` 0.5px | Vertical column border |
| Sauce/tincture text | `rgba(255,255,255,0.6)` | Inline prose, no pills |

### v3 Крафт — Warm Vintage

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#F0E6C8` | Kraft paper fill |
| Paper texture | `repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(139,90,43,0.03) 2px, rgba(139,90,43,0.03) 4px)` | Layered on background |
| Text | `#1C0A00` | Deep dark brown, all body |
| Accent primary | `#8B1A00` | Brick red — sections, prices |
| Accent secondary | `#C4501A` | Terracotta — tagline, underlines |
| Weight | `rgba(139,58,0,0.5)` | Gram notation |
| Separator dots | `rgba(139,26,0,0.2)` | Dotted line |
| Column divider | `rgba(139,26,0,0.15)` 1.5px | Vertical column border |
| Pill bg | `rgba(139,26,0,0.08)` | Sauce/tincture tags |
| Pill border | `rgba(139,26,0,0.2)` | Sauce/tincture tags |
| Header strip | `rgba(139,90,43,0.08)` | Slightly darker header area |

---

## 3. Typography

All fonts fall back to system sans-serif. No external font loading — menus must be fully self-contained for offline print.

| Element | v1 Инферно | v2 Уголь | v3 Крафт |
|---------|-----------|---------|---------|
| Restaurant name | Helvetica Neue, 18pt, weight 900 | Helvetica Neue, 20pt, weight 300 | Georgia serif, 22pt, weight 900 |
| Tagline | Helvetica Neue, 7pt, letter-spacing 0.25em | Helvetica Neue, 6pt, letter-spacing 0.3em | Helvetica Neue, 8pt, italic |
| Section title | Helvetica Neue, 7.5pt, weight 700, UPPERCASE | Helvetica Neue, 6.5pt, weight 700, UPPERCASE, letter-spacing 0.3em | Helvetica Neue, 7.5pt, weight 700, UPPERCASE, letter-spacing 0.2em |
| Item name | Helvetica Neue, 8.5pt, weight 400 | Helvetica Neue, 8pt, weight 400 | Helvetica Neue, 8.5pt, weight 400 |
| Item weight | Helvetica Neue, 7pt | Helvetica Neue, 6.5pt | Helvetica Neue, 7pt |
| Price | Helvetica Neue, 9pt, weight 700 | Helvetica Neue, 8.5pt, weight 600 | Helvetica Neue, 9pt, weight 700 |
| Pill / tag | Helvetica Neue, 7pt | N/A (inline prose) | Helvetica Neue, 7pt |
| Footer | Helvetica Neue, 6pt | Helvetica Neue, 6pt | Helvetica Neue, 6.5pt, italic |
| Website URL | Helvetica Neue, 7pt | Helvetica Neue, 7pt | Helvetica Neue, 7pt |

**Typographic principles:**
- Font sizes in `pt` only — never `px` in print contexts
- Maximum item name size: 9pt to ensure all items fit on one page
- Line-height for item rows: 1.3–1.4 for comfortable scanning
- Letter-spacing on section titles aids hierarchy at small sizes

---

## 4. Component Styling

### Menu Item Row

The atomic unit of the menu. Always: name + weight + price on one logical row.

```
v1/v3 pattern (dots):
[Name]·············[Weight]·····[Price]
  flex row, name grows, dotted border-bottom on name span

v2 pattern (clean):
[Name] [Weight]              [Price]
  flex row, space-between, no decoration
```

**v1 / v3 implementation:**
```css
.item { display: flex; align-items: baseline; gap: 1mm; margin-bottom: 1.2mm; }
.item-name { flex: 1; border-bottom: 1px dotted <separator-color>; padding-bottom: 0.3mm; }
.item-weight { font-size: 7pt; color: <weight-color>; white-space: nowrap; }
.item-price { font-size: 9pt; font-weight: 700; color: <price-color>; white-space: nowrap; }
```

**v2 implementation:**
```css
.item { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.2mm; }
.item-name { color: rgba(255,255,255,0.85); font-size: 8pt; }
.item-weight { color: rgba(255,255,255,0.3); font-size: 6.5pt; margin-left: 1mm; }
.item-price { color: #FF6B00; font-size: 8.5pt; font-weight: 600; }
```

### Section Header

```css
/* v1 */
.section-title {
  font-size: 7.5pt; font-weight: 700; text-transform: uppercase;
  color: #FF6B00; letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(232,50,26,0.3);
  padding-bottom: 1mm; margin-bottom: 2mm; margin-top: 3mm;
}

/* v2 */
.section-title {
  font-size: 6.5pt; font-weight: 700; text-transform: uppercase;
  color: #FFFFFF; letter-spacing: 0.3em;
  margin-top: 3mm; margin-bottom: 1.5mm;
  border-top: 0.5px solid rgba(255,255,255,0.08);
  padding-top: 2mm;
}

/* v3 */
.section-title {
  font-size: 7.5pt; font-weight: 700; text-transform: uppercase;
  color: #8B1A00; letter-spacing: 0.2em;
  border-bottom: 1.5px solid rgba(196,80,26,0.5);
  padding-bottom: 1mm; margin-bottom: 2mm; margin-top: 3mm;
}
```

### Tag Pill (sauce/tincture)

Used in v1 and v3. v2 uses inline prose instead.

```css
/* v1 */
.pill {
  display: inline-block; padding: 0.8mm 2mm;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px; font-size: 7pt; color: #F0ECE4;
  margin: 0.5mm 0.5mm 0.5mm 0;
}

/* v3 */
.pill {
  display: inline-block; padding: 0.8mm 2mm;
  background: rgba(139,26,0,0.08);
  border: 1px solid rgba(139,26,0,0.2);
  border-radius: 20px; font-size: 7pt; color: #8B1A00;
  margin: 0.5mm 0.5mm 0.5mm 0;
}
```

### Empty Slot Placeholder

Two empty slots appear in БЛЮДА НА УГЛЯХ and ЗАКУСКИ columns.

```css
/* v1 */
.empty-slot {
  border: 1px dashed rgba(232,50,26,0.3); border-radius: 3px;
  color: rgba(240,236,228,0.2); font-style: italic; font-size: 7.5pt;
  text-align: center; padding: 1.5mm 2mm; margin-bottom: 1.2mm;
}

/* v2 */
.empty-slot {
  text-align: center; color: rgba(255,255,255,0.15);
  font-size: 7.5pt; letter-spacing: 0.1em;
  padding: 1mm 0; margin-bottom: 1.2mm;
}

/* v3 */
.empty-slot {
  border: 1px dashed rgba(139,26,0,0.3); border-radius: 3px;
  color: rgba(28,10,0,0.25); font-style: italic; font-size: 7.5pt;
  text-align: center; padding: 1.5mm 2mm; margin-bottom: 1.2mm;
}
```

---

## 5. Layout Principles

### Grid Structure

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER  (full width, ~18mm height)                         │
│  Restaurant name left · tagline below · URL/icon right      │
├──────────────────┬──────────────────┬───────────────────────┤
│  COL 1 (~88mm)   │  COL 2 (~88mm)   │  COL 3 (~88mm)        │
│                  │                  │                        │
│  БЛЮДА НА        │  КОМПЛЕКСЫ       │  СОУСЫ                 │
│  УГЛЯХ           │  ШАШ. В ЛАВАШЕ   │  НАПИТКИ               │
│  (+ 2 empty)     │  ШАУРМА          │  НАСТОЙКИ              │
│                  │  ЗАКУСКИ         │  ДОПОЛНИТЕЛЬНО         │
│                  │  (+ 2 empty)     │                        │
└──────────────────┴──────────────────┴───────────────────────┘
```

### Column Rules
- Three equal columns, separated by a thin vertical rule
- Column padding: 4mm horizontal, 2mm vertical
- No scrolling — all content must fit within `190mm` height
- First section in each column has no top margin (flush to column top)
- Columns are independent scroll contexts — content in col 2 is denser, so font-size may need to be tighter

### Header Rules
- Left zone: restaurant name + tagline (stacked)
- Right zone: website URL + decorative element (icon, flame, CSS shape)
- Height: ~18mm, flex-aligned center
- Background: variant-specific (dark strip for v1/v2, kraft strip for v3)

### Footer
- v1: small text strip at bottom of col 3 only
- v2: centered across full page bottom (inside 190mm constraint)
- v3: centered across full page bottom

---

## 6. Depth & Elevation

### v1 Инферно — Layered darkness

Elevation is expressed through lightness increases:
- **Level 0** — background `#0A0A0A`
- **Level 1** — column surface (implied, same color but bounded)
- **Level 2** — section titles in `#FF6B00` float above body text
- **Level 3** — price values in bold orange command highest visual weight
- **Accent** — fire gradient on restaurant name creates the peak focal point

Empty slots sit *below* normal items visually (lower opacity, italic) — they are negative space.

### v2 Уголь — Luminance contrast only

No surfaces, no fills. Hierarchy expressed purely through:
- Weight: 300 (name) → 400 (items) → 600 (prices) → 700 (sections)
- Opacity: 100% (sections) → 85% (items) → 30% (weights) → 15% (empty slots)
- Color: white → orange (prices only) → muted (everything else)

### v3 Крафт — Warm tactile layers

- **Base** — kraft paper texture `#F0E6C8` with diagonal noise
- **Header** — slightly darkened strip creates a "band" effect
- **Ink** — dark brown `#1C0A00` simulates printing on paper
- **Accent** — brick red `#8B1A00` reads as a rubber stamp or hand annotation
- **Price** — same brick red, bold — creates urgency within the warm palette

---

## 7. Guardrails

### DO
- Keep all font sizes at or below 9pt for item names; headers may go up to 22pt
- Use `pt` units for all font sizes (print media)
- Use `mm` units for all spacing and layout (print media)
- Set `print-color-adjust: exact` and `-webkit-print-color-adjust: exact` on `*`
- Ensure all content fits within `277mm × 190mm` with no overflow
- Keep empty slot placeholders visually distinct but subordinate to real items
- Use `overflow: hidden` on the body to hard-clip any overflow during print
- Test with browser print preview at A4 landscape before final output

### DON'T
- Do NOT use `px` for font sizes in print HTML
- Do NOT use external font imports (`@import url(...)`, Google Fonts) — menus must work offline
- Do NOT use JavaScript — static HTML only
- Do NOT add `box-shadow` — it often fails in print color-adjust contexts
- Do NOT use `vh`/`vw` units — they refer to screen viewport, not print area
- Do NOT exceed `9pt` for item text — it will cause content overflow on one page
- Do NOT omit any menu items or empty slots
- Do NOT use `position: fixed` or `position: sticky` — print layout is static
- Do NOT mix color schemes between variants — each must be visually independent

---

## 8. Print Considerations

### Required CSS Block (all variants)

```css
@page {
  size: A4 landscape;
  margin: 10mm;
}

@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}

body {
  width: 277mm;
  height: 190mm;
  overflow: hidden;
  margin: 0;
  padding: 0;
}
```

### Color Rendering

- Dark backgrounds (`#0A0A0A`, `#111111`) require `print-color-adjust: exact` to print — without it, browsers strip backgrounds
- Gradients on text (background-clip: text) render correctly in Chrome/Edge print; Firefox may need a fallback solid color
- Kraft paper background (`#F0E6C8`) prints naturally as a tinted fill

### Font Rendering

- System fonts (Helvetica Neue, Arial) are always available in print contexts
- Light-weight fonts (300) may print slightly heavier on physical printers — account for this in contrast ratios
- Minimum recommended print font size: 6pt (for footer/captions only)

### Page Break Handling

- All three files are single-page — no `page-break-*` rules needed
- `overflow: hidden` on body prevents content from bleeding to a second page
- If content overflows during editing, reduce `margin-bottom` on item rows first, then reduce font sizes by 0.5pt steps

### Browser Compatibility for Print

| Browser | Notes |
|---------|-------|
| Chrome/Edge | Full support for all CSS features used |
| Firefox | `background-clip: text` gradient may need `-webkit-` prefix fallback |
| Safari | Full support; test with File → Print |

---

## 9. Agent Prompt Guide

Use this section when prompting an AI agent to modify or extend these menus.

### Adding a New Menu Item

> "Add a new item to the БЛЮДА НА УГЛЯХ section in all three variants. Name: '[NAME]', weight: '[WEIGHT]г', price: '[PRICE]₽'. Replace the first empty slot placeholder. Follow the exact HTML pattern of existing item rows in each variant."

### Filling an Empty Slot

> "In menu-v1-inferno.html, replace the first `.empty-slot` div in COL1 with a real menu item. Name: '[NAME]', weight: '[WEIGHT]г', price: '[PRICE]₽'. Use the same markup structure as other items in that section."

### Changing a Price

> "Update the price of '[ITEM NAME]' from [OLD]₽ to [NEW]₽ in all three HTML variants. The price appears in the `.item-price` span of the matching row."

### Adding a New Section

> "Add a new section '[SECTION NAME]' to COL2 in all three variants, after ЗАКУСКИ. Follow the section header style of each variant. Include these items: [LIST]."

### Changing a Color Token

> "In menu-v1-inferno.html, change the section title color from `#FF6B00` to `#FFB347`. Update all occurrences of `color: #FF6B00` within `.section-title` rules only."

### Resizing for a Different Paper Format

> "Adapt menu-v2-minimal.html from A4 landscape to A3 landscape. Update `@page { size: A3 landscape }`, change body dimensions to `width: 400mm; height: 277mm`, and scale all font sizes up by 1.3× (multiply each `pt` value by 1.3 and round to nearest 0.5pt)."

### Switching to a Light Theme

> "Create a light variant of menu-v1-inferno.html. Replace `#0A0A0A` background with `#FFFFFF`, `#F0ECE4` text with `#1A1A1A`, `rgba(255,255,255,0.05)` pill backgrounds with `rgba(0,0,0,0.04)`. Keep all orange accent colors unchanged."

### Validating Completeness

> "Check that menu-v3-kraft.html contains all required menu items. The complete item list is: [paste full list]. Identify any missing items and add them to the correct sections."
