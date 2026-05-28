# Dashboard Portal Consolidation Design

**Date:** 2026-05-28
**Repo:** maplemoon-dashboard
**Branch:** feature/portal-consolidation (to be created from current `main`)
**Owner:** Nate (HandToMouse)
**Predecessor:** `2026-05-28-dashboard-cleanup-billing-merge-design.md` (Phase 01)
**Status:** Draft, awaiting Nate's spec review

---

## Goal

Reshape the dashboard's 12-tab nav into a real client portal for Carli and Dylan. Phase 01 solved data drift, em-dash hygiene, responsive break-points, and added the Billing tab. It did NOT retire or consolidate any tab; it added one. The dashboard still presents as a developer's swiss-army-knife layout. Phase 02 makes it a client portal.

## Audience

Carli and Dylan at MapleMoon (shared inbox `info@maplemoon.com.au`). They need clear answers to:

1. What's being worked on?
2. What's owed and when?
3. What's done and where do I find it?
4. Where do I look up old reference material (proposals, research, forms)?

The current 12-tab nav buries answers to (1) and (3) under a wall of historical, half-superseded surfaces. Question (4) has no organized answer at all.

## Architecture decision: 5-tab Lifecycle + visible Archive (Proposal B)

Five surviving tabs in the nav. One of them (Archive) is a curated index of historical artifacts. Nothing is hidden behind raw URLs; everything is one click from somewhere visible.

### Final tab inventory

| Pos | Tab | DOM id | Composition |
|-----|-----|--------|-------------|
| 1 | Status | `tracker-tab` (renamed) | Project Tracker kanban + new "This week" hook (top) + Assets status (folded inline, below kanban) |
| 2 | Billing | `billing-tab` | Kept as built in Phase 01. Adds footer cross-link to Archive#quote. |
| 3 | Specs | `specs-tab` (renamed) | Existing Spec Tracker + new SKU and barcode reference table (top) for manufacturer-share |
| 4 | Final Files | `files-tab` | Kept as-is |
| 5 | Archive | `archive-tab` (NEW) | Card grid linking to 8 historical artifacts retained in HTML but hidden from nav |

### Retired from nav (HTML retained, reachable via Archive)

| Was | DOM id stays | Reachable via |
|-----|---------------|---------------|
| Quote and Invoice | `quote-tab` | Archive card + Billing footer cross-link |
| Project Tracker (renamed to Status) | `tracker-tab` | Still in nav as Status (renamed only) |
| Spec Tracker (renamed to Specs) | `specs-tab` | Still in nav as Specs (renamed only) |
| Timeline (full 1834 lines) | `timeline-tab` | Archive card; condensed milestones surface via Status's "This week" hook |
| Assets and Specs | `assets-tab` | Folded inline into Status. Tab div retained for future re-promotion if needed. |
| E-Commerce Proposal | `ecommerce-tab` | Archive card only |
| Photoshoot Guide | `photoshoot-tab` | Archive card only |
| Shopify Research | `research-tab` | Archive card only |
| Theme Preview | `preview-tab` | Archive card only |
| Client Form | `clientform-tab` | Archive card with "if you already submitted, this is historical" footnote |
| Design Review (external link) | `review/` subfolder | Archive card with "last current as of" date |

### Why retain HTML for retired tabs instead of deleting

1. **Lowest risk.** If Carli or Dylan ever ask "what happened to that Shopify proposal?", we re-promote a tab back to nav by un-hiding one button. Hard-delete forecloses that.
2. **Atomic commits stay small.** We move buttons and add Archive. We do not surgery 4000 lines of HTML.
3. **Page-load impact is minimal.** The static HTML is already cached after first load; the retired divs are display-none until reached via Archive click.

If file-size becomes a concern later, a follow-up phase can hard-split archive content into separate static HTML pages. Out of scope here.

## Architecture: Archive tab

Archive renders as a 2-column responsive grid of section cards (single column at <600px). Each card:

- **Title** (e.g., "Shopify E-Commerce Proposal")
- **Subtitle** (one-line context, e.g., "Feb 2026 proposal, approved 17 Feb")
- **Body** (2-3 lines: what this is, why it's archived, where current state lives)
- **Footer:** "Last current as of: `<date>`" + a "View" button

The "View" button calls `switchTab('<id>', event)` (the same function the surviving tabs use), which brings the existing hidden tab content into the visible content area. The tab nav highlighting is suppressed for archived tabs (no button to highlight). A breadcrumb "← Back to Archive" appears at the top of each archived tab content area when arrived from Archive.

### Archive cards (8)

1. **Original Quote and Invoice** - AFQA pricing breakdown. Superseded by Billing as source of truth. Last current: 2026-02-18.
2. **E-Commerce Proposal** - Feb 2026 Shopify pitch. Approved 17 Feb 2026. Superseded by live build at `~/maplemoon-website`. Last current: 2026-02-17.
3. **Shopify Research** - Pre-build research deck (platform, theme stack, competitive intel). One-shot reference, build now in flight. Last current: 2026-02 (estimate).
4. **Theme Preview** - Pre-build theme A/B preview. Superseded by live website staging. Last current: 2026-02 (estimate).
5. **Client Form** - Intake form for Shopify project. Pre-filled with MapleMoon defaults; if already submitted to Nate separately this is historical, if not please complete and email `info@`. Last current: 2026-02 (estimate).
6. **Photoshoot Guide** - Shot manifest for the 24 May 2026 Shopify shoot (iframe to `mm-photoshoot-guide.vercel.app`). Retrospective reference. Last current: 2026-05-24.
7. **Design Review** - External link to `review/` subfolder. Screenshots may be stale post-website-refresh; refresh is a separate follow-up. Last current: pre-refresh date (TBD by Nate during review).
8. **Full Timeline** - Original week-by-week timeline (1834 lines). Condensed into Status's "This week" hook (10-row milestones). Last current: ongoing.

Card copy: hand-curated for this spec, pre-flight em-dash sweep before commit.

## Architecture: Status tab "This week" hook

A compact 3-card section at the top of Status (above the existing kanban) reads from a new `data/milestones.json`. Each card shows:

- Status pill (done / in-progress / upcoming)
- Title
- Date
- One-line context

The full 10-milestone set lives in `data/milestones.json`; Status surfaces only the 3 most-relevant by date (last completed + next 2 upcoming, or next 3 upcoming if all upcoming). The Archive's "Full Timeline" card link still goes to the verbatim 1834-line `#timeline-tab` for historical detail.

### milestones.json structure

```json
{
  "lastUpdated": "2026-05-28T17:00:00+10:00",
  "milestones": [
    {
      "date": "2026-05-24",
      "title": "Shopify photoshoot completed",
      "status": "done",
      "context": "Carli, Dylan, Mitch, Melly. 122-shot Shopify mapping captured."
    },
    {
      "date": "2026-06-XX",
      "title": "Direction A live website review",
      "status": "in_progress",
      "context": "Carli and Dylan review staging build at ~/maplemoon-website Direction A."
    }
    // 10 total, Nate curates during spec review
  ]
}
```

## Architecture: Status tab Assets fold-in

The existing `#assets-tab` content is JSON-populated by an existing render function. The fold-in:

1. Adds a new `<section id="status-assets">` block at the bottom of `#tracker-tab`
2. Re-uses the existing assets render function, retargeting it to the new section
3. The original `#assets-tab` div is retained but hidden from nav (no Archive card; it's a compact list, redundancy with Status would not add value)

If the existing render function is tightly coupled to `#assets-tab` selectors, the implementation either parameterizes the target selector or duplicates a small render block (decision deferred to execute phase based on the existing code shape).

## Architecture: Specs tab SKU and barcode reference

A compact table at the top of `#specs-tab` listing all production SKUs with their codes and barcodes. Drives Carli and Dylan's manufacturer-share comms (Custom Queen and any future production partner needs codes, not artwork specs).

Columns: Product, SKU code, Barcode, Status, Notes.

Source: real values extracted from `data/project_status.json` `products[].checklist` entries. No fabricated values.

Scope note: artwork bleed, safe-area, and dimension values live in external spec sheets / Illustrator files, not in dashboard data. A future phase can add an artwork-dimensions table if Carli and Dylan ask for it; current scope is SKU and barcode codes only.

## Architecture: Billing footer cross-link

A single `<p>` at the bottom of the AFQA section in `#billing-tab`:

> See the original quote and invoice rationale → **View in Archive**

Click handler: `switchTab('quote', event)` (same as Archive's quote card), scrolling to the top of `#quote-tab`. A breadcrumb "← Back to Billing" appears at the top of `#quote-tab` when arrived from Billing.

## Data flow

```
data/project_status.json     -> Status (kanban), Specs (existing + dimensions)    [unchanged structurally]
data/billing.json            -> Billing                                             [unchanged]
data/milestones.json         -> Status "This week" hook                             [NEW]
data/archive_index.json      -> Archive cards                                       [NEW]

Retired-but-retained tab divs: quote, ecommerce, photoshoot, research, preview,
clientform, assets, timeline. All reachable via Archive's switchTab('<id>') call.
```

## Components

### W1. Data scaffolding (new files)

- `data/archive_index.json`: 8 cards, hand-curated
- `data/milestones.json`: 10 milestones, Nate-curated during spec review or execute phase

### W2. Archive tab

- New `<div id="archive-tab" class="tab-content">` inserted before `</div>` closing `.container` (placement after the last existing tab div)
- New nav button after Final Files
- Inline JS function `renderArchiveCards()` reads `data/archive_index.json`, builds cards
- Each card's "View" button uses the existing `switchTab` to bring historical content into view
- "Back to Archive" breadcrumb injected at top of any archived tab when arrived via Archive (tracked via a `data-from-archive` attribute or sessionStorage flag)

### W3. Nav restructure

- Remove buttons (7): Quote, E-Commerce, Photoshoot, Shopify Research, Theme Preview, Client Form, Design Review
- Rename (2): Project Tracker → Status; Spec Tracker → Specs
- Add (1): Archive
- Result: 5 buttons (Status, Billing, Specs, Final Files, Archive)
- DOM ids unchanged; only button text, icons, and aria-controls bindings updated where needed

### W4. Status enhancements

- New `<section id="status-this-week">` at top of `#tracker-tab`
- JS reads `data/milestones.json`, renders 3 cards (filter: last done + next 2 upcoming, fallback to next 3)
- New `<section id="status-assets">` at bottom of `#tracker-tab`
- Re-uses or parameterizes the existing assets render

### W5. Specs SKU and barcode reference

- New `<section id="specs-codes">` at top of `#specs-tab`
- Hand-coded table extracted from `data/project_status.json` `products[].checklist` entries
- Columns: Product / SKU code / Barcode / Status / Notes
- 16 rows: 6 Bar CDUs, 6 Moon CDUs, Banana 4-pack, Banana CDU, 2 Elixirs (SKU-only)

### W6. Billing footer cross-link

- New `<p>` inside the AFQA section block of `#billing-tab`
- onclick: `switchTab('quote', event)` plus optional sessionStorage flag for "from billing" breadcrumb

### W7. Back-to-source breadcrumbs

- Inject a `<div class="back-link">` at the top of `#quote-tab` and the 7 archived tab divs when arrived via Archive or Billing cross-link
- Implementation: a single sessionStorage flag `mm:returnTo` set by the caller, read by a global init hook on tab switch


### W8. Small visual refresh on the 5 surviving tabs

Targets Nate's "outdated styling" concern without becoming a redesign. Scope is surgical: typography hierarchy, spacing rationalisation, hero anchor, and stale page-title cleanup. Palette stays locked (no cornflower migration).

**What this changes:**

1. **Hero page-title cleanup.** Replace the hardcoded `<h1>Project Portal - Updated Feb 2026</h1>` (still live and stale-dated) with `<h1>MapleMoon Project Portal</h1>`. The "Updated N days ago (Mmm DD, YYYY)" staleness pill below it already carries the freshness signal; the date in the H1 is redundant and rots.
2. **Typography scale.** Apply consistent type rhythm across the 5 surviving tabs:
   - H1 (page anchor): 2rem / 700 weight, Crimson Text serif, `var(--mm-dark-blue)`
   - H2 (section header): 1.5rem / 600 weight, Inter sans, `var(--mm-deep-blue)`
   - H3 (subsection): 1.15rem / 600 weight, Inter sans, `var(--mm-dark-blue)`
   - Body: 1rem / 400 weight (bumped from 0.95rem to hit WCAG 16px ideal)
   - Labels / pills: 0.78rem / 600 weight, uppercase
   - Apply via explicit CSS rules on `.tab-content h1`, `.tab-content h2`, `.tab-content h3`, `.tab-content p`. Override inline `style="..."` attributes on h2/h3 where present.
3. **Spacing rationalisation.** Standardise across the 5 surviving tabs:
   - Section gap (between major blocks within a tab): 32px
   - Card padding (inside `.financial-card`, `.billing-section`, equivalent): 24px (desktop), 16px (mobile)
   - Inline element gap (between header items, money rows): 16px
   - Apply via existing class selectors. Where ad-hoc inline `style="margin: ..."` is in use, remove the inline style in favour of class rules.
4. **Tab nav active-state colour audit.** Current active tab uses a pink/coral accent (`#D4A574` per the existing CSS). This is off-brand from the locked `--mm-*` palette. Two options the executor evaluates and surfaces for Nate's pick BEFORE applying:
   - (a) Keep `#D4A574` as-is (the accent is intentional brand spice)
   - (b) Swap to `var(--mm-deep-blue)` for consistency with the rest of the palette
   - Default: surface to Nate, do not unilaterally change.

**What this does NOT change:**

- Palette stays locked: no cornflower `#7B9DBF` migration
- No card-grid restructure beyond spacing normalisation
- No icon swaps in the tab nav or section headers
- No new fonts loaded
- No animation or transition changes
- No retired-tab content edits (those tabs stay hidden, untouched)

**Files touched:** `index.html` only (CSS block at the top, inline style attribute cleanups throughout the 5 surviving tab divs).

**Verification:** All 5 surviving tabs render with the new type rhythm at 1440 / 768 / 480 / 375px. No JS console errors. Manual visual sweep confirms the dashboard reads tighter without changing what content is shown.

## Error handling

- **Archive card click with missing target id:** `console.warn` plus a small inline error in the Archive card ("Target content unavailable. Refresh the page.")
- **milestones.json fetch failure:** Status's "This week" section is hidden cleanly; kanban below renders normally
- **archive_index.json fetch failure:** Archive tab shows "Reference data not loaded. Refresh the page or contact Nate."

No retries, no exponential backoff. These are static JSON in the same origin; if they fail, the network is down and retry won't help.

## Testing

Visual verification at:

- 1440px desktop (primary)
- 768px tablet
- 480px mobile
- 375px iPhone SE

For each viewport, confirm:

1. Tab nav fits without overflow (currently overflows even at 1440px)
2. All 5 nav buttons render and switch correctly
3. Status's "This week" cards render with the 3 most-relevant milestones
4. Status's Assets section renders below the kanban with the same data as the old Assets tab
5. Specs's SKU and barcode reference table renders at top, existing tracker below
6. Billing footer cross-link to Archive#quote works (lands on Quote tab with breadcrumb)
7. Archive renders 8 cards, each "View" button brings the correct historical content into view
8. Archive's "Back to Archive" breadcrumb appears on archived tab arrival, returns correctly
9. No JS console errors on tab switch
10. No em-dashes in any Archive card copy or new Status / Specs copy

## Out of scope

- `~/maplemoon-website` repo (separate Shopify build; touched read-only)
- Vercel deploy (Nate ships manually after review)
- Cornflower palette migration (separate decision tree)
- Hard-deletion of any retired tab content (deferred indefinitely; if file size becomes an issue, separate phase)
- Email or iMessage to Carli and Dylan announcing the restructure (separate comms decision)
- Any `CLAUDE.md` or memory file modifications
- Refreshing `review/` screenshots (separate follow-up; Archive card surfaces staleness via "last current as of")
- INV-0406 or any invoice work (already authorised in Phase 01 closeout)

## Open questions / caveats

1. **Client Form true state.** The form is "Download Responses" (client-side, no backend). Pre-fills are Nate's MapleMoon best guesses; radios are blank. Whether Carli has already sent her responses separately to Nate is outside-the-repo state. Archive card includes a footnote covering both possibilities. Nate can adjust the copy during spec review.

2. **Timeline 10-milestone curation.** RESOLVED. Curated during spec review (2026-05-28). 10 milestones inlined in plan T1. Items 8-10 have "(target)" qualifier on upcoming dates; Nate can firm up before T1 ships.

3. **Design Review screenshot freshness.** Linkable from Archive, but screenshots may be stale post-website-refresh. Archive card shows "last current as of" so Carli sees freshness at a glance. Refresh deferred to follow-up.

4. **Specs reference scope.** RESOLVED. Pivoted from artwork dimensions to SKU and barcode reference (data we actually have anchored in `project_status.json`). Artwork dimensions live in external spec sheets / Illustrator files; future phase can add an artwork-dimensions table if Carli and Dylan request it.

5. **Phase 01 caveats still open.** Per parent session handoff: website `line_items` weights are unvalidated placeholder estimates; 375px responsive added but not visually verified. Both surface in Phase 02 execute QA if they touch any surviving tab.

## Success criteria

- Tab nav has 5 buttons (Status, Billing, Specs, Final Files, Archive) in this order
- Nav fits without horizontal overflow at 1440px desktop
- Nav scrolls cleanly at 375px mobile (Phase 01 scroll-snap behavior preserved)
- All 8 historical artifacts reachable from Archive in one click, with correct breadcrumb on return
- Billing tab cross-links to Archive#quote with breadcrumb
- Status tab shows "This week" hook with up to 3 milestones and folded Assets section
- Specs tab shows SKU and barcode reference table above the existing tracker
- No regressions in Billing tab (`billing.json` still loads and renders three sections correctly)
- No em-dashes in any client-visible copy
- All commits on `feature/portal-consolidation`; merged to `main` via 4 PRs (one per logical commit cluster); no Vercel auto-deploy triggered from CLI

## Implementation plan

See `.planning/phases/02-portal-consolidation/02-PLAN.md` for the GSD task breakdown with atomic-commit boundaries and verification steps.
