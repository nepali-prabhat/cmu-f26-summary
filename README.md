# Fall 2026 Timeline

A one-page semester dashboard for three Fall 2026 courses — merges three separate course schedules into a single visual timeline, a weekly workload chart, and a checkable task list, so there's no need to cross-reference three different Canvas pages.

![The same page split diagonally — light theme upper left, dark theme lower right](screenshot.png)

## Features

- **Day-by-day timeline** — every class, release, due date, exam, and event across all three courses on one scrollable SVG chart, with a "this week" marker and a dotted line for today.
- **Weekly workload chart** — a stacked bar per week counting due dates and exams (release dates and class sessions aren't counted as workload), with exam/quiz markers on top. Click a bar to jump to that week.
- **Week panel** — the current week's tasks with checkboxes and free-text notes that save automatically. Checking a task off also marks its matching pin in the timeline with a checkmark.
- **Missing-start-date flag** — any task with only a due date and no known release or window-open date is called out with a badge in the week panel and a distinct dashed ring on its timeline pin, so it doesn't read as more certain than it is.
- **Course policy cards** — late-day, grading, and AI-use policy per course behind a tab per course, transcribed from each syllabus with a source and date.
- **Plain-list fallback view** — every date in one sortable, screen-reader-friendly table.
- **Copy folder path** — one click to copy a course's local folder path (paste into Finder's Go to Folder).
- **Light/dark theme**, keyboard focus states, and `prefers-reduced-motion` support throughout.

## Look

The page runs on the "Classical" design system — its spacing, radius, shadow and component classes — with the palette revised to Catppuccin and the type set in Instrument Sans, with JetBrains Mono reserved for figures: dates, counts and percentages.

**Catppuccin Mocha is the theme** and the page opens in it: `--color-accent` Mauve `#cba6f7`, with Blue / Maroon / Teal as the three course inks. Secondary text sits one rung above stock Mocha — `--ink-faint` is Subtext0 rather than Overlay2, and `--ink-soft` is Text — because Overlay2 measured only 4.45:1 against `--surface-2` and carries most of the 9–11px figures.

**The grounds are green, not Mocha's blue-violet.** Every rung of Mocha's neutral ramp sits at hue 272–284° in OKLCH, which read too blue here, so the whole neutral family — grounds, surfaces, lines and text — is rotated to **hue 150** with lightness and chroma untouched. Same rungs, same contrast (text/bg 12.2:1, `--ink-faint`/`--surface-2` 5.6:1), green cast; and ~30° off the teal course ink, so the lanes stay distinct. `--color-bg` is `#111d13`, `--surface` `#152418`, `--color-text` `#c4dfc9`. **The accent and course inks are not rotated** — those stay pure Mocha.

The toggle's other half is **a deliberate hybrid, not stock Latte**: Latte's neutral grounds carrying Mocha's *pastel* accent and course inks, because Latte's own accents (`#8839ef`, `#1e66f5`, `#d20f39`) read harsh and saturated rather than pastel. Don't "correct" light mode back to Latte accents. Latte's grounds get the same hue-150 rotation, giving a sage page (`#e5ebe6` / `#eef2ef` / `#405845`).

The tradeoff that comes with it: those pastels are light-on-light in the light theme, so they hold only as **large fills** — strip bars, dots, chart marks, progress tracks. Anywhere `var(--course)` sets small **text** (`.lr-code` at 13.5px, `.drawer-course-head`, `.policy-head .code`, `.pol-tab.is-active`) the rule is `var(--course-ink, var(--course))` instead: the same Mocha hue walked down in OKLCH until it clears 4.5:1 on `--surface`. The JS sets `--course-ink` beside every `--course`. If you add course-colored text, use `--course-ink` — don't reuse the raw pastel. Mocha Yellow gets the same treatment for exam marks, since `#f9e2af` is 1.3:1 on the light ground.

Theme choice persists in `localStorage` under `fall2026-theme-ctp2`.

Type is Instrument Sans throughout with JetBrains Mono for small figures (`--font-figure`). Hierarchy comes from size and weight only — no horizontal rules under headings; that was removed deliberately.

All of it is inlined in the single `<style>` block at the top of `index.html`, in four layers: the design-system tokens, the timeline's component skin, the Catppuccin palette layer, then this page's layout. Retune the look from the `:root` variables rather than by patching individual rules.

**Debug swatches.** Hovering the palette dot in the bottom-right corner opens a panel that reassigns a ground variable — page, surface, surface-2 or line — to any rung of the ground ramp, live. Only the neutrals are offered: the accent hues are pastels meant to sit *on* a ground, not to be one. The swatches carry the hue-150 rotation too, and keep the Mocha rung names (crust → overlay2) as labels. Picks persist until Reset, and are written as an inline style on `<html>`, so they override both themes.

## Running it

It's a static file — open `index.html` directly, or serve it locally:

```
python3 server.py
```

then open http://localhost:8000/index.html. This also persists checkbox/note state to a local SQLite file (`state.db`) so it survives across browsers, not just one browser's `localStorage`. Opening `index.html` directly (no server) still works — it just falls back to `localStorage` only.

## Updating the schedule

All schedule data (dates, lecture topics, assignment names, exam dates) lives in the `viz-data` JSON block embedded in `index.html`; the syllabus policy text lives in the `window.POLICIES` array just below it. It's transcribed by hand from each course's syllabus/schedule PDFs and Canvas assignments page, so it goes stale if a syllabus is amended — always double check anything that actually matters against Canvas or the instructor.
