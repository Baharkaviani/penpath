# Penpath DESIGN.md

> Plan on paper. Track digitally. — Design system for the Vue app.

Inspired by the [DESIGN.md pattern](https://github.com/VoltAgent/awesome-design-md) (Google Stitch). Styles live in `src/styles/penpath.css`.

---

## 1. Visual Theme & Atmosphere

**Mood:** Calm focus — analog warmth meets precise digital tracking. Not gamified chaos; disciplined, journal-like clarity with subtle celebration for wins.

**Philosophy:**
- The **flowboard** should feel like the printed A4 sheet: ink-blue structure, ruled lines, circle trackers.
- The **app shell** (dashboard, badges, scan) uses the same ink palette on soft paper-white and mist surfaces — one brand, two modes (sheet vs. chrome).
- Whitespace is generous; data is scannable; badges add color only as accent jewels.

**Density:** Medium — tables and stats are information-rich but never cramped.

---

## 2. Color Palette & Roles

| Token | Hex | Role |
|-------|-----|------|
| `--ink` | `#142A69` | Primary text, headings, table headers (from flowboard LaTeX) |
| `--ink-muted` | `#142A6999` | Secondary labels |
| `--paper` | `#FAFBFE` | Page background (app) |
| `--paper-sheet` | `#FFFFFF` | Flowboard sheet surface |
| `--head-bg` | `#E8EDFC` | Table header row background |
| `--line` | `#BEBEBE` | Table borders |
| `--rule` | `#AFAFAF` | Ruled lines, placeholders |
| `--ring` | `#878787` | Tracker circle strokes |
| `--mist` | `#F0F3FA` | Card backgrounds |
| `--success` | `#1B7D5A` | Win state, positive trend |
| `--warning` | `#C47A12` | Near-threshold (70–79%) |
| `--danger` | `#B83A3A` | Loss week, streak break |
| `--badge-seed` | `#2BB8C4` | Week 1 crystal |
| `--badge-flame` | `#E8A020` | Week 2 crystal |
| `--badge-garden` | `#2EAD6E` | Week 3 crystal |
| `--badge-gem` | `#9B7FD4` | Week 4 crystal |
| `--badge-crown` | `#D4AF37` | Crown milestone |
| `--badge-phoenix` | `#E85D3A` | Recovery badge |

---

## 3. Typography

Based on [WIRED (getdesign.md)](https://getdesign.md/wired/design-md): serif for narrative, sans for structure, mono for table kickers.

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Display | Playfair Display | 2rem–2.75rem | 400–700 |
| Lead / intro | Lora | 1–1.125rem | 400 |
| UI, body, buttons | Inter | 0.875–0.9375rem | 400 / 700 |
| Table headers | IBM Plex Mono | 0.7rem | 500, uppercase |
| Stat value | Inter | 1.75rem–2.25rem | 700, tabular-nums |

**Google Fonts:** loaded in `index.html`.

---

## 4. Component Stylings

### Buttons
- **Primary:** `--ink` fill, white text, 8px radius.
- **Secondary:** white fill, `--ink` border 1.5px.
- **Ghost:** transparent, `--ink-muted` text, hover `--mist` bg.

### Flowboard table
- Header row: `--head-bg`, `--ink` labels.
- Tracker circles: 18px diameter, `--ring` stroke; filled = `--ink` bg.

### FLAME rating
- 5 circles per row, numbered 1–5; selected = `--ink` fill.

---

## 5. Layout Principles

- **Max content width:** 1200px app; flowboard sheet max 1100px centered.
- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48px.

---

## 6. Dark mode

Applied via `data-theme="dark"` on `<html>`. Toggle: Light / Dark / System. Persisted as `penpath-theme` in `localStorage`.

| Token | Light | Dark |
|-------|-------|------|
| `--ink` | `#142A69` | `#E8EDFC` |
| `--ink-muted` | `rgba(20,42,105,0.65)` | `rgba(232,237,252,0.65)` |
| `--paper` | `#FAFBFE` | `#0F1419` |
| `--paper-sheet` | `#FFFFFF` | `#1A2332` |
| `--head-bg` | `#E8EDFC` | `#243352` |
| `--mist` | `#F0F3FA` | `#151D2B` |
| `--line` | `#BEBEBE` | `#3A4558` |
| `--rule` | `#AFAFAF` | `#4A5568` |
| `--ring` | `#878787` | `#6B7A94` |
| `--stat-icon-bg` | `#E8EDFC` | `#1A2744` |
| `--stat-icon-color` | `#142A69` | `#7B9AE8` |

**Rules:** Badge streak discs stay `#000000`. Print/PDF export always uses light sheet tokens.

---

## 7. Vue routes (UI map)

| Route | View |
|-------|------|
| `/` | Home — hub + How Penpath works |
| `/dashboard` | Stats, chart, FLAME, streak, quick actions |
| `/flowboard` | Current week sheet |
| `/flowboard/:weekId` | Archived week (read-only) |
| `/badges` | Badge rules & collection |
| `/scan` | Upload / OCR flow |
| `/history` | Week list → flowboard archive |
