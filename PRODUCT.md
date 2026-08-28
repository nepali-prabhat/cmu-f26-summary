# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

`index.html` is still a single static file (inline CSS and vanilla JS, no build step, no framework) — keep it a file that can be opened or edited directly, not restructured into a build pipeline. It now has an optional companion: `server.py`, a stdlib-only Python script (`http.server` + `sqlite3`) that serves the file and exposes a `GET`/`POST /api/state` endpoint backed by a local `state.db` SQLite file, so checkbox/note progress survives across browsers and machines rather than living in one browser's `localStorage`. `localStorage` remains as an instant-load cache and as the fallback when the page is opened without `server.py` running (e.g. as a plain `file://` page). Keep this persistence layer equally simple: one row, one JSON blob — no ORM, no schema migrations, no new dependencies.

## Users

A single user: the site owner, a CMU student, planning their own Fall 2026 semester. Not built for classmates or any other audience — content, tone, and UI can assume exactly one reader who already knows their own courses and situation.

## Product Purpose

Give the owner one page that answers "what's happening and what's due, across all four of my courses, this semester" — merging four separate course schedules (lectures, releases, due dates, exams) into a single visual timeline, a per-week workload view, and a checkable task list with personal notes, so they don't have to cross-reference four different Canvas pages/syllabi.

## Positioning

A personal semester dashboard purpose-built for this exact course load (15-440, 14-642, 15-618, 14-757), not a generic student planner — the data model, policy text, and folder paths are specific to these four syllabi and this student's own file layout.

## Operating Context

- Checked at a desktop browser, most likely opened as a local file or from a personal repo — not phone-first.
- Source data (lecture topics, release/due dates, exam dates) comes from each course's syllabus/schedule PDFs and Canvas assignment pages, transcribed by hand into the embedded `viz-data` JSON — it goes stale if a syllabus is amended and isn't automatically synced.
- The owner cross-references this page against Canvas/instructor announcements for anything that actually matters (e.g. late-day usage, TBD dates) rather than treating it as the system of record.

## Capabilities and Constraints

- Four courses currently tracked, each with a color identity (`--c-ds`, `--c-es`, `--c-pa`, `--c-ml`) already established in the visual system: `15-440` Distributed Systems, `14-642` Embedded Systems, `15-618` Parallel Computer Architecture, `14-757` ML with Adversaries in Mind.
- Day-by-day SVG timeline (classes, releases, due dates, exams, events) with course/type toggle filters and a "this week" indicator.
- Weekly workload chart (stacked bar of due dates + exams per week, diamond markers for exams).
- Week panel: click a week to see its tasks with checkboxes and free-text notes.
- Course policy cards: late-day policy, grading breakdown, and AI-use policy per course, each sourced/dated.
- Plain-list fallback view (sortable-by-eye table) for screen-reader/accessibility use.
- A "copy folder path" affordance per course, since a browser page can't open Finder directly — pastes into Finder's Go to Folder.
- Checkbox/note state persists to a local SQLite file (`state.db`) via `server.py`'s `/api/state` endpoint, with `localStorage` as an instant-load cache and offline/no-server fallback. Nothing leaves the machine — no analytics, no tracking, no external network calls.

## Evidence on Hand

- Full Fall 2026 schedule data for all four courses is already embedded in `index.html`'s `viz-data` JSON (dates, lecture topics, assignment names/points, exam dates) — treat this as real, current data, not a placeholder to replace.
- Course policy text (late days, grading, AI policy) is transcribed from each course's actual syllabus, with source/date noted per card (e.g. "PDF syllabus, uploaded Aug 25, 2026"). Do not invent or alter policy content — only the presentation.
- Semester bounds: Aug 24 – Dec 13, 2026, including named breaks (Labor Day, Fall Break, Democracy Day, Thanksgiving).

## Product Principles

- One page, one reader: optimize for the owner's own workflow and vocabulary, not for a general audience.
- The data is real and already correct — visual/UX work should make it easier to scan and act on, never fabricate or approximate schedule facts.
- Minimal infrastructure: the page still works standalone via `localStorage`; `server.py` + SQLite is an optional, stdlib-only local layer for persistence across browsers, not a hosted service.
- Desktop-first: the primary reading context is a browser window at a computer, not a phone.
- When in doubt about a date or policy, defer to Canvas/the instructor — this page is a convenience layer, not the source of truth.

## Accessibility & Inclusion

No specific standard was required, but the existing implementation already invests in this (`role="img"` + `aria-label` on both SVG charts, `aria-live` tooltip, focus-visible outlines, `prefers-reduced-motion` handling, and a plain-list fallback table described as "screen-reader friendly"). Preserve these as a baseline rather than only decorative parity.
