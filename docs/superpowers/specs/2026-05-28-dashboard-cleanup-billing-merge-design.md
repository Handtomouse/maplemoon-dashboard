# Dashboard Cleanup + Billing Merge Design

**Date:** 2026-05-28
**Repo:** maplemoon-dashboard
**Branch:** feature/dashboard-cleanup-billing-merge
**Owner:** Nate (HandToMouse)
**Status:** Draft, awaiting review

---

## Goal

Clean up cruft accumulated across 20+ commits on `~/maplemoon-dashboard`, consolidate scattered data sources, and add a new Billing tab that surfaces AFQA work, Shopify website progress, and the photoshoot scope with mates-rate-aware display. Ship as a single PR-style diff against `main`, no auto-deploy.

## Scope

In scope:

- W1 polish on existing tabs: em-dash sweep, broken staleness display, tab nav overflow, 375px responsive add
- W2 data consolidation: collapse 4 pricing markdowns down to 1 canonical, archive the older drafts
- W3 new Billing tab inside `index.html` with three sections: AFQA Retrospective, Website Progress, Photoshoot
- W3 supporting data: new `data/billing.json` (hand-curated, static)
- Verification at desktop 1440px, tablet 768px, mobile 480px and 375px

Out of scope (do not touch in this SPIN):

- `~/maplemoon-website` repo (separate Shopify build, separate decision tree)
- Xero billing logic or live API integration
- Photoshoot deliverables folder
- Any CLAUDE.md / memory file modifications
- Vercel deployment (Nate ships this manually after review)
- Drafting or sending any invoice (INV C21_MM_07 stays with parent session)

## Architecture

### Choice: W3a, new tab inside `index.html`

The dashboard is a single static HTML file with 11 tabs already. Adding a 12th tab named "Billing" between "Quote and Invoice" and "Final Files" matches the existing pattern, requires zero new infrastructure, and ships in one Vercel static deploy.

Rejected alternatives:

- W3b (sibling file `billing.html` linked from tab nav): forces a second page load for Carli and Dylan, duplicates header and palette
- W3c (canonical receipt-builder at `~/UFC/tools/receipt_builder/`): couples client experience to an HTM-internal tool URL, makes future client-specific changes harder

### Data flow

```
project_status.json  -> AFQA tab rendering (existing, unchanged structurally)
billing.json (new)   -> Billing tab rendering (new)
                          + reused JSON timestamp for hero staleness display
```

The Billing tab JS reads `data/billing.json` at page load, builds three sections from three top-level keys: `afqa_retrospective`, `website_progress`, `photoshoot`. Each section renders into a dedicated DOM root inside `<div id="billing-tab" class="tab-content">`.

## Components

### W1.1 Em-dash sweep

- Target: 88 em-dashes in visible-copy lines (`grep -n "—" index.html | grep -vE '<!--|//'`)
- Replacement rule: replace with hyphen-space, sentence break, or comma per sentence context. Default to hyphen-space if ambiguous.
- Exclusions: HTML comments, JS comments, CSS, copyright/license headers
- Method: line-by-line review via Edit tool, not bulk sed (mass-substitution risks breaking inline `style="font: 1px solid"`-style attributes that contain `--` CSS variables)

### W1.2 Staleness display fix

Current bug: `initDynamicDate()` at `index.html:5432-5442` reads `data-updated` attribute from `#last-updated-text`. That attribute is hard-coded HTML containing `2026-02-11`, but `data/project_status.json.lastUpdated` is `2026-02-18`. Two truth sources drifted.

Fix: `initDynamicDate()` reads from `project_status.json.lastUpdated` via the existing JSON fetch at init time. Remove the hard-coded `data-updated` attribute. Single source of truth.

### W1.3 Tab nav overflow

Current behavior at 1404px viewport: tabs 9, 10, 11 (`Shopify Research`, `Theme Preview`, `Client Form`) are clipped off the right edge. The Design Review link is also clipped.

Fix: add `overflow-x: auto` and `scroll-snap-type: x mandatory` to `.tab-navigation`. Tab buttons get `scroll-snap-align: start` and `flex-shrink: 0`. Add a subtle right-edge gradient cue so users can see content is scrollable.

### W1.4 375px responsive

Existing media queries: `@media (max-width: 768px)` and `@media (max-width: 480px)`. No 375px-specific. Most layouts collapse correctly at 480px so 375px usually inherits cleanly, but tab nav and the Complete Financial Overview cards need verification.

Add: one new `@media (max-width: 375px)` block addressing only the cases that visibly break (to be enumerated during execute phase from visual verification, not pre-listed here).

### W2 Data consolidation

- `FINAL_PRICING_BREAKDOWN.md` becomes the canonical AFQA pricing source (already the most current at $10,029.28)
- `PRICING_CALCULATIONS.md` moves to `_archive/PRICING_CALCULATIONS.md` with a top banner: `> ARCHIVED 2026-05-28. See FINAL_PRICING_BREAKDOWN.md for current pricing.`
- `REVISED_PRICING.md` moves to `_archive/REVISED_PRICING.md` with the same banner
- `README.md` stays, updated to point at the canonical pricing source
- `DEPLOYMENT.md` stays (operational doc, separate concern)
- `data/project_status.json` stays as canonical for AFQA product state (unchanged structurally in this SPIN)

### W3.1 Billing tab structure

```
<button class="tab-button" ... onclick="switchTab('billing', event)">
  <i class="fas fa-receipt"></i> Billing
</button>

<div id="billing-tab" class="tab-content" role="tabpanel">
  <section id="billing-afqa">...</section>
  <section id="billing-website">...</section>
  <section id="billing-photoshoot">...</section>
</div>
```

### W3.2 Billing data model

`data/billing.json`:

```json
{
  "lastUpdated": "2026-05-28T17:00:00+10:00",
  "currency": "AUD",
  "afqa_retrospective": {
    "scope_label": "AFQA Compliance (26 products + 8 icons)",
    "rate_context": "mates_rate",
    "rate_explainer": "50% on master templates, 15% on clones, 25% on light updates, 100% on new products.",
    "invoices": [
      {
        "number": "INV-0354",
        "amount": 151.25,
        "date": "2026-01-15",
        "status": "paid",
        "scope": "Icons (8)"
      },
      {
        "number": "INV-0355",
        "amount": 1567.09,
        "date": "2026-01-15",
        "status": "paid",
        "scope": "Bars (6)"
      },
      {
        "number": "INV-0356",
        "amount": 2350.61,
        "date": "2026-01-15",
        "status": "paid",
        "scope": "Bar CDUs (6)"
      },
      {
        "number": "INV-0359",
        "amount": 1567.09,
        "date": "2026-01-25",
        "status": "paid",
        "scope": "Moons (6)"
      },
      {
        "number": "INV-0363",
        "amount": 4393.26,
        "date": "2026-02-04",
        "status": "paid",
        "scope": "Moon CDUs (6) + Banana CDU + Bananas 4-Pack"
      }
    ]
  },
  "website_progress": {
    "scope_label": "Shopify Build (10 line items)",
    "scope_total": 13206.00,
    "deposit_paid": 3961.80,
    "deposit_invoice": "INV-0369",
    "consumed_percent": 17,
    "remaining": 9244.20,
    "rate_context": "standard_with_goodwill",
    "line_items": [
      { "name": "Store setup",          "status": "in_progress", "weight": 12 },
      { "name": "Theme customisation",  "status": "in_progress", "weight": 18 },
      { "name": "Content pages",        "status": "not_started", "weight": 10 },
      { "name": "Klaviyo",              "status": "not_started", "weight": 8 },
      { "name": "GA4",                  "status": "not_started", "weight": 6 },
      { "name": "WooCommerce migration","status": "not_started", "weight": 12 },
      { "name": "Copywriting",          "status": "not_started", "weight": 12 },
      { "name": "Photo art direction",  "status": "in_progress", "weight": 10 },
      { "name": "Reviews",              "status": "not_started", "weight": 6 },
      { "name": "Training",             "status": "not_started", "weight": 6 }
    ]
  },
  "photoshoot": {
    "scope_label": "Photoshoot (weekend flat)",
    "rate_context": "mates_rate_flat",
    "rate_explainer": "Flat fee for Saturday prep + Sunday shoot, weekend total.",
    "invoices": [
      {
        "number": "C21_MM_07",
        "amount": 500.00,
        "date": "2026-05-28",
        "status": "draft",
        "scope": "Weekend prep + shoot"
      }
    ]
  }
}
```

Notes:

- The line-item weights sum to 100 and represent rough share of the Shopify scope, used to compute the consumed-percent bar visually. Weights are Nate's estimate, NOT a published milestone breakdown to Carli or Dylan. The 30/40/30 milestone split mentioned in the website spec is NOT used here (Carli and Dylan never saw it).
- AFQA invoice amounts sum to $10,029.30, while `FINAL_PRICING_BREAKDOWN.md` totals $10,029.28. The 2c delta is from cents-rounding across category subtotals; treat $10,029.30 as the invoice-level truth and $10,029.28 as the quote-level total. Display the quote-level total in any "Quote vs Paid" comparison.
- Quote reference C21_MM_07 is the format Nate used in the handoff. The actual Xero invoice number (`INV-NNNN` format) will be assigned at draft time in the parent session and the JSON updated accordingly. The Billing tab's renderer treats the `number` field as opaque (string), so both formats work.

### W3.3 Billing tab rendering

JS renderer reads `billing.json` once at init. Renders three DOM sections, each with its own section header showing scope label, scope total, and rate badge (where applicable). No top-level summary card; each scope owns its own framing.

- AFQA Retrospective: section header shows scope label + invoice total ($10,029.30) + MATES RATE pill. Body is a table of 5 paid invoices, each row showing scope + amount + invoice number + paid date with a PAID pill.
- Website Progress: section header shows scope label + scope total ($13,206) + consumed percentage. Body has a progress bar (filled to `consumed_percent`), a quick row of (deposit paid / remaining) numbers, then 10 line items as a list with a status pill per item.
- Photoshoot: section header shows scope label + total ($500) + MATES RATE pill. Body has a single invoice row showing scope + amount + invoice number + date with a BILLED pill.

### W3.4 Status pills

Reuse existing pill classes:

- DONE green (`--success-color #5A8F5A`) for paid invoices
- PARTIAL amber (`--warning-color #B8844A`) for in-progress line items
- NOT-STARTED grey (new, derive a `--neutral-color`) for not-started line items
- BILLED blue (use `--mm-deep-blue`) for draft invoices not yet sent
- PAID gold (new accent for the AFQA retrospective, derive a `--success-gold`)
- MATES RATE badge: lilac (`--mm-lilac #D8CFF2`) with darker text, distinct from status pills

### W3.5 Mates-rate display

A small lilac pill labeled "MATES RATE" appears in:

- AFQA section header (always, since `rate_context === "mates_rate"`)
- Photoshoot section header (always, since `rate_context === "mates_rate_flat"`)
- NOT on Website section (Shopify build is `standard_with_goodwill`, distinct)

The pill is decorative-explanatory, NOT a discount percentage. Carli and Dylan see that we acknowledge the rate context, they do not see internal margin math.

## Implementation order

1. W2 data consolidation (move two markdowns to `_archive/`, update README pointers) - cheap, no JS risk, lands first as a clean commit
2. W1.2 staleness display fix (JSON-driven init, remove `data-updated` attribute) - single function, one commit
3. W1.3 tab nav overflow CSS - small CSS-only diff, one commit
4. W3.2 author `data/billing.json` with the structure above
5. W3.1 + W3.3 + W3.4 + W3.5 add Billing tab markup + renderer + status pills + mates-rate display - one or two commits
6. W1.1 em-dash sweep across visible copy - one commit
7. W1.4 375px responsive add for any breaks found - one commit
8. Verification pass at 1440, 768, 480, 375

Each step ends with the dashboard still loadable, no broken state between commits.

## Verification checklist

To be confirmed in the verify phase, NOT pre-marked complete:

- Dashboard loads at `http://localhost:8765/` with no JS console errors
- `Quote and Invoice` tab still renders identically to pre-change baseline (visual diff acceptable only where palette polish was scoped)
- New `Billing` tab present in nav, clickable, content renders
- `billing.json` parses, all three sections populate
- AFQA Retrospective shows 5 paid invoices summing to $10,029.30, each row with a PAID pill
- Website Progress shows 17% bar, $13,206 scope, $3,961.80 deposit, $9,244 remaining, 10 line items with mixed in-progress / not-started pills
- Photoshoot shows quote ref C21_MM_07 at $500 with a BILLED pill
- MATES RATE pill present on AFQA header and Photoshoot header
- MATES RATE pill absent from Website section
- Staleness display reads "Updated 0 days ago" or "Updated today" at first load (will become stale naturally over time)
- Tab nav at 1404px shows all 12 tabs accessible (either visible or scrollable with overhang cue)
- Mobile at 480px: tab nav scrollable, sections stack vertically, no horizontal scroll on body
- Mobile at 375px: no horizontal scroll on body, all interactive elements reachable, all section content readable without overlap or clipping
- `grep "—" index.html | grep -vE '<!--|//' | wc -l` returns 0 (all visible em-dashes removed)
- `PRICING_CALCULATIONS.md` and `REVISED_PRICING.md` moved to `_archive/`, README updated
- Palette unchanged: `#7B9DBF` still absent (we are NOT migrating to cornflower this SPIN)
- No CLAUDE.md or memory file changes in the diff
- No `~/maplemoon-website` touches
- No Vercel deploy triggered

## Risks and rollback

| Risk | Mitigation |
| --- | --- |
| Em-dash sweep breaks inline CSS attribute (`style="border: 1px solid --var(--mm)"` etc) | Line-by-line review, exclude `<style>` blocks and `style="..."` attributes from sweep |
| `billing.json` typo crashes the renderer | Wrap render in try/catch, show fallback "Billing data load failed" message |
| Staleness display fix breaks if `project_status.json.lastUpdated` is missing | Fallback to "Recently updated" string, no crash |
| Tab nav scroll-snap not supported on older mobile Safari | Acceptable degradation: nav still scrolls, just without snap |
| New `Billing` tab disturbs deep-link routing | `initDeepLink()` already handles arbitrary `#tab` slugs; verify with `#billing` |

Rollback: branch is isolated, Nate reverts `feature/dashboard-cleanup-billing-merge` to `main` if anything ships wrong.

## Open questions resolved (from brainstorm gates)

- G1 palette: keep current `#457798 + #1E4366` blues. No cornflower migration this SPIN.
- G2 em-dash: full retroactive sweep across visible copy in `index.html` and README.md.
- G3 billing data: static `data/billing.json`, hand-curated. No live Xero.
- G4 polish scope: include staleness fix + tab overflow + 375px work in this SPIN.

## Communication-rules compliance

- No em-dashes in any client-visible copy added in this SPIN (banned per memory rule)
- Any client-readable copy in the Billing tab routes through `info@maplemoon.com.au` if it surfaces contact details
- No "Hi Dylan" or "Hi Carli" copy patterns; if the tab includes a greeting line it uses "Hey team"
- No third-party speak in tab copy ("so Mitch can review", "while Travis is around", etc)
- No mention of internal milestone splits (30/40/30 stays internal)

## Done when

1. Spec committed to `docs/superpowers/specs/`
2. Nate has reviewed the spec
3. Plan committed to `.planning/PLAN.md` via GSD plan-phase
4. All implementation order steps shipped on `feature/dashboard-cleanup-billing-merge`
5. Verification checklist all green
6. Branch ready for Nate's review as a PR-style diff against `main`
7. Handoff file appended with `## Status: DONE | <one-line summary>`
